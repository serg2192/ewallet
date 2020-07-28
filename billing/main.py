import importlib
import logging

from aiohttp import web

from billing.settings import get_config
# from billing.resources.routes import set_routes

logger = logging.getLogger(__name__)

ON_STARTUP = (
    # 'billing.services.redis:on_startup',
)

ON_CLEANUP = (
    # 'billing.services.redis:on_cleanup',
)

MIDDLEWARE = (
    'billing.middlewares:request_id_middleware',
    'billing.middlewares:base_response_middleware',
)


def imp(path):
    module, attr = path.split(':')
    module = importlib.import_module(module)
    return getattr(module, attr)


def setup_routes(app):
    # set_routes(app)
    for i, resource in enumerate(app.router.resources(), start=1):
        logger.info(
            f'Route #{i:<4} --> {resource.canonical}, name={resource.name}'
        )


def init_app():
    config = get_config()
    app = web.Application()
    app['config'] = config
    for on_startup in ON_STARTUP:
        app.on_startup.append(imp(on_startup))
    for on_cleanup in ON_CLEANUP:
        app.on_cleanup.append(imp(on_cleanup))
    for middleware in MIDDLEWARE:
        app.middlewares.append(imp(middleware))
    setup_routes(app)
    return app


async def app_factory():
    return init_app()


if __name__ == '__main__':
    app = init_app()
    web.run_app(app=app, **app['config']['application'])
