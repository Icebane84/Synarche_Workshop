import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that assigns a unique ID to each request and sets up
    logging context.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())

        # Create a context-aware logger for this request
        with logger.contextualize(request_id=request_id):
            start_time = time.time()

            # Add request ID to request state for access in routers
            request.state.request_id = request_id

            logger.info(f"Started request: {request.method} {request.url.path}")

            try:
                response = await call_next(request)

                # Add request ID to response headers
                response.headers["X-Request-ID"] = request_id

                process_time = (time.time() - start_time) * 1000
                logger.info(
                    f"Completed request: {response.status_code} "
                    f"in {process_time:.2f}ms"
                )

                return response
            except Exception as e:
                process_time = (time.time() - start_time) * 1000
                logger.error(f"Request failed: {e!s} " f"in {process_time:.2f}ms")
                raise
