from pydantic import BaseModel, Field
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str = Field(..., description="The semantic search query string")
    top_k: int = Field(5, description="Number of top results to return", ge=1, le=50)
    provider: Optional[str] = Field(None, description="Optional provider filter (e.g. google_drive)")
    status: Optional[str] = Field(None, description="Optional document status filter (e.g. READY)")

class SearchResultResponse(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    snippet: str
    score: float
    provider: str
    source: str
    section_heading: Optional[str] = None
    page_number: Optional[int] = None
    document_status: str

class SearchResponse(BaseModel):
    query: str
    total: int
    latency_ms: int
    results: List[SearchResultResponse]
