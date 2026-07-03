from datetime import datetime
import uuid
from pydantic import BaseModel

class ProcessingTimelineItem(BaseModel):
    key: str
    label: str
    status: str  # completed | current | pending | failed
    timestamp: datetime | None = None

class DocumentListItemResponse(BaseModel):
    id: uuid.UUID
    title: str
    provider: str
    source: str | None = None
    mime_type: str
    status: str
    version: int
    chunk_count: int
    updated_at: datetime
    last_synced_at: datetime | None = None
    knowledge_object_count: int | None = 0

class DocumentDetailResponse(DocumentListItemResponse):
    checksum: str
    created_at: datetime
    processing_timeline: list[ProcessingTimelineItem]
    graph_relation_count: int | None = 0
    page_count: int | None = None
    section_count: int | None = None

class DocumentListResponse(BaseModel):
    items: list[DocumentListItemResponse]
    total: int
    page: int
    size: int
