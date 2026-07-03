import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.documents.models import DocumentChunk
from app.modules.search.embeddings import EmbeddingInterface
from app.modules.search.snippets import extract_snippet

class VectorSearchService:
    def __init__(self, session: AsyncSession, embedder: EmbeddingInterface):
        self.session = session
        self.embedder = embedder

    async def search_chunks(
        self, 
        org_id: uuid.UUID, 
        query: str, 
        limit: int = 5,
        threshold: float = None,
        provider: str | None = None,
        status: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Perform a semantic search across document chunks using pgvector.
        Returns a list of chunks ordered by similarity (cosine distance).
        """
        # Embed the search query
        query_vector = await self.embedder.embed_query(query)
        
        from app.modules.documents.models import Document
        
        stmt = (
            select(
                DocumentChunk, 
                DocumentChunk.embedding.cosine_distance(query_vector).label('distance'),
                Document
            )
            .join(Document, Document.id == DocumentChunk.document_id)
            .where(Document.organization_id == org_id)
            .where(Document.deleted_at.is_(None))
            .where(DocumentChunk.deleted_at.is_(None))
        )
        
        if provider and provider != "all":
            stmt = stmt.where(Document.source == provider)
            
        if status and status != "all":
            stmt = stmt.where(Document.status == status)
            
        stmt = stmt.order_by('distance')
        
        if threshold is not None:
            stmt = stmt.where(DocumentChunk.embedding.cosine_distance(query_vector) < threshold)
            
        stmt = stmt.limit(limit)
        
        result = await self.session.execute(stmt)
        
        output = []
        for row in result:
            chunk = row[0]
            distance = row[1]
            doc = row[2]
            
            # Extract query-aware snippet
            snippet = extract_snippet(chunk.text, query)
            
            output.append({
                "chunk_id": str(chunk.id),
                "document_id": str(chunk.document_id),
                "document_title": doc.title,
                "snippet": snippet,
                "score": 1.0 - distance, # Convert distance to similarity score
                "provider": doc.source,
                "source": doc.source or f"{str(doc.source).capitalize()} / {doc.title}",
                "section_heading": chunk.section_heading,
                "page_number": chunk.page_number,
                "document_status": doc.status
            })
            
        return output
