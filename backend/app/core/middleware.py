"""Application middleware.

Request ID generation, organization context resolution,
rate limiting, and global exception handling.
"""

import time
import uuid

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.logging import request_id_var, correlation_id_var

logger = structlog.get_logger(__name__)


class RequestIDAndLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to assign a unique request ID and log request lifecycles."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Extract or generate Request ID and Correlation ID
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        
        # Set the context variables
        token_req = request_id_var.set(req_id)
        token_corr = correlation_id_var.set(corr_id)
        request.state.request_id = req_id
        request.state.correlation_id = corr_id

        start_time = time.perf_counter()

        logger.info(
            "Request started",
            endpoint=request.url.path,
            method=request.method,
        )

        try:
            response = await call_next(request)
            
            # Attach X-Request-ID to the response
            response.headers["X-Request-ID"] = req_id
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            logger.info(
                "Request completed",
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )
            
            return response
            
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "Request failed with unhandled exception",
                endpoint=request.url.path,
                method=request.method,
                duration_ms=round(duration_ms, 2),
                error=str(e),
            )
            raise
        finally:
            # Reset the context variable
            request_id_var.reset(token_req)
            correlation_id_var.reset(token_corr)
