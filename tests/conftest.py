import pytest

from billing.main import init_app


@pytest.fixture#(scope='session')
def app():
    print('making app')
    yield init_app()
    print('closing app')


@pytest.fixture#(scope='session')
async def cli(aiohttp_client, app):
    # app = init_app()
    # return loop.run_until_complete(aiohttp_client(app))
    print('making client')
    app_client = await aiohttp_client(app)
    yield app_client
    await app_client.close()
    # return loop.run_until_complete(aiohttp_client(app))
    print('closing client')
