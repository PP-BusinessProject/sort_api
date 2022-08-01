from dataclasses import dataclass
from functools import partial
from inspect import isfunction, ismethod
from typing import Any, Callable, List, Optional, Tuple

from starlette.datastructures import URLPath
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette.routing import (
    BaseRoute,
    Match,
    NoMatchFound,
    compile_path,
    get_name,
    replace_params,
    request_response,
    websocket_session,
)
from starlette.types import Receive, Scope, Send
from typing_extensions import Self


@dataclass(init=False, frozen=True)
class CombinedRoute(BaseRoute):
    def __init__(
        self: Self,
        /,
        path: str,
        endpoint: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
        include_in_schema: bool = True,
    ) -> None:
        if not path.startswith('/'):
            raise ValueError("Routed paths must start with '/'")

        object.__setattr__(self, 'path', path)
        object.__setattr__(self, 'endpoint', endpoint)
        object.__setattr__(
            self, 'name', get_name(endpoint) if name is None else name
        )
        object.__setattr__(self, 'include_in_schema', include_in_schema)

        endpoint_handler = endpoint
        while isinstance(endpoint_handler, partial):
            endpoint_handler = endpoint_handler.func
        if methods is None and (
            isfunction(endpoint_handler) or ismethod(endpoint_handler)
        ):
            methods = ['GET']
        if methods is None:
            object.__setattr__(self, 'methods', None)
        else:
            if 'GET' in (_methods := {method.upper() for method in methods}):
                _methods.add('HEAD')
            object.__setattr__(self, 'methods', _methods)

        path_regex, path_format, param_convertors = compile_path(path)
        object.__setattr__(self, 'path_regex', path_regex)
        object.__setattr__(self, 'path_format', path_format)
        object.__setattr__(self, 'param_convertors', param_convertors)

    def matches(self: Self, /, scope: Scope) -> Tuple[Match, Scope]:
        if scope['type'] in {'http', 'websocket'} and (
            match := self.path_regex.match(scope['path'])
        ):
            matched_params = match.groupdict()
            for key, value in matched_params.items():
                matched_params[key] = self.param_convertors[key].convert(value)
            child_scope = {
                'endpoint': self.endpoint,
                'path_params': dict(scope.get('path_params', {}))
                | matched_params,
            }
            if scope['type'] == 'http' and (
                self.methods and scope['method'] not in self.methods
            ):
                return Match.PARTIAL, child_scope
            else:
                return Match.FULL, child_scope
        return Match.NONE, {}

    def url_path_for(self: Self, /, name: str, **path_params: Any) -> URLPath:
        seen_params = set(path_params.keys())
        expected_params = set(self.param_convertors.keys())
        if name != self.name or seen_params != expected_params:
            raise NoMatchFound(name, path_params)

        path, remaining_params = replace_params(
            self.path_format, self.param_convertors, path_params
        )
        if remaining_params:
            raise ValueError
        return URLPath(path)

    async def handle(
        self: Self,
        /,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope['type'] == 'http' and (
            self.methods and scope['method'] not in self.methods
        ):
            headers = {'Allow': ', '.join(self.methods)}
            if 'app' in scope:
                raise HTTPException(status_code=405, headers=headers)
            else:
                response = PlainTextResponse(
                    'Method Not Allowed', status_code=405, headers=headers
                )
            await response(scope, receive, send)
        else:
            app = None
            endpoint_handler = self.endpoint
            while isinstance(endpoint_handler, partial):
                endpoint_handler = endpoint_handler.func
            if isfunction(endpoint_handler) or ismethod(endpoint_handler):
                if scope['type'] == 'http':
                    app = request_response(self.endpoint)
                elif scope['type'] == 'websocket':
                    app = websocket_session(self.endpoint)
            await (app or self.endpoint)(scope, receive, send)

    def __eq__(self: Self, /, other: Any) -> bool:
        return (
            isinstance(other, CombinedRoute)
            and self.path == other.path
            and self.endpoint == other.endpoint
            and self.methods == other.methods
        )
