from asyncio import current_task
from logging import basicConfig
from os import environ
from pathlib import Path
from typing import Final

from fastapi.applications import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool.impl import AsyncAdaptedQueuePool
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route
from uvicorn import run

from .callbacks.create_visual_schema import create_visual_schema
from .methods._exception_handlers import sqlalchemy_error_handler
from .methods.endpoint import endpoint
from .methods.schema import schema
from .middleware.async_sqlalchemy_middleware import AsyncSQLAlchemyMiddleware
from .middleware.misc_middleware import (
    AddToScopeMiddleware,
    logger_middleware,
    process_time_middleware,
)
from .models.base_interface import Base, DefaultORJSONResponse

# print(*(_ for _ in Base.metadata.tables if not _.startswith('_')), sep='\n')
basicConfig(level=environ.get('LOGGING', 'INFO'))
schema_path: Final[Path] = Path('./api/schema.png').resolve()
app = FastAPI(
    version='0.0.1',
    docs_url=None,
    default_response_class=DefaultORJSONResponse,
    on_startup=(
        lambda: create_visual_schema(Base.metadata, path=schema_path),
    ),
    exception_handlers={SQLAlchemyError: sqlalchemy_error_handler},
    middleware=(
        Middleware(AddToScopeMiddleware, scope=dict(schema_path=schema_path)),
        Middleware(BaseHTTPMiddleware, dispatch=process_time_middleware),
        Middleware(BaseHTTPMiddleware, dispatch=logger_middleware),
        *(
            (Middleware(HTTPSRedirectMiddleware),)
            if 'DATABASE_URL' in environ
            else ()
        ),
        Middleware(
            AsyncSQLAlchemyMiddleware,
            metadata=Base.metadata,
            bind=async_scoped_session(
                sessionmaker(
                    create_async_engine(
                        echo=environ.get('LOGGING', '').upper() == 'DEBUG',
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
            ),
        ),
    ),
    routes=[
        Route('/', schema),
        Route(
            *('/{route}', endpoint),
            methods=['GET', 'POST', 'PUT', 'DELETE'],
        ),
        Route('/{route}/{option}', endpoint),
    ],
)

if 'DATABASE_URL' not in environ:
    run(app, host='localhost', port=8000)
