import asyncio
import uuid
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from app.core.models import Base
import app.modules.organizations.models
import app.integrations.models
import app.modules.documents.models
from app.integrations.models import Connector, ConnectorState, SyncJob
from app.core.queue import task_queue
from app.core.database import AsyncSessionLocal
from app.main import app

# Patch JSONB for sqlite compilation
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, 'sqlite')
def compile_jsonb_sqlite(type_, compiler, **kw):
    return 'JSON'

async def setup_test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    global AsyncSessionLocal
    import app.core.database as db
    import app.integrations.worker as worker
    import app.integrations.services as services
    import app.integrations.router as router
    
    db.AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    worker.AsyncSessionLocal = db.AsyncSessionLocal
    
    # We must patch get_db in the fastapi app to use this engine
    from app.core.database import get_db
    
    async def override_get_db():
        async with db.AsyncSessionLocal() as session:
            yield session
            
    app.dependency_overrides[get_db] = override_get_db

    return engine, db.AsyncSessionLocal

async def run_happy_path_api(session_maker):
    org_id = uuid.uuid4()
    
    # Setup mock Connector
    async with session_maker() as session:
        from app.modules.organizations.models import Organization
        org = Organization(id=org_id, name='Test Org', slug='test-org-api-1', plan='free', status='active', created_by=uuid.uuid4())
        session.add(org)
        
        connector = Connector(
            organization_id=org_id,
            provider="google_drive",
            display_name="Google Drive API",
            status=ConnectorState.ACTIVE,
            health="healthy"
        )
        session.add(connector)
        
        from app.integrations.models import OAuthCredential
        cred = OAuthCredential(
            organization_id=org_id,
            connector_provider="google_drive",
            encrypted_blob=b"fake_access_token",
            key_id="fake_key_id",
            provider_user_id="00000000-0000-0000-0000-000000000001"
        )
        session.add(cred)
        await session.commit()
        connector_id = connector.id
        
    print("\n\n==== 1. HAPPY PATH API TEST ====")
    headers = {
        "X-Organization-Id": str(org_id),
        "X-User-Id": "00000000-0000-0000-0000-000000000001"
    }
    
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # PENDING STATE
        resp = await client.post(f"/api/v1/integrations/{connector_id}/sync", headers=headers)
        print(f"\nPOST /api/v1/integrations/{connector_id}/sync Response (PENDING):")
        print(resp.json())
        job_id = resp.json()["id"]
        
        # Test Duplicate Run Guard
        print(f"\nTriggering duplicate sync while PENDING:")
        dup_resp = await client.post(f"/api/v1/integrations/{connector_id}/sync", headers=headers)
        print(f"POST /api/v1/integrations/{connector_id}/sync Response (Duplicate):")
        print(f"Status: {dup_resp.status_code}")
        print(dup_resp.json())
        
        # We manually process the queue instead of background worker for precise timing in test
        task = await task_queue.queue.get()
        import app.integrations.worker as worker_mod
        worker = worker_mod.SyncWorker(session_maker)
        
        from unittest.mock import patch, AsyncMock
        
        class MockConnector:
            async def discover(self):
                yield {"id": "1", "name": "doc1"}
                yield {"id": "2", "name": "doc2"}
            async def download(self, metadata):
                return b"content"
            async def normalize(self, metadata, raw_content):
                from app.modules.documents.models import Document
                return Document(id=metadata["id"], title=metadata["name"], content=raw_content.decode(), source_url="mock://url")
        
        with patch('app.integrations.services.ConnectorFactory.get_connector_instance', new_callable=AsyncMock) as mock_get_connector:
            mock_get_connector.return_value = MockConnector()
            worker_task = asyncio.create_task(worker.handle_sync_job(task['payload']))
            await asyncio.sleep(0.5) # let worker set to RUNNING
            
            run_resp = await client.get(f"/api/v1/integrations/jobs/{job_id}", headers=headers)
            print(f"\nGET /api/v1/integrations/jobs/{job_id} Response (RUNNING):")
            print(run_resp.json())
            
            await worker_task
            
            # SUCCESS STATE
            succ_resp = await client.get(f"/api/v1/integrations/jobs/{job_id}", headers=headers)
            print(f"\nGET /api/v1/integrations/jobs/{job_id} Response (SUCCESS):")
            print(succ_resp.json())


async def run_failure_path_api(session_maker):
    org_id = uuid.uuid4()
    
    async with session_maker() as session:
        from app.modules.organizations.models import Organization
        org = Organization(id=org_id, name='Test Org 2', slug='test-org-api-2', plan='free', status='active', created_by=uuid.uuid4())
        session.add(org)
        
        connector = Connector(
            organization_id=org_id,
            provider="google_drive",
            display_name="Google Drive Fail API",
            status=ConnectorState.ACTIVE,
            health="healthy"
        )
        session.add(connector)
        
        from app.integrations.models import OAuthCredential
        cred = OAuthCredential(
            organization_id=org_id,
            connector_provider="google_drive",
            encrypted_blob=b"fake_access_token",
            key_id="fake_key_id",
            provider_user_id="00000000-0000-0000-0000-000000000001"
        )
        session.add(cred)
        await session.commit()
        connector_id = connector.id
        
    print("\n\n==== 2. FAILURE PATH API TEST ====")
    headers = {
        "X-Organization-Id": str(org_id),
        "X-User-Id": "00000000-0000-0000-0000-000000000001"
    }
    
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(f"/api/v1/integrations/{connector_id}/sync", headers=headers)
        job_id = resp.json()["id"]
        
        task = await task_queue.queue.get()
        import app.integrations.worker as worker_mod
        worker = worker_mod.SyncWorker(session_maker)
        
        from unittest.mock import patch, AsyncMock
        
        class MockFailConnector:
            async def discover(self):
                raise Exception("Simulated forced failure")
                yield {"id": "1"}
                
        with patch('app.integrations.services.ConnectorFactory.get_connector_instance', new_callable=AsyncMock) as mock_get_connector:
            mock_get_connector.return_value = MockFailConnector()
            await worker.handle_sync_job(task['payload'])
            
            fail_resp = await client.get(f"/api/v1/integrations/jobs/{job_id}", headers=headers)
            print(f"\nGET /api/v1/integrations/jobs/{job_id} Response (FAILED):")
            print(fail_resp.json())

async def main():
    engine, session_maker = await setup_test_db()
    await run_happy_path_api(session_maker)
    await run_failure_path_api(session_maker)

if __name__ == "__main__":
    asyncio.run(main())
