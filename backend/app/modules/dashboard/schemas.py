from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class DashboardStatsResponse(BaseModel):
    connected_sources: int
    documents_total: int
    knowledge_objects_total: int
    last_sync_at: datetime | None

class DashboardActivityItemResponse(BaseModel):
    id: str
    type: Literal["sync_success", "sync_failed", "document_added", "document_updated"]
    title: str
    description: str
    created_at: datetime
    status: str | None = None

class DashboardChecklistItemResponse(BaseModel):
    id: str
    label: str
    completed: bool
    href: str | None = None

class DashboardResponse(BaseModel):
    stats: DashboardStatsResponse
    activity: list[DashboardActivityItemResponse]
    checklist: list[DashboardChecklistItemResponse]
    system_health: dict
