import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from app.modules.auth.models import User
from app.modules.members.invitation_models import Invitation
from app.modules.members.models import Membership


@pytest.fixture
def mock_user():
    return User(
        id=uuid.uuid4(),
        email="owner@example.com",
        full_name="Owner",
        is_active=True
    )

@pytest.fixture
def mock_invitation_service():
    return AsyncMock()

@pytest.fixture
def mock_membership_service():
    return AsyncMock()

@pytest.mark.asyncio
async def test_create_invitation_api(
    async_client: AsyncClient,
    mock_user,
    mock_invitation_service,
    mock_membership_service
):
    org_id = uuid.uuid4()
    invitation_id = uuid.uuid4()
    role_id = uuid.uuid4()

    from app.core.security import get_current_user
    from app.main import app
    from app.modules.organizations.router import (
        get_invitation_service,
        get_membership_service,
    )

    mock_membership_service.check_permission.return_value = True

    expires_at = datetime.now(UTC) + timedelta(hours=72)
    mock_invitation = Invitation(
        id=invitation_id,
        email="invitee@example.com",
        organization_id=org_id,
        role_id=role_id,
        status="pending",
        invited_by=mock_user.id,
        token_hash="fakehash",
        expires_at=expires_at,
        created_at=datetime.now(UTC),
    )
    raw_token = "fakesecuretoken123"

    mock_invitation_service.create_invitation.return_value = (mock_invitation, raw_token)

    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_invitation_service] = lambda: mock_invitation_service
    app.dependency_overrides[get_membership_service] = lambda: mock_membership_service

    response = await async_client.post(
        f"/api/v1/organizations/{org_id}/invitations",
        json={"email": "invitee@example.com", "role": "employee"}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["invitation"]["email"] == "invitee@example.com"
    assert data["data"]["invite_url"] == f"/api/v1/invitations/{raw_token}/accept"

@pytest.mark.asyncio
async def test_accept_invitation_api(
    async_client: AsyncClient,
    mock_user,
    mock_invitation_service
):
    raw_token = "fakesecuretoken123"
    org_id = uuid.uuid4()

    from app.core.security import get_current_user
    from app.main import app
    from app.modules.members.invitation_router import get_invitation_service

    mock_membership = Membership(
        id=uuid.uuid4(),
        user_id=mock_user.id,
        organization_id=org_id,
        status="ACTIVE",
        role_id=uuid.uuid4(),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    mock_invitation_service.accept_invitation.return_value = mock_membership

    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_invitation_service] = lambda: mock_invitation_service

    response = await async_client.post(f"/api/v1/invitations/{raw_token}/accept")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["organization_id"] == str(org_id)
    assert data["data"]["user_id"] == str(mock_user.id)
