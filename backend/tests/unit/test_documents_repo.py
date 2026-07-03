import uuid
import pytest
from unittest.mock import AsyncMock

from app.modules.documents.models import Document, DocumentChunk
from app.modules.documents.repositories import DocumentRepository, ChunkRepository

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.mark.asyncio
async def test_document_repository_create(mock_session):
    repo = DocumentRepository(mock_session)
    doc = Document(
        organization_id=uuid.uuid4(),
        external_id="ext-123",
        title="Test Doc",
        mime_type="text/plain",
        checksum="abcd123"
    )
    
    result = await repo.create(doc)
    
    mock_session.add.assert_called_once_with(doc)
    mock_session.flush.assert_called_once()
    mock_session.refresh.assert_called_once_with(doc)
    assert result == doc

@pytest.mark.asyncio
async def test_chunk_repository_create_many(mock_session):
    repo = ChunkRepository(mock_session)
    chunks = [
        DocumentChunk(
            document_id=uuid.uuid4(),
            index=0,
            text="chunk 1",
            token_count=10,
            start_offset=0,
            end_offset=100,
            checksum="hash1",
            chunk_hash="chash1"
        )
    ]
    
    result = await repo.create_many(chunks)
    
    mock_session.add_all.assert_called_once_with(chunks)
    mock_session.flush.assert_called_once()
    assert result == chunks
