from asyncio import current_task
from logging import basicConfig
from os import environ

from fastapi.applications import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.log import InstanceLogger
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool.impl import AsyncAdaptedQueuePool
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route
from uvicorn import run

from .callbacks.create_visual_schema import create_visual_schema
from .methods._exception_handlers import sqlalchemy_error_handler
from .methods.endpoint import endpoint
from .middleware.async_sqlalchemy_middleware import AsyncSQLAlchemyMiddleware
from .middleware.misc_middleware import (
    logger_middleware,
    process_time_middleware,
)
from .models.base_interface import Base, DefaultORJSONResponse

#
if __name__ == '__main__':
    basicConfig(level=environ.get('LOGGING', 'INFO'))
    app = FastAPI(
        version='0.0.1',
        docs_url='/',
        default_response_class=DefaultORJSONResponse,
        on_startup=(lambda: create_visual_schema(Base.metadata),),
        exception_handlers={SQLAlchemyError: sqlalchemy_error_handler},
        middleware=(
            Middleware(BaseHTTPMiddleware, dispatch=process_time_middleware),
            Middleware(BaseHTTPMiddleware, dispatch=logger_middleware),
            # Middleware(HTTPSRedirectMiddleware),
            # Middleware(GZipMiddleware, minimum_size=1000),
            Middleware(
                AsyncSQLAlchemyMiddleware,
                metadata=Base.metadata,
                bind=async_scoped_session(
                    sessionmaker(
                        create_async_engine(
                            echo=InstanceLogger._echo_map.get(
                                environ.get('DB_ECHO'), None
                            ),
                            url='postgresql+asyncpg://'
                            '%(username)s:%(password)s@'
                            '%(endpoint)s:%(port)s/%(name)s'
                            % dict(
                                name=environ.get('DB_NAME', 'postgres'),
                                username=environ.get(
                                    'DB_USERNAME',
                                    'postgres',
                                ),
                                password=environ.get(
                                    'DB_PASSWORD',
                                    'postgres',
                                ),
                                endpoint=environ.get(
                                    'DB_ENDPOINT',
                                    'localhost',
                                ),
                                port=environ.get('DB_PORT', 5432),
                            ),
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
            Route(
                *('/{route}', endpoint),
                methods=['GET', 'POST', 'PUT', 'DELETE']
            ),
            Route('/{route}/{option}', endpoint),
        ],
    )
    run(
        app,
        host=environ.get('HOST', 'localhost'),
        port=int(environ.get('PORT', 8000)),
    )
