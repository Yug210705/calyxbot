import uuid
from unittest.mock import AsyncMock

import pytest

from app.modules.members.models import Membership
from app.modules.members.services import MembershipService


@pytest.fixture
def mock_membership_repo():
    return AsyncMock()

@pytest.fixture
def mock_role_repo():
    return AsyncMock()

@pytest.fixture
def membership_service(mock_membership_repo, mock_role_repo):
    return MembershipService(
        membership_repo=mock_membership_repo,
        role_repo=mock_role_repo
    )

@pytest.mark.asyncio
async def test_get_organization_members(membership_service, mock_membership_repo):
    org_id = uuid.uuid4()

    mock_members = [
        Membership(id=uuid.uuid4(), user_id=uuid.uuid4(), organization_id=org_id, status="ACTIVE"),
        Membership(id=uuid.uuid4(), user_id=uuid.uuid4(), organization_id=org_id, status="ACTIVE")
    ]

    mock_membership_repo.list_by_organization.return_value = mock_members

    result = await membership_service.get_organization_members(org_id, limit=10, offset=0)

    assert len(result) == 2
    assert result[0].organization_id == org_id
    mock_membership_repo.list_by_organization.assert_called_once_with(str(org_id), 10, 0)

@pytest.mark.asyncio
async def test_check_permission_granted(membership_service, mock_membership_repo):
    org_id = uuid.uuid4()
    user_id = uuid.uuid4()

    from app.modules.members.models import Permission, Role
    mock_role = Role(id=uuid.uuid4(), name="owner")
    mock_role.permissions = [Permission(id=uuid.uuid4(), permission="membership.read")]

    # Mock user is a member
    membership = Membership(
        id=uuid.uuid4(), user_id=user_id, organization_id=org_id, status="ACTIVE"
    )
    membership.role = mock_role

    mock_membership_repo.get_by_user_and_org.return_value = membership

    # Note: check_permission now verifies RBAC
    has_permission = await membership_service.check_permission(user_id, org_id, "membership.read")

    assert has_permission is True
    mock_membership_repo.get_by_user_and_org.assert_called_once_with(str(user_id), str(org_id))

@pytest.mark.asyncio
async def test_check_permission_denied(membership_service, mock_membership_repo):
    org_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # Mock user is NOT a member
    mock_membership_repo.get_by_user_and_org.return_value = None

    has_permission = await membership_service.check_permission(user_id, org_id, "membership.read")

    assert has_permission is False
    mock_membership_repo.get_by_user_and_org.assert_called_once_with(str(user_id), str(org_id))
