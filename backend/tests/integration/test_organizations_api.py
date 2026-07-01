import uuid
from datetime import UTC
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from app.modules.auth.models import User
from app.modules.organizations.models import Organization


@pytest.fixture
def mock_user():
    return User(
        id=uuid.uuid4(),
        email="test_org_creator@example.com",
        full_name="Org Creator",
        is_active=True
    )

@pytest.fixture
def mock_org_service():
    service = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_create_organization_api(async_client: AsyncClient, mock_user, mock_org_service):
    user = mock_user

    from datetime import datetime

    from app.core.security import get_current_user
    from app.main import app
    from app.modules.organizations.router import get_organization_service
    mock_org = Organization(
        id=uuid.uuid4(),
        name="Acme Corp",
        slug="acme",
        plan="free",
        status="active",
        created_by=user.id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    mock_org_service.create_organization.return_value = mock_org

    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_organization_service] = lambda: mock_org_service

    payload = {
        "name": "Acme Corp",
        "slug": "acme"
    }

    response = await async_client.post(
        "/api/v1/organizations",
        json=payload,
        headers={"Idempotency-Key": "test-key-123"}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Acme Corp"
    assert data["data"]["slug"] == "acme"
    assert data["meta"]["idempotency_key"] == "test-key-123"

@pytest.mark.asyncio
async def test_create_organization_api_duplicate_slug(async_client: AsyncClient, mock_user, mock_org_service):
    user = mock_user

    from app.core.security import get_current_user
    from app.main import app
    from app.modules.organizations.router import get_organization_service

    mock_org_service.create_organization.side_effect = ValueError("Organization with slug 'acme2' already exists")

    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_organization_service] = lambda: mock_org_service

    payload = {
        "name": "Acme Corp",
        "slug": "acme2"
    }

    response = await async_client.post("/api/v1/organizations", json=payload)

    app.dependency_overrides.clear()

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"]["success"] is False
    assert data["detail"]["error"]["code"] == "ORGANIZATION_CREATION_FAILED"
