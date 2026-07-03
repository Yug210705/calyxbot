import hashlib
import uuid
import time
from app.integrations.pipeline import PipelineStage, PipelineContext
from app.modules.documents.repositories import ChunkRepository
from app.modules.documents.models import DocumentChunk
from app.modules.documents.chunker import RecursiveChunker
from app.modules.search.embeddings import EmbeddingInterface
from app.core.config import get_settings

class PipelineError(Exception):
    def __init__(self, code: str, message: str, retryable: bool, stage: str):
        self.code = code
        self.message = message
        self.retryable = retryable
        self.stage = stage
        super().__init__(f"[{stage}] {code}: {message}")

class ChunkerStage(PipelineStage):
    stage_name = "chunker"
    
    def __init__(self, chunker: RecursiveChunker, repo: ChunkRepository):
        self.chunker = chunker
        self.repo = repo
        self.settings = get_settings()

    async def process(self, context: PipelineContext) -> PipelineContext:
        if not context.normalized_content or not context.document_id:
            raise ValueError("ChunkerStage requires normalized_content and document_id in context.")

        text = context.normalized_content.get("content", "")
        raw_bytes_len = len(context.raw_content) if context.raw_content else 0
        
        # 1. Check before chunking limits
        if raw_bytes_len > self.settings.PIPELINE_MAX_DOCUMENT_BYTES:
            raise PipelineError(
                code="DOCUMENT_TOO_LARGE",
                message=f"Raw document exceeds max bytes: {raw_bytes_len} > {self.settings.PIPELINE_MAX_DOCUMENT_BYTES}",
                retryable=False,
                stage=self.stage_name
            )
            
        if len(text) > self.settings.PIPELINE_MAX_NORMALIZED_TEXT_CHARS:
            raise PipelineError(
                code="DOCUMENT_TOO_LARGE",
                message=f"Normalized text exceeds max chars: {len(text)} > {self.settings.PIPELINE_MAX_NORMALIZED_TEXT_CHARS}",
                retryable=False,
                stage=self.stage_name
            )

        doc_checksum = context.normalized_content.get("checksum", hashlib.sha256(text.encode("utf-8")).hexdigest())
        
        start_time = time.perf_counter()
        
        chunks = self.chunker.chunk_document(text, doc_checksum)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        if elapsed_ms > self.settings.PIPELINE_MAX_CHUNKING_TIME_MS:
            raise PipelineError(
                code="CHUNKING_TIMEOUT",
                message=f"Chunking took too long: {elapsed_ms:.0f}ms > {self.settings.PIPELINE_MAX_CHUNKING_TIME_MS}ms",
                retryable=False,
                stage=self.stage_name
            )
            
        if len(chunks) > self.settings.PIPELINE_MAX_CHUNKS_PER_DOCUMENT:
            raise PipelineError(
                code="CHUNK_LIMIT_EXCEEDED",
                message=f"Too many chunks: {len(chunks)} > {self.settings.PIPELINE_MAX_CHUNKS_PER_DOCUMENT}",
                retryable=False,
                stage=self.stage_name
            )
        
        doc_chunks = []
        for c in chunks:
            chunk_id = uuid.uuid5(context.document_id, f"{c.start_offset}_{c.checksum}")
            doc_chunks.append(DocumentChunk(
                id=chunk_id,
                document_id=context.document_id,
                index=c.index,
                text=c.text,
                token_count=c.token_count,
                start_offset=c.start_offset,
                end_offset=c.end_offset,
                checksum=c.checksum,
                language=c.language,
                page_number=c.page_number,
                section_heading=c.section_heading,
                chunker_version=c.chunker_version,
                source_document_version=context.document_metadata.get("version", 1),
                chunk_hash=f"{context.document_id}-{c.index}"
            ))
            
        await self.repo.create_many(doc_chunks)
        return context

class EmbedderStage(PipelineStage):
    stage_name = "embedder"
    
    def __init__(self, embedder: EmbeddingInterface, repo: ChunkRepository):
        self.embedder = embedder
        self.repo = repo

    async def process(self, context: PipelineContext) -> PipelineContext:
        if not context.document_id:
            raise ValueError("EmbedderStage requires document_id in context.")

        chunks = await self.repo.get_by_document_id(context.org_id, context.document_id)
        if not chunks:
            return context

        texts = [c.text for c in chunks]
        embeddings = await self.embedder.embed_documents(texts)
        
        for chunk, embedding in zip(chunks, embeddings, strict=True):
            chunk.embedding = embedding
            
        await self.repo.update_many(chunks)
        return context
