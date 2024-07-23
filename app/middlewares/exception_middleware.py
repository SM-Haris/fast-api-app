import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("fastapi")


class UnexpectedErrorMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            logger.info(f"Request: {request.method} {request.url}")
            response = await call_next(request)
            logger.info(f"Response: {response.status_code} {request.url}")

            return response
        except Exception as exc:
            logger.error(f"Error: {500} {exc} {request.url}")

            logging.exception("An unexpected error occurred.")
            return JSONResponse(
                status_code=500,
                content={"detail": "Something went wrong"},
            )
