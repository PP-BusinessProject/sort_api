from pathlib import Path

from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse, Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


async def schema(request: Request, /) -> Response:
    if not isinstance(schema_path := request.scope.get('schema_path'), Path):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'Schema path is not present.'
        )
    elif not schema_path.exists():
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'Schema path does not exist.'
        )
    return FileResponse(schema_path, filename=schema_path.name)
