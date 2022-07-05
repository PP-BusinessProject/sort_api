from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import Response


async def sqlalchemy_error_handler(
    request: Request,
    exception: SQLAlchemyError,
    /,
) -> Response:
    sa_exception = dialect_exception = text = None
    if message := next(iter(exception.args), ''):
        exceptions, _, text = message.partition(':')
        sa_exception, _, dialect_exception = exceptions.partition(' ')
        sa_exception = sa_exception.removeprefix('(').removesuffix(')')
        dialect_exception = (
            dialect_exception.split(' ', 1)[-1].removesuffix('>').strip('\'')
        )
        text = text.split('DETAIL:')[-1].strip()
    return ORJSONResponse(
        status_code=500,
        content={
            k: v
            for k, v in dict(
                sqlalchemy_exception=sa_exception
                or exception.__class__.__name__,
                dialect_exception=dialect_exception,
                detail=text,
            ).items()
            if v is not None
        },
    )
