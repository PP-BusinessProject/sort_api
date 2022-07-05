from dataclasses import dataclass
from logging import Logger
from time import monotonic
from types import MappingProxyType
from typing import Any, Final, Mapping

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from typing_extensions import Self


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


@dataclass(init=False, frozen=True)
class AddToScopeMiddleware(BaseHTTPMiddleware):

    scope: Final[MappingProxyType[str, Any]]

    def __init__(
        self: Self,
        /,
        app: ASGIApp,
        scope: Mapping[str, Any],
    ) -> None:
        object.__setattr__(self, 'app', app)
        object.__setattr__(self, 'dispatch_func', self.dispatch)
        object.__setattr__(self, 'scope', MappingProxyType(scope))

    async def dispatch(
        self: Self,
        request: Request,
        call_next: RequestResponseEndpoint,
        /,
    ) -> Response:
        request.scope.update(self.scope)
        return await call_next(request)
