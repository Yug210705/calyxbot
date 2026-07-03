import uuid
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.integrations.worker import SyncWorker
from app.integrations.services import ConnectorFactory
from app.modules.search.service import VectorSearchService
from app.modules.search.embeddings import EmbeddingInterface
from app.modules.documents.models import Document, DocumentChunk, DocumentStatus

class MockEmbedder(EmbeddingInterface):
    @property
    def vector_size(self) -> int:
        return 1536
        
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Mock simple vectors based on text length for testing
        return [[float(len(t))] * 1536 for t in texts]
        
    async def embed_query(self, text: str) -> list[float]:
        return [float(len(text))] * 1536

@pytest.fixture
def mock_session():
    session = AsyncMock()
    
    # We need to mock the result of await session.execute(...)
    # It returns a result object that has scalar_one_or_none() and scalars().all()
    # This must be a synchronous MagicMock, not AsyncMock, because scalar_one_or_none is sync.
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_result.scalars.return_value.all.return_value = []
    
    session.execute.return_value = mock_result
    
    def mock_add(obj):
        if not getattr(obj, "id", None):
            import uuid
            obj.id = uuid.uuid4()
            
    session.add = MagicMock(side_effect=mock_add)
    session.add_all = MagicMock()
    
    ctx_mgr = AsyncMock()
    ctx_mgr.__aenter__.return_value = session
    return ctx_mgr

@pytest.mark.asyncio
async def test_end_to_end_retrieval_flow(mock_session):
    org_id = uuid.uuid4()
    connector_id = uuid.uuid4()
    
    # 1. Setup mock factory to return a Google Drive Connector
    mock_factory = AsyncMock(spec=ConnectorFactory)
    mock_connector = AsyncMock()
    mock_connector.discover.return_value = AsyncMock()
    
    # Mock an async generator for discover()
    async def mock_discover():
        yield {
            "external_id": "gdrive-999",
            "title": "Q3 Budget Roadmap",
            "mime_type": "text/plain",
            "owner": "test@example.com",
            "last_modified": "2023-10-01"
        }
    mock_connector.discover = mock_discover
    mock_connector.download = AsyncMock(return_value=b"We need to allocate $50,000 for the Q3 budget.")
    mock_connector.normalize = AsyncMock(return_value={
        "external_id": "gdrive-999",
        "title": "Q3 Budget Roadmap",
        "mime_type": "text/plain",
        "content": "We need to allocate $50,000 for the Q3 budget.",
        "source": "google_drive"
    })
    
    mock_factory.get_connector_instance.return_value = mock_connector
    
    # We patch OpenAIEmbeddings to use our MockEmbedder during worker execution
    with patch("app.integrations.worker.OpenAIEmbeddings", return_value=MockEmbedder()):
        # 2. Start SyncWorker
        worker = SyncWorker(session_maker=lambda: mock_session, connector_factory=mock_factory)
        
        # 3. Simulate SyncJobService enqueueing a job
        job_id = uuid.uuid4()
        payload = {
            "job_id": str(job_id),
            "org_id": str(org_id),
            "connector_id": str(connector_id)
        }
        
        mock_job = AsyncMock()
        mock_job.organization_id = org_id
        mock_job.provider = "google_drive"
        actual_session = mock_session.__aenter__.return_value
        actual_session.get.return_value = mock_job
        
        # 4. Manually trigger the worker handler (simulating queue processing)
        await worker.handle_sync_job(payload)
        
        # Verify the pipeline stages were called
        actual_session = mock_session.__aenter__.return_value
        
        mock_connector.download.assert_called_once()
        mock_connector.normalize.assert_called_once()
        actual_session.add.assert_called() # Document save
        actual_session.add_all.assert_called() # Chunk save
        actual_session.commit.assert_called()
        
    # 5. Search for "budget"
    embedder = MockEmbedder()
    
    # The session we pass to VectorSearchService should be the underlying session, not the ctx_mgr
    search_service = VectorSearchService(actual_session, embedder)
    
    # Mocking session.execute for search to return a mock chunk
    mock_chunk = DocumentChunk(
        id=uuid.uuid4(), 
        document_id=uuid.uuid4(), 
        text="We need to allocate $50,000 for the Q3 budget.",
        page_number=1,
        section_heading=None
    )
    
    mock_doc = Document(
        id=mock_chunk.document_id,
        title="Q3 Budget Roadmap",
        source="google_drive",
        status=DocumentStatus.READY
    )
    
    mock_search_result = MagicMock()
    # row format: (chunk, distance, document)
    mock_search_result.__iter__.return_value = [(mock_chunk, 0.12, mock_doc)]
    actual_session.execute.return_value = mock_search_result
    
    results = await search_service.search_chunks(org_id, "budget")
    
    assert len(results) == 1
    assert results[0]["document_title"] == "Q3 Budget Roadmap"
    assert "budget" in results[0]["snippet"].lower()
    assert results[0]["score"] == 0.88
