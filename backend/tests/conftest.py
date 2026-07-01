import os
from unittest.mock import AsyncMock

# Set dummy environment variables for tests before importing the app
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key"
os.environ["SUPABASE_JWT_SECRET"] = "test-secret"
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test"

from contextlib import asynccontextmanager

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
def mock_db_engine():
    """Mock the app lifespan to prevent real database connections during tests."""
    from app.main import app
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def dummy_lifespan(*args, **kwargs):
        yield

    app.router.lifespan_context = dummy_lifespan

    # Also override the JWKS provider globally for tests
    from app.core.auth_providers import FakeJWKSProvider
    from app.core.security import get_jwks_provider

    # We use 'test-secret' because it matches the environment variable SUPABASE_JWT_SECRET
    # set at the top of conftest.py
    app.dependency_overrides[get_jwks_provider] = lambda: FakeJWKSProvider(secret="test-secret")

    yield
    app.router.lifespan_context = original_lifespan
    app.dependency_overrides.pop(get_jwks_provider, None)


@pytest.fixture
def mock_db_session():
    """Fixture providing a mock AsyncSession."""
    session = AsyncMock(spec=AsyncSession)
    return session

@pytest.fixture
async def async_client():
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
