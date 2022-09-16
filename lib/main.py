from asyncio import current_task
from datetime import datetime
from logging import Filter, Logger, LogRecord, basicConfig, getLogger
from os import environ
from pathlib import Path
from typing import Any, Final
from urllib.parse import unquote

from dateutil.tz.tz import tzlocal
from fastapi.applications import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.security.oauth2 import OAuth2PasswordBearer
from orjson import dumps
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool.impl import AsyncAdaptedQueuePool
from starlette.middleware import Middleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette_authlib.middleware import AuthlibMiddleware
from typing_extensions import Self
from uvicorn import run

from .callbacks.create_visual_schema import create_visual_schema
from .methods._exception_handlers import sqlalchemy_error_handler
from .methods.endpoint import endpoint, endpoint_info
from .methods.schema import schema
from .methods.test_database import test_database
from .middleware.add_to_scope_middleware import AddToScopeMiddleware
from .middleware.async_sqlalchemy_middleware import AsyncSQLAlchemyMiddleware
from .models.base_interface import Base, serialize


class _DefaultORJSONResponse(JSONResponse):
    media_type: Final[str] = 'application/json'

    def render(self: Self, content: Any, /) -> bytes:
        return dumps(content, default=serialize)


class _EndpointFilter(Filter):
    def filter(self: Self, record: LogRecord, /) -> bool:
        record.args = list(record.args)
        record.args[2] = unquote(record.args[2].replace('+', ' '))
        record.args = tuple(record.args)
        return True


# print(*(_ for _ in Base.metadata.tables if not _.startswith('_')), sep='\n')
basicConfig(level=environ.get('LOGGING', 'INFO'))
getLogger('uvicorn.access').addFilter(_EndpointFilter())
schema_path: Final[Path] = Path('./lib/schema.png').resolve()
sqlalchemy: Final = async_scoped_session(
    sessionmaker(
        create_async_engine(
            echo=True,  # environ.get('LOGGING', '').upper() == 'DEBUG',
            url='postgresql+asyncpg://'
            + environ.get(
                'DATABASE_URL',
                'postgres:postgres@localhost:5432/postgres',
            ).split('://')[-1],
            poolclass=AsyncAdaptedQueuePool,
            pool_size=1,
            max_overflow=-1,
            pool_recycle=3600,
            pool_pre_ping=True,
            pool_use_lifo=True,
            connect_args=dict(server_settings=dict(jit='off')),
        ),
        class_=AsyncSession,
        expire_on_commit=False,
        future=True,
    ),
    scopefunc=current_task,
)


async def _create_visual_schema() -> None:
    return await create_visual_schema(Base.metadata, path=schema_path)


app = FastAPI(
    version='0.0.1',
    docs_url=None,
    default_response_class=_DefaultORJSONResponse,
    on_startup=(_create_visual_schema,),
    exception_handlers={SQLAlchemyError: sqlalchemy_error_handler},
    dependencies=[OAuth2PasswordBearer(tokenUrl='token')],
    middleware=(
        Middleware(
            AuthlibMiddleware,
            secret_key='d716b68b370baa9bbb73ad5e121a0c21b1a8aa3f9800db61',
        ),
        Middleware(
            AddToScopeMiddleware,
            scope=lambda scope: dict(
                schema_path=schema_path,
                logger=Logger('%(method)s %(path)s' % scope)
                if scope['type'] == 'http'
                else None,
            ),
        ),
        *(
            (Middleware(HTTPSRedirectMiddleware),)
            if 'DATABASE_URL' in environ
            else ()
        ),
        Middleware(AsyncSQLAlchemyMiddleware, metadata=Base, bind=sqlalchemy),
    ),
    routes=[
        Route('/', schema),
        Route('/settings/test', test_database),
        Route(
            '/settings/time',
            lambda request: Response(datetime.now(tzlocal()).isoformat()),
        ),
        Route('/settings/info', endpoint_info),
        *(
            Route(
                '/'.join(
                    ('/{route}', *('{option%s}' % (i + 1) for i in range(i)))
                ),
                endpoint,
                methods=['GET', 'POST', 'PUT', 'DELETE'],
            )
            for i in range(4)
        ),
    ],
)

if 'DATABASE_URL' not in environ:
    run(app, host='localhost', port=8000, http='h11', loop='asyncio')
