import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BigInteger, Column, DateTime, Enum as SAEnum, ForeignKey, String, Integer, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base, TimestampMixin

class DocumentStatus(str, Enum):
    PENDING = "PENDING"
    FETCHED = "FETCHED"
    NORMALIZED = "NORMALIZED"
    CHUNKED = "CHUNKED"
    EMBEDDED = "EMBEDDED"
    GRAPH_BUILT = "GRAPH_BUILT"
    READY = "READY"
    FAILED = "FAILED"

class Document(Base, TimestampMixin):
    __tablename__ = "documents"
    __table_args__ = (
        Index('ix_doc_org_status', 'organization_id', 'status'),
        Index('ix_doc_org_external_id', 'organization_id', 'external_id'),
        Index('ix_doc_org_checksum', 'organization_id', 'checksum'),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    connector_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True) 
    
    external_id: Mapped[str] = mapped_column(String, index=True, nullable=False)   
    title: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)                    
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    checksum: Mapped[str] = mapped_column(String, nullable=False)
    
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sync_cursor: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    sync_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ingestion_source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    processing_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    status: Mapped[DocumentStatus] = mapped_column(SAEnum(DocumentStatus), default=DocumentStatus.PENDING, nullable=False)
    root_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    parent_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class DocumentChunk(Base, TimestampMixin):
    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False)
    
    start_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    end_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    section_heading: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    checksum: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, default="en", nullable=False)
    
    chunker_version: Mapped[str] = mapped_column(String, nullable=False)
    embedding_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    source_document_version: Mapped[int] = mapped_column(Integer, nullable=False)
    
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(1536), nullable=True)
    
    chunk_hash: Mapped[str] = mapped_column(String, index=True, nullable=False)
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
