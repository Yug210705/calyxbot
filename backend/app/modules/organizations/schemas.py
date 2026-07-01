from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100, pattern=r'^[a-z0-9-]+$')

class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    logo_url: str | None = None
    plan: str
    status: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
