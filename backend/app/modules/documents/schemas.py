from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel

class ProcessingTimelineItem(BaseModel):
    key: str
    label: str
    status: str  # completed | current | pending | failed
    timestamp: Optional[datetime] = None

class DocumentListItemResponse(BaseModel):
    id: uuid.UUID
    title: str
    provider: str
    source: Optional[str] = None
    mime_type: str
    status: str
    version: int
    chunk_count: int
    updated_at: datetime
    last_synced_at: Optional[datetime] = None
    knowledge_object_count: Optional[int] = 0

class DocumentDetailResponse(DocumentListItemResponse):
    checksum: str
    created_at: datetime
    processing_timeline: List[ProcessingTimelineItem]
    graph_relation_count: Optional[int] = 0
    page_count: Optional[int] = None
    section_count: Optional[int] = None

class DocumentListResponse(BaseModel):
    items: List[DocumentListItemResponse]
    total: int
    page: int
    size: int
