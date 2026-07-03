import uuid
import time
from fastapi import APIRouter, Depends, HTTPException, Header

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.search.service import VectorSearchService
from app.modules.search.embeddings import OpenAIEmbeddings
from app.modules.search.schemas import SearchRequest, SearchResponse, SearchResultResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.post("", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    x_organization_id: uuid.UUID = Header(...),
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    Perform a semantic search across the organization's synced documents.
    """
    start_time = time.time()
    
    # Initialize services
    embedder = OpenAIEmbeddings()
    search_service = VectorSearchService(session, embedder)
    
    try:
        raw_results = await search_service.search_chunks(
            org_id=x_organization_id,
            query=request.query,
            limit=request.top_k,
            provider=request.provider,
            status=request.status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    results = []
    
    for r in raw_results:
        results.append(
            SearchResultResponse(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                document_title=r.get("document_title", "Unknown Document"),
                snippet=r["snippet"],
                score=r["score"],
                provider=r["provider"],
                source=r["source"],
                section_heading=r["section_heading"],
                page_number=r["page_number"],
                document_status=r["document_status"]
            )
        )
        
    end_time = time.time()
    latency_ms = int((end_time - start_time) * 1000)
        
    return SearchResponse(
        query=request.query,
        total=len(results),
        latency_ms=latency_ms,
        results=results
    )
