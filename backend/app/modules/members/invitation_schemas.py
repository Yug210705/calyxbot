"""Invitation schemas for request/response validation."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class InvitationCreate(BaseModel):
    email: EmailStr
    role: str = "employee"  # Default role for invitees


class InvitationResponse(BaseModel):
    id: uuid.UUID
    email: str
    organization_id: uuid.UUID
    role_id: uuid.UUID
    status: str
    invited_by: uuid.UUID
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InvitationAccept(BaseModel):
    token: str


class InvitationWithToken(BaseModel):
    """Returned only to the inviter — includes the raw token for the invite link."""
    invitation: InvitationResponse
    invite_url: str
