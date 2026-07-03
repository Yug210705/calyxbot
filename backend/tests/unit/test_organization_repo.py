import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.modules.organizations.models import Organization
from app.modules.organizations.repositories import SQLAlchemyOrganizationRepository


@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def repo(mock_session):
    return SQLAlchemyOrganizationRepository(session=mock_session)

@pytest.mark.asyncio
async def test_create_organization_success(repo, mock_session):
    org = Organization(id=uuid.uuid4(), name="Test", slug="test", created_by=uuid.uuid4())
    
    result = await repo.create(org)
    
    mock_session.add.assert_called_once_with(org)
    mock_session.flush.assert_called_once()
    mock_session.refresh.assert_called_once_with(org)
    assert result == org

@pytest.mark.asyncio
async def test_create_organization_integrity_error(repo, mock_session):
    org = Organization(id=uuid.uuid4(), name="Test", slug="test", created_by=uuid.uuid4())
    
    mock_session.flush.side_effect = IntegrityError("test", "test", "test")
    
    with pytest.raises(IntegrityError):
        await repo.create(org)
        
    mock_session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_get_by_id_found(repo, mock_session):
    org = Organization(id=uuid.uuid4(), name="Test", slug="test")
    
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = org
    mock_session.execute.return_value = mock_result
    
    result = await repo.get_by_id(org.id)
    assert result == org

@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_session.execute.return_value = mock_result
    
    result = await repo.get_by_id(uuid.uuid4())
    assert result is None

@pytest.mark.asyncio
async def test_get_by_slug_found(repo, mock_session):
    org = Organization(id=uuid.uuid4(), name="Test", slug="test")
    
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = org
    mock_session.execute.return_value = mock_result
    
    result = await repo.get_by_slug("test")
    assert result == org

@pytest.mark.asyncio
async def test_delete_success(repo, mock_session):
    org = Organization(id=uuid.uuid4(), name="Test", slug="test")
    
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = org
    mock_session.execute.return_value = mock_result
    
    result = await repo.delete(org.id)
    
    assert result is True
    assert org.deleted_at is not None
    mock_session.flush.assert_called_once()

@pytest.mark.asyncio
async def test_delete_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_session.execute.return_value = mock_result
    
    result = await repo.delete(uuid.uuid4())
    
    assert result is False

@pytest.mark.asyncio
async def test_restore_success(repo, mock_session):
    org = Organization(id=uuid.uuid4(), name="Test", slug="test", deleted_at=datetime.now(UTC))
    
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = org
    mock_session.execute.return_value = mock_result
    
    result = await repo.restore(org.id)
    
    assert result is True
    assert org.deleted_at is None
    mock_session.flush.assert_called_once()

@pytest.mark.asyncio
async def test_restore_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_session.execute.return_value = mock_result
    
    result = await repo.restore(uuid.uuid4())
    
    assert result is False
