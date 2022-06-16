from dataclasses import dataclass
from logging import Logger
from types import TracebackType
from typing import Final, Optional, Type, Union

from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session as SyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import MetaData
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from typing_extensions import Self

from ..utils.anyfunction import anycorofunction


@dataclass(init=False, frozen=True)
class AsyncSQLAlchemyMiddleware(BaseHTTPMiddleware):

    logger: Final[Logger]
    app: Final[ASGIApp]
    engine: Final[Union[Engine, AsyncEngine]]
    Session: Final[
        Union[None, sessionmaker, scoped_session, async_scoped_session]
    ]
    metadata: Final[MetaData]

    def __init__(
        self: Self,
        /,
        app: ASGIApp,
        bind: Union[
            Union[scoped_session, SyncSession, Connection, Engine],
            async_scoped_session,
            AsyncSession,
            AsyncConnection,
            AsyncEngine,
        ],
        metadata: MetaData,
    ) -> None:
        if not isinstance(metadata, MetaData):
            raise ValueError(f'Invalid metadata: {metadata}')

        Session = None
        while not isinstance(bind, (Engine, AsyncEngine)):
            if isinstance(bind, (scoped_session, async_scoped_session)):
                if Session is None:
                    Session = bind
                bind = bind.session_factory
            elif isinstance(bind, sessionmaker):
                if Session is None:
                    Session = bind
                bind = bind.kw['bind']
            elif isinstance(bind, (SyncSession, AsyncSession)):
                bind = bind.bind
            elif isinstance(bind, (Connection, AsyncConnection)):
                bind = bind.engine
            else:
                raise ValueError(f'Invalid bind: {bind}')

        object.__setattr__(self, 'logger', Logger(self.__class__.__name__))
        object.__setattr__(self, 'app', app)
        object.__setattr__(self, 'dispatch_func', self.dispatch)
        object.__setattr__(self, 'engine', bind)
        object.__setattr__(self, 'Session', Session)
        object.__setattr__(self, 'metadata', metadata)

    async def start(self: Self, /) -> Self:
        if self.metadata.is_bound():
            self.logger.debug('Metadata Tables creation skipped.')
            return self

        self.logger.info('Metadata Tables creation.')
        if isinstance(self.engine, Engine):
            with self.engine.begin() as connection:
                self.metadata.create_all(connection)
                self.metadata.bind = self.engine
                return self

        async with self.engine.begin() as connection:
            await connection.run_sync(self.metadata.create_all)
            self.metadata.bind = self.engine
            return self

    async def stop(self: Self, /, *, dispose: bool = True) -> None:
        try:
            if (remove := getattr(self.Session, 'remove', None)) is not None:
                self.logger.debug('Scoped Session removal.')
                await anycorofunction(remove)
            else:
                self.logger.debug('Scoped Session removal skipped.')
        finally:
            if dispose:
                self.logger.info('Engine disposal.')
                await anycorofunction(self.engine.dispose)
            else:
                self.logger.debug('Engine disposal skipped.')

    async def __aenter__(self: Self) -> Self:
        return await self.start()

    async def __aexit__(
        self: Self,
        /,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.stop(dispose=exc_val is not None)

    async def dispatch(
        self: Self,
        request: Request,
        call_next: RequestResponseEndpoint,
        /,
    ) -> Response:
        async with self:
            request.scope['engine'] = self.engine
            request.scope['Session'] = self.Session
            request.scope['metadata'] = self.metadata
            return await call_next(request)
