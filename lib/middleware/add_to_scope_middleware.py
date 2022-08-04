from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Final, Mapping, Union

from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send
from typing_extensions import Self


@dataclass(init=False, frozen=True)
class AddToScopeMiddleware(object):

    app: Final[ASGIApp]
    scope: Final[
        Union[
            Mapping[str, Any],
            Callable[[Mapping[str, Any]], Mapping[str, Any]],
        ]
    ]

    def __init__(
        self: Self,
        /,
        app: ASGIApp,
        scope: Union[
            Mapping[str, Any],
            Callable[[Mapping[str, Any]], Mapping[str, Any]],
        ],
    ) -> None:
        object.__setattr__(self, 'app', app)
        object.__setattr__(
            self,
            'scope',
            MappingProxyType(scope) if isinstance(scope, dict) else scope,
        )

    async def __call__(
        self: Self,
        /,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> Response:
        merge = (
            self.scope if isinstance(self.scope, dict) else self.scope(scope)
        )
        return await self.app(scope | merge, receive, send)
