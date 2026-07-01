"""Standard API response builders.

Utility functions for constructing consistent API response envelopes
matching the approved response format specification.
"""
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str | None = None
    timestamp: str | None = None
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


def create_error_response(
    code: str,
    message: str,
    request_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> ErrorResponse:
    return ErrorResponse(
        success=False,
        error=ErrorDetail(
            code=code,
            message=message,
            request_id=request_id,
            timestamp=datetime.now(UTC).isoformat(),
            details=details,
        ),
    )


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta: dict[str, Any] = Field(default_factory=dict)


def create_success_response(
    data: T, request_id: str | None = None, meta: dict[str, Any] | None = None
) -> SuccessResponse[T]:
    meta_dict = meta or {}
    if request_id:
        meta_dict["request_id"] = request_id
    meta_dict["timestamp"] = datetime.now(UTC).isoformat()

    return SuccessResponse(success=True, data=data, meta=meta_dict)
