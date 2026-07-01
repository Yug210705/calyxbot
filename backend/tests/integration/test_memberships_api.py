import pytest
import uuid
from httpx import AsyncClient
from unittest.mock import AsyncMock

from app.modules.auth.models import User
from app.modules.members.models import Membership, Role

@pytest.fixture
def mock_user():
    return User(
        id=uuid.uuid4(),
        email="test_org_creator@example.com",
        full_name="Org Creator",
        is_active=True
    )

@pytest.fixture
def mock_membership_service():
    service = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_get_organization_members_api(async_client: AsyncClient, mock_user, mock_membership_service):
    user = mock_user
    org_id = uuid.uuid4()
    
    from app.main import app
    from app.core.security import get_current_user
    from app.modules.organizations.router import get_membership_service
    
    mock_role = Role(id=uuid.uuid4(), name="owner")
    mock_member_user = User(id=uuid.uuid4(), email="member@example.com", full_name="Member", is_active=True)
    from datetime import datetime, timezone
    mock_membership = Membership(
        id=uuid.uuid4(),
        user_id=mock_member_user.id,
        organization_id=org_id,
        status="ACTIVE",
        role_id=mock_role.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    # We assign user and role to the membership manually as if joinedload did it
    mock_membership.user = mock_member_user
    mock_membership.role = mock_role
    
    mock_membership_service.check_permission.return_value = True
    mock_membership_service.get_organization_members.return_value = [mock_membership]

    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_membership_service] = lambda: mock_membership_service
    
    response = await async_client.get(f"/api/v1/organizations/{org_id}/members")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["items"]) == 1
    
    member_data = data["data"]["items"][0]
    assert member_data["user_id"] == str(mock_member_user.id)
    assert member_data["user"]["email"] == "member@example.com"
    assert member_data["role"]["name"] == "owner"

@pytest.mark.asyncio
async def test_get_organization_members_api_forbidden(async_client: AsyncClient, mock_user, mock_membership_service):
    user = mock_user
    org_id = uuid.uuid4()
    
    from app.main import app
    from app.core.security import get_current_user
    from app.modules.organizations.router import get_membership_service
    
    mock_membership_service.check_permission.return_value = False

    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_membership_service] = lambda: mock_membership_service
    
    response = await async_client.get(f"/api/v1/organizations/{org_id}/members")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 403
    data = response.json()
    assert data["detail"]["success"] is False
    assert data["detail"]["error"]["code"] == "FORBIDDEN"
