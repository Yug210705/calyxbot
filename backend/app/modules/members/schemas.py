import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.modules.auth.schemas import UserBase

class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)

class MembershipResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    # We include full nested objects for convenience on the frontend
    user: Optional[UserBase] = None
    role: Optional[RoleResponse] = None

    model_config = ConfigDict(from_attributes=True)

class PaginatedMembershipResponse(BaseModel):
    items: list[MembershipResponse]
    total: int
    limit: int
    offset: int
