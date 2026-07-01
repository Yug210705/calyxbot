import uuid
from unittest.mock import AsyncMock

import pytest

from app.modules.members.models import Role
from app.modules.organizations.models import Organization
from app.modules.organizations.schemas import OrganizationCreate
from app.modules.organizations.services import (
    OrganizationCreatedEvent,
    OrganizationService,
)


@pytest.fixture
def mock_org_repo():
    return AsyncMock()

@pytest.fixture
def mock_membership_repo():
    return AsyncMock()

@pytest.fixture
def mock_role_repo():
    return AsyncMock()

@pytest.fixture
def mock_event_bus():
    return AsyncMock()

@pytest.fixture
def mock_db_session():
    return AsyncMock()

@pytest.fixture
def org_service(mock_db_session, mock_org_repo, mock_membership_repo, mock_role_repo, mock_event_bus):
    return OrganizationService(
        session=mock_db_session,
        org_repo=mock_org_repo,
        membership_repo=mock_membership_repo,
        role_repo=mock_role_repo,
        event_bus=mock_event_bus
    )

@pytest.mark.asyncio
async def test_create_organization_success(
    org_service, mock_org_repo, mock_membership_repo, mock_role_repo, mock_event_bus
):
    user_id = uuid.uuid4()
    data = OrganizationCreate(name="Test Org", slug="test-org")

    mock_org_repo.get_by_slug.return_value = None

    mock_org = Organization(id=uuid.uuid4(), name="Test Org", slug="test-org", created_by=user_id)
    mock_org_repo.create.return_value = mock_org

    mock_owner_role = Role(id=uuid.uuid4(), name="owner")
    mock_role_repo.get_by_name.return_value = mock_owner_role

    result = await org_service.create_organization(user_id, data)

    assert result.id == mock_org.id
    assert result.slug == "test-org"

    mock_org_repo.create.assert_called_once()
    mock_membership_repo.create.assert_called_once()
    mock_event_bus.publish.assert_called_once()

    # Check that event was fired with correct payload
    event_arg = mock_event_bus.publish.call_args[0][0]
    assert isinstance(event_arg, OrganizationCreatedEvent)
    assert event_arg.payload["slug"] == "test-org"

@pytest.mark.asyncio
async def test_create_organization_duplicate_slug(
    org_service, mock_org_repo, mock_membership_repo, mock_role_repo, mock_event_bus
):
    user_id = uuid.uuid4()
    data = OrganizationCreate(name="Test Org", slug="test-org")

    mock_org_repo.get_by_slug.return_value = Organization()

    with pytest.raises(ValueError, match="already exists"):
        await org_service.create_organization(user_id, data)
