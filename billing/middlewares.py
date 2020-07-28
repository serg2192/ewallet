import logging
import uuid

from aiohttp import web
from webargs.aiohttpparser import AIOHTTPParser, MultiDictProxy

from billing.errors import (
    CodeError,
    InvalidInputParamsError,
)
from billing.helpers import json_dumps
from billing.status_codes import (
    SUCCESS,
    get_message
)

logger = logging.getLogger(__name__)


class Parser(AIOHTTPParser):
    async def parse(self, argmap, req, **kwargs):
        # todo: log request
        return await super().parse(argmap, req, **kwargs)

    def handle_error(self, error, req, schema, **kwargs):
        raise InvalidInputParamsError(
            details=error.args
        )

    def load_files(self, req, schema):
        return super().load_files(req, schema)


parser = Parser()
loadreq = parser.use_args


@parser.location_loader("query_and_json")
async def load_query_and_json(request, schema):
    data = await request.json()
    data.update(request.query)
    return MultiDictProxy(data, schema)


@web.middleware
async def request_id_middleware(request, handler):
    request['request_id'] = str(uuid.uuid4())
    return await handler(request)


@web.middleware
async def base_response_middleware(request, handler):
    # noinspection PyBroadException
    try:
        res = await handler(request)
        # probably, the response can set the response code
        code = SUCCESS
        details = None
        msg = None

    except CodeError as exc:
        res = None
        code = exc.code
        details = exc.details
        msg = exc.msg
    except Exception as exc:
        logger.exception(f'Failed with {exc}')
        raise
    else:
        if isinstance(res, web.StreamResponse):
            # already formed response
            return res

    if msg is None:
        msg = get_message(request, code)

    response = {
        'data': res,
        'metadata': {
            'code': code,
            'message': msg,
            'details': details
        }
    }

    return web.json_response(
        data=response,
        status=200,  # todo: HTTP status from Error
        dumps=json_dumps
    )
