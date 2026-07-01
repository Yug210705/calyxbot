"""Tests for Authentication module."""

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import jwt
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.auth.models import User


def create_test_jwt(sub: str, email: str, name: str = None) -> str:
    """Helper to create a signed JWT matching Supabase format."""
    payload = {
        "sub": sub,
        "email": email,
        "user_metadata": {"name": name} if name else {},
        "aud": "authenticated",
        "exp": datetime.now(UTC) + timedelta(minutes=15)
    }
    return jwt.encode(payload, "test-secret", algorithm="HS256")


@pytest.fixture
def test_client():
    # Provide a clean TestClient
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def mock_db(mock_db_session):
    """Overrides get_db with mock_db_session."""
    from app.core.database import get_db
    app.dependency_overrides[get_db] = lambda: mock_db_session
    yield mock_db_session
    app.dependency_overrides.pop(get_db, None)


def test_complete_signup_creates_new_user(test_client, mock_db):
    user_id = str(uuid.uuid4())
    token = create_test_jwt(sub=user_id, email="newuser@example.com", name="New User")

    # Mock DB where user does not exist
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    response = test_client.post(
        "/api/v1/auth/complete-signup",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "New User"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["id"] == user_id
    assert data["data"]["user"]["email"] == "newuser@example.com"

    # Verify DB insertion
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


def test_complete_signup_existing_user(test_client, mock_db):
    user_id = str(uuid.uuid4())
    token = create_test_jwt(sub=user_id, email="existing@example.com")

    # Mock DB where user DOES exist
    existing_user = User(id=uuid.UUID(user_id), email="existing@example.com", full_name="Old Name", is_active=True)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_user
    mock_db.execute.return_value = mock_result

    response = test_client.post(
        "/api/v1/auth/complete-signup",
        headers={"Authorization": f"Bearer {token}"},
        json={}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Verify DB was NOT added to
    mock_db.add.assert_not_called()


def test_get_me_returns_current_user(test_client, mock_db):
    user_id = str(uuid.uuid4())
    token = create_test_jwt(sub=user_id, email="me@example.com")

    existing_user = User(id=uuid.UUID(user_id), email="me@example.com", full_name="Me", is_active=True)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_user
    mock_db.execute.return_value = mock_result

    response = test_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["user"]["email"] == "me@example.com"
    assert data["data"]["api_version"] == "v1.0"


def test_get_me_fails_unauthorized_if_user_deleted(test_client, mock_db):
    user_id = str(uuid.uuid4())
    token = create_test_jwt(sub=user_id, email="me@example.com")

    # User not in DB
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    response = test_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
