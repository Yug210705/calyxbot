import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.members.models import Membership, Role
from app.modules.members.invitation_models import Invitation
from app.modules.members.repositories import (
    SQLAlchemyMembershipRepository,
    SQLAlchemyRoleRepository,
    SQLAlchemyInvitationRepository
)


@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def membership_repo(mock_session):
    return SQLAlchemyMembershipRepository(session=mock_session)

@pytest.fixture
def role_repo(mock_session):
    return SQLAlchemyRoleRepository(session=mock_session)

@pytest.fixture
def inv_repo(mock_session):
    return SQLAlchemyInvitationRepository(session=mock_session)

@pytest.mark.asyncio
async def test_membership_create(membership_repo, mock_session):
    mem = Membership(id=uuid.uuid4(), user_id=uuid.uuid4(), organization_id=uuid.uuid4(), role_id=uuid.uuid4())
    result = await membership_repo.create(mem)
    mock_session.add.assert_called_once_with(mem)
    mock_session.flush.assert_called_once()
    mock_session.refresh.assert_called_once_with(mem)
    assert result == mem

@pytest.mark.asyncio
async def test_membership_get_by_user_and_org_found(membership_repo, mock_session):
    mem = Membership(id=uuid.uuid4())
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mem
    mock_session.execute.return_value = mock_result
    assert await membership_repo.get_by_user_and_org(uuid.uuid4(), uuid.uuid4()) == mem

@pytest.mark.asyncio
async def test_membership_get_by_user_and_org_not_found(membership_repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_session.execute.return_value = mock_result
    assert await membership_repo.get_by_user_and_org(uuid.uuid4(), uuid.uuid4()) is None

@pytest.mark.asyncio
async def test_membership_list_by_organization(membership_repo, mock_session):
    mems = [Membership(id=uuid.uuid4())]
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = mems
    mock_session.execute.return_value = mock_result
    assert await membership_repo.list_by_organization(uuid.uuid4()) == mems

@pytest.mark.asyncio
async def test_role_get_by_name_found(role_repo, mock_session):
    r = Role(id=uuid.uuid4(), name="admin")
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = r
    mock_session.execute.return_value = mock_result
    assert await role_repo.get_by_name("admin") == r

@pytest.mark.asyncio
async def test_role_get_by_name_not_found(role_repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_session.execute.return_value = mock_result
    with pytest.raises(ValueError):
        await role_repo.get_by_name("invalid")

@pytest.mark.asyncio
async def test_inv_create(inv_repo, mock_session):
    inv = Invitation(id=uuid.uuid4(), organization_id=uuid.uuid4(), email="test@test.com", token_hash="abc")
    result = await inv_repo.create(inv)
    mock_session.add.assert_called_once_with(inv)
    assert result == inv

@pytest.mark.asyncio
async def test_inv_get_by_token_found(inv_repo, mock_session):
    inv = Invitation(id=uuid.uuid4(), email="test@test.com", token_hash="abc")
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = inv
    mock_session.execute.return_value = mock_result
    assert await inv_repo.get_by_token("abc") == inv

@pytest.mark.asyncio
async def test_inv_get_by_token_not_found(inv_repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_session.execute.return_value = mock_result
    assert await inv_repo.get_by_token("abc") is None
