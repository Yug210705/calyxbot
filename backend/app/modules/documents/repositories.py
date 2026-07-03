import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.documents.models import Document, DocumentChunk

class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, document: Document) -> Document:
        self.session.add(document)
        await self.session.flush()
        await self.session.refresh(document)
        return document

    async def get_by_id(self, org_id: uuid.UUID, document_id: uuid.UUID) -> Optional[Document]:
        stmt = select(Document).where(Document.id == document_id, Document.organization_id == org_id, Document.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_by_external_id(self, org_id: uuid.UUID, connector_id: uuid.UUID, external_id: str) -> Optional[Document]:
        stmt = select(Document).where(
            Document.organization_id == org_id, 
            Document.connector_id == connector_id,
            Document.external_id == external_id,
            Document.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_connector(self, org_id: uuid.UUID, connector_id: uuid.UUID) -> List[Document]:
        stmt = select(Document).where(
            Document.organization_id == org_id,
            Document.connector_id == connector_id,
            Document.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_documents(
        self, 
        org_id: uuid.UUID, 
        q: Optional[str] = None, 
        provider: Optional[str] = None, 
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ):
        from sqlalchemy import func, or_
        from app.integrations.models import Connector
        
        stmt = select(Document, Connector.provider).outerjoin(
            Connector, Document.connector_id == Connector.id
        ).where(
            Document.organization_id == org_id,
            Document.deleted_at.is_(None)
        )
        
        if status and status != "all":
            stmt = stmt.where(Document.status == status.upper())
            
        if provider and provider != "all":
            stmt = stmt.where(Connector.provider == provider)
            
        if q:
            stmt = stmt.where(Document.title.ilike(f"%{q}%"))
            
        stmt = stmt.order_by(Document.created_at.desc()).limit(limit).offset(offset)
        
        # We also want the total count
        count_stmt = select(func.count(Document.id)).outerjoin(
            Connector, Document.connector_id == Connector.id
        ).where(
            Document.organization_id == org_id,
            Document.deleted_at.is_(None)
        )
        if status and status != "all":
            count_stmt = count_stmt.where(Document.status == status.upper())
        if provider and provider != "all":
            count_stmt = count_stmt.where(Connector.provider == provider)
        if q:
            count_stmt = count_stmt.where(Document.title.ilike(f"%{q}%"))
            
        result = await self.session.execute(stmt)
        count_result = await self.session.execute(count_stmt)
        
        rows = result.all()
        total = count_result.scalar() or 0
        
        return rows, total

    async def get_document_detail(self, org_id: uuid.UUID, document_id: uuid.UUID):
        from sqlalchemy import func
        from app.integrations.models import Connector
        from app.modules.documents.models import DocumentChunk
        
        stmt = select(Document, Connector.provider).outerjoin(
            Connector, Document.connector_id == Connector.id
        ).where(
            Document.id == document_id,
            Document.organization_id == org_id,
            Document.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        row = result.first()
        if not row:
            return None
            
        doc, provider = row
        
        # Get chunk count
        chunk_count_stmt = select(func.count(DocumentChunk.id)).where(
            DocumentChunk.document_id == document_id,
            DocumentChunk.deleted_at.is_(None)
        )
        chunk_count_result = await self.session.execute(chunk_count_stmt)
        chunk_count = chunk_count_result.scalar() or 0
        
        return doc, provider, chunk_count

class ChunkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        self.session.add_all(chunks)
        await self.session.flush()
        return chunks

    async def get_by_document_id(self, org_id: uuid.UUID, document_id: uuid.UUID) -> List[DocumentChunk]:
        stmt = select(DocumentChunk).join(Document).where(
            DocumentChunk.document_id == document_id,
            Document.organization_id == org_id,
            DocumentChunk.deleted_at.is_(None)
        ).order_by(DocumentChunk.index)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
