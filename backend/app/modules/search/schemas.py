from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., description="The semantic search query string")
    top_k: int = Field(5, description="Number of top results to return", ge=1, le=50)
    provider: str | None = Field(None, description="Optional provider filter (e.g. google_drive)")
    status: str | None = Field(None, description="Optional document status filter (e.g. READY)")

class SearchResultResponse(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    snippet: str
    score: float
    provider: str
    source: str
    section_heading: str | None = None
    page_number: int | None = None
    document_status: str

class SearchResponse(BaseModel):
    query: str
    total: int
    latency_ms: int
    results: list[SearchResultResponse]
