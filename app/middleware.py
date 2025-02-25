import time
import uuid
from typing import Callable

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize the LoggingMiddleware."""
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Dispatch the request and log details."""
        request_id = str(uuid.uuid4())

        with logger.contextualize(request_id=request_id):
            logger.info(
                "Request",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "client_host": request.client.host if request.client else None,
                },
            )

            start_time = time.time()

            try:
                response = await call_next(request)
                process_time = time.time() - start_time

                logger.info(
                    "Response",
                    extra={
                        "status_code": response.status_code,
                        "processing_time": f"{process_time:.4f}s",
                    },
                )

                return response

            except Exception as e:
                process_time = time.time() - start_time
                logger.error(
                    f"Request failed: {str(e)}",
                    extra={
                        "processing_time": f"{process_time:.4f}s",
                        "error": str(e),
                    },
                )
                raise
