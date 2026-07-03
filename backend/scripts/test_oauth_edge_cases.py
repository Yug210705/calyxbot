import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import httpx
import pytest

from app.core.models import Base
from app.integrations.services import IntegrationService, OAuthCredentialService
from app.integrations.credentials import CredentialEncryptionService
from app.integrations.oauth_state import create_oauth_state
from app.integrations.models import Connector, OAuthCredential
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)

# Mock httpx
class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code
        
    def json(self):
        return self._json_data
        
    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("Error", request=None, response=self)

class MockGoogleOAuthFlowManager:
    def generate_authorization_url(self, state: str) -> str:
        return "mock_url"
        
    async def exchange_code_for_tokens(self, code: str):
        if code == "invalid_code":
            raise ValueError("Invalid code")
        return {
            "access_token": "mock_access",
            "refresh_token": "mock_refresh",
            "expires_at": 9999999999
        }

async def run_tests():
    # Setup in-memory DB
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    org_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    from app.integrations.credentials import EnvironmentKeyProvider
    key_provider = EnvironmentKeyProvider()
    encryption_service = CredentialEncryptionService(key_provider)
    
    # Run tests
    async with async_session() as session:
        cred_service = OAuthCredentialService(session, encryption_service)
        service = IntegrationService(session, cred_service)
        
        # Inject mocks
        service.google_oauth = MockGoogleOAuthFlowManager()
        
        # Create a mock for httpx.AsyncClient
        original_client = httpx.AsyncClient
        
        # Test A: Fresh connect
        print("Running Test A: Fresh connect...")
        state = create_oauth_state(org_id, user_id, "google_drive")
        
        class MockClientA:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            async def get(self, url, headers): return MockResponse({"email": "test@example.com"})
            
        httpx.AsyncClient = MockClientA
        
        connector_a = await service.complete_google_connect(org_id, "valid_code", state)
        await session.commit()
        
        assert connector_a.provider_account_id == "test@example.com"
        assert connector_a.status.value == "ACTIVE"
        print("✅ Test A passed")
        
        # Test B: Reconnect same account
        print("Running Test B: Reconnect same account...")
        state_b = create_oauth_state(org_id, user_id, "google_drive")
        
        connector_b = await service.complete_google_connect(org_id, "valid_code", state_b)
        await session.commit()
        
        # Ensure it's the exact same connector
        assert connector_b.id == connector_a.id
        # Ensure no duplicate connectors
        connectors = await service.list_integrations(org_id)
        assert len(connectors) == 1
        print("✅ Test B passed")
        
        # Test C: Reconnect different account
        print("Running Test C: Reconnect different account...")
        state_c = create_oauth_state(org_id, user_id, "google_drive")
        
        class MockClientC:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            async def get(self, url, headers): return MockResponse({"email": "different@example.com"})
            
        httpx.AsyncClient = MockClientC
        
        try:
            await service.complete_google_connect(org_id, "valid_code", state_c)
            assert False, "Should have raised ValueError for mismatched account"
        except ValueError as e:
            assert "Another Google Drive account is already connected" in str(e)
            print("✅ Test C passed (Error raised correctly)")
            await session.rollback()
            
        # Test D: Invalid code / cancel
        print("Running Test D: Invalid code...")
        state_d = create_oauth_state(org_id, user_id, "google_drive")
        
        try:
            await service.complete_google_connect(org_id, "invalid_code", state_d)
            assert False, "Should have raised exception"
        except ValueError as e:
            print("✅ Test D passed (Error raised correctly)")
            await session.rollback()
            
        # Final Verification
        connectors = await service.list_integrations(org_id)
        assert len(connectors) == 1
        print("✅ All edge case assertions passed.")

if __name__ == "__main__":
    asyncio.run(run_tests())
