from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
from fastapi import Request, Response


class RouterCacheControlResetMiddleware(BaseHTTPMiddleware):
    """Disable Response headers Cache-Control (set to 'no-cache').

    The initial reason for this is that the fastapi-cache library sets the max-age param of the header
    equal to the expire parameter that is provided to the caching layer (Redis),
    so the response is also cached on the browser side, which in most cases is unnecessary."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response: Response = await call_next(request)
        response.headers.update({"Cache-Control": "no-cache"})
        return response
