from billing.middlewares import loadreq
from billing.resources import schemas
from billing.services.postgres import views as p_views


@loadreq(schemas.CreateAccountSchema, location='json')
async def create_account(req, inp):
    """Создание кошелька"""
    return await p_views.create_account(req, inp)


@loadreq(schemas.AddMoneySchema, location='json')
async def add_money(req, inp):
    """Пополнение кошелька"""
    return await p_views.add_money(req, inp)


@loadreq(schemas.TransferSchema, location='json')
async def transfer(req, inp):
    """Перевод между кошельками"""
    return await p_views.transfer(req, inp)
