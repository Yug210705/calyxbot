import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.main import app
from app.modules.auth.models import User
from app.modules.members.invitation_router import get_invitation_service
from app.modules.members.invitation_service import (
    InvitationAlreadyAcceptedError,
    InvitationError,
    InvitationExpiredError,
    InvitationRevokedError,
)

@pytest.fixture
def mock_user():
    return User(id=uuid.uuid4(), email="test@test.com", is_active=True)

def test_dependencies():
    mock_db = AsyncMock(spec=AsyncSession)
    assert get_invitation_service(mock_db) is not None

@pytest.mark.asyncio
async def test_accept_invitation_already_accepted(mock_user):
    mock_inv = AsyncMock()
    mock_inv.accept_invitation.side_effect = InvitationAlreadyAcceptedError("accepted")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_invitation_service] = lambda: mock_inv
    
    client = TestClient(app)
    response = client.post("/api/v1/invitations/abc/accept")
    app.dependency_overrides.clear()
    
    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "INVITATION_ALREADY_ACCEPTED"

@pytest.mark.asyncio
async def test_accept_invitation_expired(mock_user):
    mock_inv = AsyncMock()
    mock_inv.accept_invitation.side_effect = InvitationExpiredError("expired")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_invitation_service] = lambda: mock_inv
    
    client = TestClient(app)
    response = client.post("/api/v1/invitations/abc/accept")
    app.dependency_overrides.clear()
    
    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "INVITATION_EXPIRED"

@pytest.mark.asyncio
async def test_accept_invitation_revoked(mock_user):
    mock_inv = AsyncMock()
    mock_inv.accept_invitation.side_effect = InvitationRevokedError("revoked")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_invitation_service] = lambda: mock_inv
    
    client = TestClient(app)
    response = client.post("/api/v1/invitations/abc/accept")
    app.dependency_overrides.clear()
    
    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "INVITATION_REVOKED"

@pytest.mark.asyncio
async def test_accept_invitation_invalid(mock_user):
    mock_inv = AsyncMock()
    mock_inv.accept_invitation.side_effect = InvitationError("invalid")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_invitation_service] = lambda: mock_inv
    
    client = TestClient(app)
    response = client.post("/api/v1/invitations/abc/accept")
    app.dependency_overrides.clear()
    
    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "INVITATION_INVALID"

@pytest.mark.asyncio
async def test_accept_invitation_internal_error(mock_user):
    mock_inv = AsyncMock()
    mock_inv.accept_invitation.side_effect = Exception("db error")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_invitation_service] = lambda: mock_inv
    
    client = TestClient(app)
    response = client.post("/api/v1/invitations/abc/accept")
    app.dependency_overrides.clear()
    
    assert response.status_code == 500
