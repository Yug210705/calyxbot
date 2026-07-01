"""Custom exception hierarchy and global handlers.

Defines CalyxException and its subclasses for structured error handling.
"""

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.shared.response import create_error_response
from app.core.logging import request_id_var

logger = structlog.get_logger(__name__)


class CalyxException(Exception):
    """Base exception for all custom Calyx errors."""

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: dict | None = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for the application."""

    @app.exception_handler(CalyxException)
    async def calyx_exception_handler(
        request: Request, exc: CalyxException
    ) -> JSONResponse:
        logger.warning(
            "CalyxException caught",
            error_code=exc.error_code,
            message=exc.message,
            status_code=exc.status_code,
        )
        response_model = create_error_response(
            code=exc.error_code,
            message=exc.message,
            request_id=request_id_var.get(),
            details=exc.details,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response_model.model_dump(exclude_none=True),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception caught", error=str(exc))
        response_model = create_error_response(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred.",
            request_id=request_id_var.get(),
        )
        return JSONResponse(
            status_code=500,
            content=response_model.model_dump(exclude_none=True),
        )
