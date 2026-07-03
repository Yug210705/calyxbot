import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base, TimestampMixin

class KnowledgeType(str, Enum):
    PERSON = "PERSON"
    COMPANY = "COMPANY"
    PROJECT = "PROJECT"
    TASK = "TASK"
    MEETING = "MEETING"
    POLICY = "POLICY"
    DOCUMENT = "DOCUMENT"
    TEAM = "TEAM"
    CUSTOM = "CUSTOM"

class RelationType(str, Enum):
    WORKS_ON = "WORKS_ON"
    REPORTS_TO = "REPORTS_TO"
    BELONGS_TO = "BELONGS_TO"
    MENTIONS = "MENTIONS"
    USES = "USES"
    OWNS = "OWNS"
    PART_OF = "PART_OF"
    RELATED_TO = "RELATED_TO"

class KnowledgeObject(Base, TimestampMixin):
    __tablename__ = "knowledge_objects"
    __table_args__ = (
        UniqueConstraint("organization_id", "canonical_key"),
        Index('ix_ko_org_canonical_key', 'organization_id', 'canonical_key'),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    type: Mapped[KnowledgeType] = mapped_column(SAEnum(KnowledgeType), nullable=False)
    canonical_name: Mapped[str] = mapped_column(String, nullable=False)
    canonical_key: Mapped[str] = mapped_column(String, index=True, nullable=False)
    properties: Mapped[dict] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    primary_source_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class KnowledgeRelation(Base, TimestampMixin):
    __tablename__ = "knowledge_relations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_node_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_objects.id"), nullable=False)
    to_node_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_objects.id"), nullable=False)
    relation_type: Mapped[RelationType] = mapped_column(SAEnum(RelationType), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    evidence_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    created_by_pipeline_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_from_document: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    created_from_chunk: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("document_chunks.id"), nullable=True)
    meta_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
