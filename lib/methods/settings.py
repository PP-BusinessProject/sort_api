from datetime import datetime

from dateutil.tz.tz import tzlocal
from starlette.requests import Request
from starlette.responses import Response


async def current_time(request: Request, /) -> Response:
    return Response(datetime.now(tzlocal()).isoformat())
