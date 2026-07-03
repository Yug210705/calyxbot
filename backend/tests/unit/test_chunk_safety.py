import pytest
import uuid
from unittest.mock import MagicMock
from app.integrations.pipeline import PipelineContext
from app.integrations.pipeline_stages import ChunkerStage, PipelineError
from app.core.config import Settings

@pytest.fixture
def mock_chunker():
    return MagicMock()

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.mark.asyncio
async def test_document_too_large_raises_pipeline_error(mock_chunker, mock_repo):
    stage = ChunkerStage(mock_chunker, mock_repo)
    # mock settings
    stage.settings = Settings(
        DATABASE_URL="", SUPABASE_URL="", SUPABASE_SERVICE_ROLE_KEY="", SUPABASE_JWT_SECRET="",
        PIPELINE_MAX_DOCUMENT_BYTES=10,
        PIPELINE_MAX_NORMALIZED_TEXT_CHARS=100
    )
    
    ctx = PipelineContext(
        org_id=uuid.uuid4(),
        job_id=uuid.uuid4(),
        connector_id=uuid.uuid4(),
        document_metadata={"version": 1},
        document_id=uuid.uuid4(),
        normalized_content={"content": "tiny text"},
        raw_content=b"A" * 20 # exceeds 10 bytes limit
    )
    
    with pytest.raises(PipelineError) as exc:
        await stage.process(ctx)
        
    assert exc.value.code == "DOCUMENT_TOO_LARGE"
    assert exc.value.retryable is False

@pytest.mark.asyncio
async def test_normalized_text_too_large_raises_pipeline_error(mock_chunker, mock_repo):
    stage = ChunkerStage(mock_chunker, mock_repo)
    stage.settings = Settings(
        DATABASE_URL="", SUPABASE_URL="", SUPABASE_SERVICE_ROLE_KEY="", SUPABASE_JWT_SECRET="",
        PIPELINE_MAX_DOCUMENT_BYTES=1000,
        PIPELINE_MAX_NORMALIZED_TEXT_CHARS=10
    )
    
    ctx = PipelineContext(
        org_id=uuid.uuid4(),
        job_id=uuid.uuid4(),
        connector_id=uuid.uuid4(),
        document_metadata={"version": 1},
        document_id=uuid.uuid4(),
        normalized_content={"content": "A" * 20}, # exceeds 10 char limit
        raw_content=b"tiny"
    )
    
    with pytest.raises(PipelineError) as exc:
        await stage.process(ctx)
        
    assert exc.value.code == "DOCUMENT_TOO_LARGE"

@pytest.mark.asyncio
async def test_chunk_limit_exceeded_returns_structured_error(mock_chunker, mock_repo):
    mock_chunker.chunk_document.return_value = [MagicMock()] * 5
    
    stage = ChunkerStage(mock_chunker, mock_repo)
    stage.settings = Settings(
        DATABASE_URL="", SUPABASE_URL="", SUPABASE_SERVICE_ROLE_KEY="", SUPABASE_JWT_SECRET="",
        PIPELINE_MAX_CHUNKING_TIME_MS=5000,
        PIPELINE_MAX_CHUNKS_PER_DOCUMENT=2 # 5 exceeds limit of 2
    )
    
    ctx = PipelineContext(
        org_id=uuid.uuid4(),
        job_id=uuid.uuid4(),
        connector_id=uuid.uuid4(),
        document_metadata={"version": 1},
        document_id=uuid.uuid4(),
        normalized_content={"content": "valid length"},
        raw_content=b"valid length"
    )
    
    with pytest.raises(PipelineError) as exc:
        await stage.process(ctx)
        
    assert exc.value.code == "CHUNK_LIMIT_EXCEEDED"
    assert exc.value.retryable is False

@pytest.mark.asyncio
async def test_chunking_timeout_returns_structured_error(mock_chunker, mock_repo):
    def slow_chunker(*args, **kwargs):
        import time
        time.sleep(0.02)
        return []
        
    mock_chunker.chunk_document.side_effect = slow_chunker
    
    stage = ChunkerStage(mock_chunker, mock_repo)
    stage.settings = Settings(
        DATABASE_URL="", SUPABASE_URL="", SUPABASE_SERVICE_ROLE_KEY="", SUPABASE_JWT_SECRET="",
        PIPELINE_MAX_CHUNKING_TIME_MS=10, # timeout is 10ms, sleep is 20ms
        PIPELINE_MAX_CHUNKS_PER_DOCUMENT=100
    )
    
    ctx = PipelineContext(
        org_id=uuid.uuid4(),
        job_id=uuid.uuid4(),
        connector_id=uuid.uuid4(),
        document_metadata={"version": 1},
        document_id=uuid.uuid4(),
        normalized_content={"content": "valid length"},
        raw_content=b"valid length"
    )
    
    with pytest.raises(PipelineError) as exc:
        await stage.process(ctx)
        
    assert exc.value.code == "CHUNKING_TIMEOUT"
    assert exc.value.retryable is False
