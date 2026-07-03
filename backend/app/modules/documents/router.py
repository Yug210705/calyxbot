import uuid
from fastapi import APIRouter, Depends, Query, HTTPException, Request
import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.modules.documents.schemas import DocumentListResponse, DocumentDetailResponse
from app.modules.documents.services import DocumentVersioningService

router = APIRouter(prefix="/documents", tags=["documents"])
logger = structlog.get_logger(__name__)

def get_document_service(session: AsyncSession = Depends(get_db)) -> DocumentVersioningService:
    return DocumentVersioningService(session)

@router.get("", response_model=DocumentListResponse)
async def list_documents(
    request: Request,
    q: str | None = Query(None),
    provider: str | None = Query(None),
    status: str | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: DocumentVersioningService = Depends(get_document_service)
):
    org_id_str = request.headers.get("X-Organization-Id", "00000000-0000-0000-0000-000000000001")
    try:
        org_id = uuid.UUID(org_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid organization ID")
        
    try:
        return await service.list_documents(
            org_id=org_id,
            q=q,
            provider=provider,
            status=status,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error("Failed to list documents", error=str(e))
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list documents")

@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document_detail(
    request: Request,
    document_id: uuid.UUID,
    service: DocumentVersioningService = Depends(get_document_service)
):
    org_id_str = request.headers.get("X-Organization-Id", "00000000-0000-0000-0000-000000000001")
    try:
        org_id = uuid.UUID(org_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid organization ID")
        
    try:
        doc = await service.get_document_detail(org_id, document_id)
        if not doc:
            raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Document not found")
        return doc
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get document detail", error=str(e), document_id=str(document_id))
        raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get document detail")
