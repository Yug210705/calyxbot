from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from dataclasses import dataclass

class IntegrationProviderResponse(BaseModel):
    provider: str
    name: str
    supports_incremental_sync: bool
    supports_binary_files: bool
    supports_webhooks: bool

class IntegrationConnectionResponse(BaseModel):
    id: UUID
    provider: str
    display_name: str
    status: str
    health: str
    connected_at: datetime | None
    last_sync_at: datetime | None
    document_count: int
    sync_state: str | None

class SyncJobResponse(BaseModel):
    id: UUID
    integration_id: UUID
    provider: str
    status: str
    documents_found: int
    documents_changed: int
    documents_skipped: int
    documents_failed: int
    bytes_processed: int
    duration_ms: int
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

@dataclass
class SyncDocumentResult:
    documents_found: int = 0
    documents_changed: int = 0
    documents_unchanged: int = 0
    documents_deleted: int = 0
    documents_skipped: int = 0
    documents_failed: int = 0
    bytes_processed: int = 0


