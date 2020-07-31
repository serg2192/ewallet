import logging

import aiopg.sa

logger = logging.getLogger(__name__)


async def on_startup(app):
    logger.info('Starting up: PostgreSQL')
    pool = await aiopg.sa.create_engine(**app['config']['db'])
    app['db_pool'] = pool


async def on_cleanup(app):
    logger.info('Cleaning up: PostgreSQL')
    app['db_pool'].close()
    await app['db_pool'].wait_closed()
