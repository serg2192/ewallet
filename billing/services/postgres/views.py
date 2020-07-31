from billing.services.postgres.base import (
    UserNotFoundError,
    NotEnoughMoneyError,
)
from billing.models import public as p_models


async def create_account(req, inp):
    """Создание кошелька"""
    pool = req.app['db_pool']
    balance = inp.get('balance', 0)
    async with pool.acquire() as conn, conn.begin() as trans:
        row = await conn.execute(
            p_models.users.insert().values()
        )
        user = await row.first()
        await conn.execute(
            p_models.wallets.insert().values(
                w_user_id=user.u_id,
                w_balance=balance
            )
        )
        await trans.commit()
    return {"user_id": user.u_id}


async def add_money(req, inp):
    """Пополнение кошелька"""
    pool = req.app['db_pool']
    async with pool.acquire() as conn, conn.begin() as trans:
        r = await conn.execute(
            p_models.wallets.select().where(
                p_models.wallets.c.w_user_id == inp['user_id']
            )
        )
        wallet = await r.first()
        if not wallet:
            raise UserNotFoundError
        await conn.execute(
            p_models.wallets.update().values(
                w_balance=wallet.w_balance+inp['amount']
            ).where(
                p_models.wallets.c.w_id == wallet.w_id
            )
        )
        await conn.execute(
            p_models.transactions.insert().values(
                t_wallet_id=wallet.w_id,
                t_user_id=wallet.w_user_id,
                t_volume=inp['amount']
            )
        )
        await trans.commit()
    return


async def transfer(req, inp):
    """Перевод между кошельками"""
    pool = req.app['db_pool']
    source = inp['source_user_id']
    target = inp['target_user_id']
    amount = inp['amount']
    async with pool.acquire() as conn, conn.begin() as trans:
        rows = await conn.execute(
            p_models.wallets.select().where(
                p_models.wallets.c.w_user_id.in_(
                    (source, target)
                )
            )
        )
        wallets = await rows.fetchall()
        if len(wallets) != 2:
            raise UserNotFoundError
        source_w = [w for w in wallets if w.w_user_id == source][0]
        target_w = [w for w in wallets if w.w_user_id == target][0]
        if source_w.w_balance < amount:
            raise NotEnoughMoneyError
        await conn.execute(
            p_models.wallets.update().values(
                w_balance=target_w.w_balance+amount
            ).where(
                p_models.wallets.c.w_id == target_w.w_id
            )
        )
        await conn.execute(
            p_models.transactions.insert().values(
                t_wallet_id=target_w.w_id,
                t_user_id=source_w.w_user_id,
                t_volume=amount
            )
        )

        await conn.execute(
            p_models.wallets.update().values(
                w_balance=source_w.w_balance-amount
            ).where(
                p_models.wallets.c.w_id == source_w.w_id
            )
        )
        await conn.execute(
            p_models.transactions.insert().values(
                t_wallet_id=source_w.w_id,
                t_user_id=target_w.w_user_id,
                t_volume=-amount
            )
        )
        await trans.commit()
    return
