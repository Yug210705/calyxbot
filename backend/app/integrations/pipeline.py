import uuid
import time
import abc
import hashlib
from typing import Any
from dataclasses import dataclass, field

from app.integrations.connectors.base import BaseConnector
from app.modules.documents.repositories import DocumentRepository
from app.modules.documents.models import Document, DocumentStatus
from app.modules.documents.services import DocumentVersioningService

class CancellationToken:
    def __init__(self):
        self._is_cancelled = False
        
    def cancel(self):
        self._is_cancelled = True
        
    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled

@dataclass(frozen=True)
class PipelineContext:
    org_id: uuid.UUID
    job_id: uuid.UUID
    connector_id: uuid.UUID
    document_metadata: dict[str, Any]
    cancel_token: CancellationToken = field(default_factory=CancellationToken)
    metrics: dict[str, float] = field(default_factory=dict)
    
    raw_content: bytes = None
    normalized_content: dict[str, Any] = None
    document_id: uuid.UUID = None
    
    def with_raw_content(self, raw_content: bytes) -> 'PipelineContext':
        return PipelineContext(
            org_id=self.org_id, job_id=self.job_id, connector_id=self.connector_id,
            document_metadata=self.document_metadata, cancel_token=self.cancel_token, metrics=self.metrics,
            raw_content=raw_content, normalized_content=self.normalized_content, document_id=self.document_id
        )

    def with_normalized_content(self, normalized_content: dict[str, Any]) -> 'PipelineContext':
        return PipelineContext(
            org_id=self.org_id, job_id=self.job_id, connector_id=self.connector_id,
            document_metadata=self.document_metadata, cancel_token=self.cancel_token, metrics=self.metrics,
            raw_content=self.raw_content, normalized_content=normalized_content, document_id=self.document_id
        )

    def with_document_id(self, document_id: uuid.UUID) -> 'PipelineContext':
        return PipelineContext(
            org_id=self.org_id, job_id=self.job_id, connector_id=self.connector_id,
            document_metadata=self.document_metadata, cancel_token=self.cancel_token, metrics=self.metrics,
            raw_content=self.raw_content, normalized_content=self.normalized_content, document_id=document_id
        )
        
    def record_metric(self, key: str, duration_ms: float) -> 'PipelineContext':
        new_metrics = self.metrics.copy()
        new_metrics[key] = duration_ms
        return PipelineContext(
            org_id=self.org_id, job_id=self.job_id, connector_id=self.connector_id,
            document_metadata=self.document_metadata, cancel_token=self.cancel_token, metrics=new_metrics,
            raw_content=self.raw_content, normalized_content=self.normalized_content, document_id=self.document_id
        )

class PipelineStage(abc.ABC):
    @abc.abstractproperty
    def stage_name(self) -> str:
        pass

    @abc.abstractmethod
    async def process(self, context: PipelineContext) -> PipelineContext:
        pass

class PipelineExecutor:
    def __init__(self):
        self._stages: list[PipelineStage] = []
        
    def register(self, stage: PipelineStage):
        self._stages.append(stage)
        
    async def execute(self, context: PipelineContext) -> PipelineContext:
        current_ctx = context
        start_total = time.perf_counter()
        
        for stage in self._stages:
            if current_ctx.cancel_token.is_cancelled:
                raise InterruptedError("Pipeline execution cancelled.")
                
            start_stage = time.perf_counter()
            current_ctx = await stage.process(current_ctx)
            end_stage = time.perf_counter()
            
            stage_ms = (end_stage - start_stage) * 1000
            current_ctx = current_ctx.record_metric(f"{stage.stage_name}_ms", stage_ms)
            
        end_total = time.perf_counter()
        total_ms = (end_total - start_total) * 1000
        current_ctx = current_ctx.record_metric("total_ms", total_ms)
        
        return current_ctx

class FetcherStage(PipelineStage):
    stage_name = "fetch"
    def __init__(self, connector: BaseConnector):
        self.connector = connector

    async def process(self, context: PipelineContext) -> PipelineContext:
        raw_content = await self.connector.download(context.document_metadata)
        return context.with_raw_content(raw_content)

class NormalizerStage(PipelineStage):
    stage_name = "normalize"
    def __init__(self, connector: BaseConnector):
        self.connector = connector

    async def process(self, context: PipelineContext) -> PipelineContext:
        normalized = await self.connector.normalize(context.document_metadata, context.raw_content)
        return context.with_normalized_content(normalized)

class DocumentSaveStage(PipelineStage):
    stage_name = "save"
    def __init__(self, repo: DocumentRepository, version_service: DocumentVersioningService):
        self.repo = repo
        self.version_service = version_service

    async def process(self, context: PipelineContext) -> PipelineContext:
        norm = context.normalized_content
        checksum = hashlib.sha256(norm["content"].encode('utf-8')).hexdigest()
        
        existing = await self.repo.get_by_external_id(
            context.org_id, 
            context.connector_id, 
            norm["external_id"]
        )
        
        if existing:
            if existing.checksum != checksum:
                doc = await self.version_service.create_new_version(context.org_id, existing, checksum)
            else:
                doc = existing
        else:
            doc = Document(
                organization_id=context.org_id,
                connector_id=context.connector_id,
                external_id=norm["external_id"],
                title=norm["title"],
                source=norm.get("source"),
                mime_type=norm["mime_type"],
                checksum=checksum,
                status=DocumentStatus.NORMALIZED
            )
            doc = await self.repo.create(doc)
            
        return context.with_document_id(doc.id)
