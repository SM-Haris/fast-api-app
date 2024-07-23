from typing import Any, Awaitable, Callable

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared_utils.auth_utils import get_current_user


class AuthenticationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Any]]
    ) -> Any:
        # return await call_next(request)

        exempt_routes = [
            "/api/v1/user/signup",
            "/api/v1/user/login",
            "/",
            "/docs",
            "/favicon.ico",
            "/openapi.json",
        ]

        if request.url.path in exempt_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header is missing or invalid"},
            )

        token = auth_header.split(" ")[1]

        try:
            user_email = await get_current_user(token=token)
            request.state.user_email = user_email
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        response = await call_next(request)
        return response
