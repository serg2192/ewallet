from aiopg.sa import SAConnection, result

from billing.models import public as p_models
from billing.services.postgres.base import (
    UserNotFoundError,
    NotEnoughMoneyError,
)


async def create_account(
        connection: SAConnection,
        balance=0
) -> result.RowProxy:
    row = await connection.execute(
        p_models.users.insert().values()
    )
    user = await row.first()
    row = await connection.execute(
        p_models.wallets.insert().values(
            w_user_id=user.u_id,
            w_balance=balance
        )
    )
    wallet = await row.first()
    # Храним зачисление, если оно было
    if balance > 0:
        await connection.execute(
            p_models.transactions.insert().values(
                t_wallet_id=wallet.w_id,
                t_user_id=user.u_id,
                t_volume=balance
            )
        )
    return user


async def add_money(
        connection: SAConnection,
        user_id,
        amount
):
    row = await connection.execute(
        p_models.wallets.select().where(
            p_models.wallets.c.w_user_id == user_id
        )
    )
    wallet = await row.first()
    if not wallet:
        raise UserNotFoundError
    await connection.execute(
        p_models.wallets.update().values(
            w_balance=wallet.w_balance + amount
        ).where(
            p_models.wallets.c.w_id == wallet.w_id
        )
    )
    await connection.execute(
        p_models.transactions.insert().values(
            t_wallet_id=wallet.w_id,
            t_user_id=wallet.w_user_id,
            t_volume=amount
        )
    )
    return


async def transfer(
        connection: SAConnection,
        source,
        target,
        amount
):
    rows = await connection.execute(
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
    await connection.execute(
        p_models.wallets.update().values(
            w_balance=target_w.w_balance + amount
        ).where(
            p_models.wallets.c.w_id == target_w.w_id
        )
    )
    await connection.execute(
        p_models.transactions.insert().values(
            t_wallet_id=target_w.w_id,
            t_user_id=source_w.w_user_id,
            t_volume=amount
        )
    )

    await connection.execute(
        p_models.wallets.update().values(
            w_balance=source_w.w_balance - amount
        ).where(
            p_models.wallets.c.w_id == source_w.w_id
        )
    )
    await connection.execute(
        p_models.transactions.insert().values(
            t_wallet_id=source_w.w_id,
            t_user_id=target_w.w_user_id,
            t_volume=-amount
        )
    )
    return
