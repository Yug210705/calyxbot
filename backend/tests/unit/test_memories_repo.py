import uuid
import pytest
from unittest.mock import AsyncMock

from app.modules.memories.models import KnowledgeObject, KnowledgeType
from app.modules.memories.repositories import KnowledgeRepository

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.mark.asyncio
async def test_knowledge_repository_create(mock_session):
    repo = KnowledgeRepository(mock_session)
    obj = KnowledgeObject(
        organization_id=uuid.uuid4(),
        type=KnowledgeType.PERSON,
        canonical_name="John Doe",
        canonical_key="john-doe",
        properties={"email": "john@example.com"},
        confidence=0.99
    )
    
    result = await repo.create_object(obj)
    
    mock_session.add.assert_called_once_with(obj)
    mock_session.flush.assert_called_once()
    mock_session.refresh.assert_called_once_with(obj)
    assert result == obj
