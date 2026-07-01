"""Authentication schemas."""

import uuid
from typing import Optional, Any
from pydantic import BaseModel, EmailStr


class OrganizationBase(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    is_active: bool

    class Config:
        from_attributes = True


class AuthBootstrapResponse(BaseModel):
    """Payload for /auth/me bootstrap endpoint."""
    user: UserBase
    current_organization: OrganizationBase | None = None
    permissions: list[str] = []
    feature_flags: dict[str, bool] = {}
    api_version: str = "v1.0"


class CompleteSignupRequest(BaseModel):
    """Payload from frontend to complete signup."""
    # Often the frontend might send metadata, but primarily we rely on the JWT token
    # to authenticate the request and extract user info.
    full_name: str | None = None
