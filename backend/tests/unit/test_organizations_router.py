import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.main import app
from app.modules.auth.models import User
from app.modules.organizations.router import (
    get_invitation_service,
    get_membership_service,
    get_organization_service,
)


@pytest.fixture
def mock_user():
    return User(id=uuid.uuid4(), email="test@test.com", is_active=True)

def test_dependencies():
    mock_db = AsyncMock(spec=AsyncSession)
    assert get_organization_service(mock_db) is not None
    assert get_membership_service(mock_db) is not None
    assert get_invitation_service(mock_db) is not None

@pytest.mark.asyncio
async def test_create_organization_internal_error(mock_user):
    mock_service = AsyncMock()
    mock_service.create_organization.side_effect = Exception("DB error")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_organization_service] = lambda: mock_service
    
    client = TestClient(app)
    response = client.post("/api/v1/organizations", json={"name": "test", "slug": "test"})
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_create_invitation_forbidden(mock_user):
    mock_mem = AsyncMock()
    mock_mem.check_permission.return_value = False
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_membership_service] = lambda: mock_mem
    
    client = TestClient(app)
    response = client.post(f"/api/v1/organizations/{uuid.uuid4()}/invitations", json={"email": "a@b.com", "role": "admin"})
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_invitation_invalid_role(mock_user):
    mock_mem = AsyncMock()
    mock_mem.check_permission.return_value = True
    
    mock_inv = AsyncMock()
    mock_inv.create_invitation.side_effect = ValueError("invalid")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_membership_service] = lambda: mock_mem
    app.dependency_overrides[get_invitation_service] = lambda: mock_inv
    
    client = TestClient(app)
    response = client.post(f"/api/v1/organizations/{uuid.uuid4()}/invitations", json={"email": "a@b.com", "role": "admin"})
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_invitation_internal_error(mock_user):
    mock_mem = AsyncMock()
    mock_mem.check_permission.return_value = True
    
    mock_inv = AsyncMock()
    mock_inv.create_invitation.side_effect = Exception("error")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_membership_service] = lambda: mock_mem
    app.dependency_overrides[get_invitation_service] = lambda: mock_inv
    
    client = TestClient(app)
    response = client.post(f"/api/v1/organizations/{uuid.uuid4()}/invitations", json={"email": "a@b.com", "role": "admin"})
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_get_members_internal_error(mock_user):
    mock_mem = AsyncMock()
    mock_mem.check_permission.return_value = True
    mock_mem.get_organization_members.side_effect = Exception("error")
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_membership_service] = lambda: mock_mem
    
    client = TestClient(app)
    response = client.get(f"/api/v1/organizations/{uuid.uuid4()}/members")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 500
