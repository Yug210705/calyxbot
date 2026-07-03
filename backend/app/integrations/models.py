import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, DateTime, Enum as SAEnum, ForeignKey, Integer, LargeBinary, String, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base, TimestampMixin

class ConnectorState(str, Enum):
    ACTIVE = "ACTIVE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DISCONNECTED = "DISCONNECTED"
    AUTH_REQUIRED = "AUTH_REQUIRED"

class TriggerType(str, Enum):
    MANUAL = "MANUAL"
    WEBHOOK = "WEBHOOK"
    SCHEDULE = "SCHEDULE"
    RETRY = "RETRY"

class SyncJobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"

class Connector(Base, TimestampMixin):
    __tablename__ = "connectors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ConnectorState] = mapped_column(SAEnum(ConnectorState), nullable=False, default=ConnectorState.ACTIVE)
    health: Mapped[str] = mapped_column(String, nullable=False, default="healthy")
    
    provider_account_id: Mapped[str | None] = mapped_column(String, nullable=True)
    
    connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    document_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sync_state: Mapped[str | None] = mapped_column(String, nullable=True)
    
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class OAuthCredential(Base, TimestampMixin):
    __tablename__ = "oauth_credentials"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    connector_provider: Mapped[str] = mapped_column(String, nullable=False)
    
    credential_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    key_id: Mapped[str] = mapped_column(String, nullable=False) 
    encryption_algorithm: Mapped[str] = mapped_column(String, default="AES-GCM", nullable=False)
    encrypted_blob: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    
    provider_account_id: Mapped[str | None] = mapped_column(String, nullable=True)
    provider_user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class SyncJob(Base, TimestampMixin):
    __tablename__ = "sync_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    connector_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False) # Refers to a ConnectorInstance if created, or string
    
    started_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    trigger_type: Mapped[TriggerType] = mapped_column(SAEnum(TriggerType), nullable=False)
    status: Mapped[SyncJobStatus] = mapped_column(SAEnum(SyncJobStatus), nullable=False, default=SyncJobStatus.PENDING)
    
    documents_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    documents_changed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    documents_unchanged: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    documents_deleted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    documents_skipped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    documents_failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bytes_processed: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    duration_ms: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    failure_reason_code: Mapped[str | None] = mapped_column(String, nullable=True)
    
    provider_cursor_before: Mapped[str | None] = mapped_column(String, nullable=True)
    provider_cursor_after: Mapped[str | None] = mapped_column(String, nullable=True)
    parent_job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("sync_jobs.id"), nullable=True)
    cancel_requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class SyncJobDocumentOutcome(str, Enum):
    DISCOVERED = "DISCOVERED"
    UNCHANGED = "UNCHANGED"
    UPDATED = "UPDATED"
    CREATED = "CREATED"
    DELETED = "DELETED"
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"

class SyncJobDocumentLog(Base, TimestampMixin):
    __tablename__ = "sync_job_document_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sync_job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sync_jobs.id"), nullable=False, index=True)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("connectors.id"), nullable=False)
    
    document_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    external_document_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    document_title: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    
    outcome: Mapped[SyncJobDocumentOutcome] = mapped_column(SAEnum(SyncJobDocumentOutcome), nullable=False)
    failure_reason_code: Mapped[str | None] = mapped_column(String, nullable=True)
    failure_message: Mapped[str | None] = mapped_column(String, nullable=True)
    
    bytes_processed: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    document_version_before: Mapped[int | None] = mapped_column(Integer, nullable=True)
    document_version_after: Mapped[int | None] = mapped_column(Integer, nullable=True)
    checksum_before: Mapped[str | None] = mapped_column(String, nullable=True)
    checksum_after: Mapped[str | None] = mapped_column(String, nullable=True)
    
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    metadata_json: Mapped[str | None] = mapped_column(String, nullable=True)
