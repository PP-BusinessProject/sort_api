from logging import Logger
from time import monotonic

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


async def process_time_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
    /,
) -> Response:
    start_time = monotonic()
    response = await call_next(request)
    response.headers['X-Process-Time'] = f'{monotonic() - start_time:.6}'
    return response


async def logger_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    request.scope['logger'] = Logger('%(method)s %(path)s' % request.scope)
    return await call_next(request)
