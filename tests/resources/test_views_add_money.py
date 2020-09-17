# import typing
# import decimal
#
# from aiohttp.test_utils import TestClient
# import pytest
#
# from billing.models import public as p_models
#
# # todo: Подумать
# #  - можно отдельно написать тесты на хелпер
# #  с помощью роллбэка транзакций,
# # а потом мокировать вызовы хелпера и тестить вью
#
#
# @pytest.fixture
# async def populate_data(app):
#     redis_client = app['db_pool']
#     records = []
#
#     async def init(data: typing.Sequence[typing.Sequence]):
#         print(f'Initializing data: {data}')
#         if data is None:
#             return
#         for key, field, value in data:
#             await redis_client.hset(key, field, value)
#             records.append(key)
#     yield init
#     # print(f'Cleaning data: {records}')
#     # if records:
#     #     await redis_client.delete(*records)
#
#
# # @pytest.fixture
# # async def clear_cache(app):
# #     yield
# #     print(f'Cleaning data.')
# #     await app['redis_cache_pool'].flushdb()
#
#
# @pytest.mark.parametrize(
#     "req_data,expected_res,expected_res_partially,expected_db_data",
#     [
#         pytest.param(
#             {'balance': -100},
#             {
#                 'data': None,
#                 'metadata': {
#                     'code': 100,
#                     'details': [
#                         {'balance': ['Value must be greater than 0.']}
#                     ],
#                     'message': 'Переданы неверные входные параметры'
#                 }
#             },
#             False,
#             None,
#             id='invalid parameters passed - negative balance'
#         ),
#         pytest.param(
#             {'balance': None},
#             {
#                 'data': None,
#                 'metadata': {
#                     'code': 100,
#                     'details': [
#                         {'balance': ['Field may not be null.']}
#                     ],
#                     'message': 'Переданы неверные входные параметры'
#                 }
#             },
#             False,
#             None,
#             id='invalid parameters passed - None balance'
#         ),
#         pytest.param(
#             {},
#             {'metadata': {'code': 0, 'details': None, 'message': 'Успех'}},
#             True,
#             {'balance': 0},
#             id='straightforward user creation'
#         ),
#         pytest.param(
#             {'balance': 100.32},
#             {'metadata': {'code': 0, 'details': None, 'message': 'Успех'}},
#             True,
#             {'balance': decimal.Decimal('100.32')},
#             id='user with initial balance'
#         ),
#     ]
# )
# async def test_create_account(
#         cli: TestClient,
#         # populate_data,
#         req_data,
#         expected_res,
#         expected_res_partially,
#         expected_db_data
# ):
#     res = await cli.request('POST', '/create_account', json=req_data)
#     res_json = await res.json()
#     assert res.status == 200
#     if expected_res_partially:
#         check_with_reference(res_json, expected_res)
#     else:
#         assert res_json == expected_res
#
#     if expected_db_data:
#         user_id = res_json['data']['user_id']
#         if req_data.get('balance') is not None:
#             await check_db_data(cli.app, user_id, expected_db_data)
#
#
# # @pytest.mark.parametrize(
# #     "init_data,req_data,req_params,expected_res,expected_data",
# #     [
# #         pytest.param(
# #             None,  # предзаполнить данными
# #             {},  # пэйлоад реквеста
# #             {},  # параметры реквеста
# #             {  # ожидаемый ответ сервиса
# #
# #                 "data": None,
# #                 "metadata": {
# #                     "code": 100,
# #                     "message": "Переданы неверные входные параметры",
# #                     "details": [
# #                         {
# #                             'merge': ['Missing data for required field.'],
# #                             'rates': ['Missing data for required field.']
# #                         }
# #                     ]
# #                 }
# #             },
# #             None,  # ожидаемые данные в хранилище
# #             id='invalid parameters passed'
# #         ),
# #         pytest.param(
# #             [('RUB', 'USD', 60)],
# #             {"rates": [{"from": "EUR", "to": "RUB", "rate": 78.50}]},
# #             {"merge": 0},
# #             {"data": None, "metadata": {"code": 0, "message": "Успех", "details": None}},
# #             {"EUR": {"RUB": "78.5"}, "RUB": {"EUR": "0.012738853503184714"}},
# #             id='replace the database'
# #         ),
# #         pytest.param(
# #             [('RUB', 'USD', 60)],
# #             {"rates": [{"from": "EUR", "to": "RUB", "rate": 78.50}]},
# #             {"merge": 1},
# #             {"data": None, "metadata": {"code": 0, "message": "Успех", "details": None}},
# #             {"EUR": {"RUB": "78.5"}, "RUB": {"EUR": "0.012738853503184714", "USD": "60"}},
# #             id='update the database'
# #         ),
# #         pytest.param(
# #             [('RUB', 'USD', 60)],
# #             {"rates": [
# #                 {"from": "EUR", "to": "RUB", "rate": 78.50},
# #                 {"from": "RUB", "to": "EUR", "rate": 0.0001},
# #             ]},
# #             {"merge": 1},
# #             {"data": None, "metadata": {"code": 0, "message": "Успех", "details": None}},
# #             {"EUR": {"RUB": "10000.0"}, "RUB": {"EUR": "0.0001", "USD": "60"}},
# #             id='update the database. v2'
# #         ),
# #     ]
# # )
# # async def test_database(
# #         cli: TestClient,
# #         populate_data,
# #         init_data,
# #         req_data,
# #         req_params,
# #         expected_res,
# #         expected_data
# # ):
# #     await populate_data(init_data)
# #     res = await cli.request('POST', '/database', json=req_data, params=req_params)
# #     res_json = await res.json()
# #
# #     await check_with_reference(
# #         cli.app['redis_cache_pool'],
# #         expected_data
# #     )
# #
# #     assert res_json == expected_res
#
#
# async def check_db_data(app, user_id, data):
#     pg_client = app['db_pool']
#     async with pg_client.acquire() as conn:
#         row = await conn.execute(
#             p_models.wallets.select().where(
#                 p_models.wallets.c.w_user_id == user_id
#             )
#         )
#         wallet = await row.first()
#         assert wallet.w_balance == data['balance']
#         row = await conn.execute(
#             p_models.transactions.select().where(
#                 p_models.transactions.c.t_wallet_id == wallet.w_id
#             )
#         )
#         transaction = await row.first()
#         assert transaction.t_user_id == user_id
#         assert transaction.t_volume == data['balance']
#
#
# def check_with_reference(response, reference):
#     for k, v in reference.items():
#         assert response[k] == v
