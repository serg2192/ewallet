from billing.services.postgres import helpers


async def create_account(req, inp):
    """Создание кошелька"""
    pool = req.app['db_pool']
    async with pool.acquire() as conn, conn.begin() as trans:
        user = await helpers.create_account(
            conn,
            inp.get('balance')
        )
        await trans.commit()
    return {"user_id": user.u_id}


async def add_money(req, inp):
    """Пополнение кошелька"""
    pool = req.app['db_pool']
    async with pool.acquire() as conn, conn.begin() as trans:
        _ = await helpers.add_money(
            connection=conn,
            user_id=inp['user_id'],
            amount=inp['amount']
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
        await helpers.transfer(
            connection=conn,
            source=source,
            target=target,
            amount=amount
        )
        await trans.commit()
    return
