import uuid
import pytest
from unittest.mock import AsyncMock

from app.integrations.pipeline import PipelineContext, FetcherStage, NormalizerStage, DocumentSaveStage
from app.integrations.connectors.google.connector import GoogleDriveConnector
from app.modules.documents.repositories import DocumentRepository
from app.modules.documents.services import DocumentVersioningService
from app.modules.documents.models import Document, DocumentStatus

from app.integrations.pipeline import PipelineExecutor
from app.integrations.pipeline_stages import ChunkerStage, EmbedderStage
from app.modules.documents.chunker import RecursiveChunker
from app.modules.search.embeddings import EmbeddingInterface
from app.modules.documents.repositories import ChunkRepository

@pytest.fixture
def mock_connector():
    return GoogleDriveConnector(credentials={"access_token": "123"})

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def mock_repo(mock_session):
    return DocumentRepository(mock_session)

@pytest.fixture
def mock_version_svc(mock_session):
    return DocumentVersioningService(mock_session)

@pytest.mark.asyncio
async def test_pipeline_stages(mock_connector, mock_repo, mock_version_svc):
    org_id = uuid.uuid4()
    job_id = uuid.uuid4()
    connector_id = uuid.uuid4()
    
    metadata = {
        "external_id": "gdrive-12345",
        "title": "Project Alpha Spec",
        "mime_type": "application/vnd.google-apps.document",
        "owner": "john.doe@example.com",
        "last_modified": "2023-10-27T10:00:00Z"
    }
    
    ctx = PipelineContext(
        org_id=org_id,
        job_id=job_id,
        connector_id=connector_id,
        document_metadata=metadata
    )
    
    # Fetcher
    fetcher = FetcherStage(mock_connector)
    ctx = await fetcher.process(ctx)
    assert ctx.raw_content == b"Raw content from Google Drive API"
    
    # Normalizer
    normalizer = NormalizerStage(mock_connector)
    ctx = await normalizer.process(ctx)
    assert ctx.normalized_content["title"] == "Project Alpha Spec"
    assert ctx.normalized_content["content"] == "Raw content from Google Drive API"
    
    # Saver
    mock_repo.get_by_external_id = AsyncMock(return_value=None)
    created_doc = Document(id=uuid.uuid4(), status=DocumentStatus.NORMALIZED)
    mock_repo.create = AsyncMock(return_value=created_doc)
    
    # Chunking & Embedding Mocks
    mock_chunk_repo = AsyncMock(spec=ChunkRepository)
    mock_chunk_repo.create_many = AsyncMock()
    mock_chunk_repo.update_many = AsyncMock()
    
    # Setup Executor
    executor = PipelineExecutor()
    executor.register(FetcherStage(mock_connector))
    executor.register(NormalizerStage(mock_connector))
    executor.register(DocumentSaveStage(mock_repo, mock_version_svc))
    
    ctx = await executor.execute(ctx)
    
    assert ctx.document_id == created_doc.id
    mock_repo.create.assert_called_once()
    
    assert "fetch_ms" in ctx.metrics
    assert "normalize_ms" in ctx.metrics
    assert "save_ms" in ctx.metrics
    assert "total_ms" in ctx.metrics
