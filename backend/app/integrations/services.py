import uuid
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.models import OAuthCredential, Connector, ConnectorState, SyncJob, SyncJobStatus, TriggerType
from app.integrations.repositories import ConnectorRepository
from app.integrations.credentials import CredentialEncryptionService
from app.integrations.oauth import GoogleOAuthFlowManager
from app.integrations.oauth_state import create_oauth_state, parse_oauth_state
import httpx
from datetime import datetime

class OAuthCredentialService:
    def __init__(self, session: AsyncSession, encryption_service: CredentialEncryptionService):
        self.repo = ConnectorRepository(session)
        self.encryption_service = encryption_service

    async def store_credentials(
        self, 
        org_id: uuid.UUID, 
        provider: str, 
        credentials: Dict[str, Any],
        provider_account_id: str = None
    ) -> OAuthCredential:
        encrypted_blob = self.encryption_service.encrypt_credentials(credentials)
        
        cred = OAuthCredential(
            organization_id=org_id,
            connector_provider=provider,
            key_id=f"kms-key-default", # In real env, map this to KMS key version
            encryption_algorithm="AES-GCM",
            encrypted_blob=encrypted_blob,
            provider_account_id=provider_account_id
        )
        return await self.repo.create_credential(cred)

    async def get_credentials(self, org_id: uuid.UUID, provider: str) -> Dict[str, Any]:
        cred = await self.repo.get_credential(org_id, provider)
        if not cred:
            raise ValueError(f"No credentials found for provider {provider} in organization {org_id}")
        
        # In a real enterprise system, check cred.key_id to determine which KMS key to use for decryption
        return self.encryption_service.decrypt_credentials(cred.encrypted_blob)

class ConnectorFactory:
    def __init__(self, credential_service: OAuthCredentialService):
        self.credential_service = credential_service

    async def get_connector_instance(self, org_id: uuid.UUID, provider: str):
        from app.integrations.registry import ConnectorRegistry
        
        # 1. Fetch credentials
        credentials = await self.credential_service.get_credentials(org_id, provider)
        
        # 2. Get the registered class
        connector_cls = ConnectorRegistry.get_connector_class(provider)
        
        # 3. Instantiate and return
        return connector_cls(credentials=credentials)

class IntegrationService:
    def __init__(self, session: AsyncSession, credential_service: OAuthCredentialService):
        self.session = session
        self.repo = ConnectorRepository(session)
        self.credential_service = credential_service
        self.google_oauth = GoogleOAuthFlowManager()

    async def list_integrations(self, org_id: uuid.UUID) -> list[Connector]:
        return await self.repo.list_by_org(org_id)

    async def begin_google_connect(self, org_id: uuid.UUID, user_id: uuid.UUID) -> str:
        state = create_oauth_state(org_id, user_id, "google_drive")
        return self.google_oauth.generate_authorization_url(state)

    async def complete_google_connect(self, org_id: uuid.UUID, code: str, state: str) -> Connector:
        # Validate state
        state_payload = parse_oauth_state(state)
        if state_payload["provider"] != "google_drive":
            raise ValueError("Invalid provider in OAuth state")
        if state_payload["org_id"] != str(org_id):
            raise ValueError("Invalid organization in OAuth state")
        
        # Exchange tokens
        tokens = await self.google_oauth.exchange_code_for_tokens(code)
        
        # Fetch user info for display name and uniqueness
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            })
            resp.raise_for_status()
            userinfo = resp.json()
            email = userinfo.get("email")
        
        # Ensure uniqueness
        existing = await self.repo.get_by_org_and_provider(org_id, "google_drive")
        if existing and existing.provider_account_id != email:
            raise ValueError("Another Google Drive account is already connected to this organization.")

        # Persist credentials
        await self.credential_service.store_credentials(
            org_id=org_id,
            provider="google_drive",
            credentials=tokens,
            provider_account_id=email
        )
        
        # Create or update Connector
        if existing:
            existing.status = ConnectorState.ACTIVE
            existing.health = "healthy"
            existing.provider_account_id = email
            existing.display_name = f"Google Drive ({email})"
            await self.session.flush()
            return existing
        else:
            connector = Connector(
                organization_id=org_id,
                provider="google_drive",
                display_name=f"Google Drive ({email})",
                status=ConnectorState.ACTIVE,
                health="healthy",
                provider_account_id=email,
                connected_at=datetime.utcnow()
            )
            return await self.repo.create_connector(connector)

    async def trigger_sync(self, org_id: uuid.UUID, integration_id: uuid.UUID, user_id: uuid.UUID = None) -> SyncJob:
        from sqlalchemy import select
        
        # 1. Fetch connector and ensure it belongs to org
        connector = await self.session.get(Connector, integration_id)
        if not connector or connector.organization_id != org_id:
            raise ValueError("Integration not found")
            
        if connector.status != ConnectorState.ACTIVE:
            raise ValueError("Cannot sync inactive integration")
            
        # 2. Prevent duplicate RUNNING/PENDING syncs (optional but good practice)
        stmt = select(SyncJob).where(
            SyncJob.connector_id == integration_id,
            SyncJob.status.in_([SyncJobStatus.PENDING, SyncJobStatus.RUNNING])
        )
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError("A sync job is already in progress for this integration")
            
        # 3. Create SyncJob
        job = SyncJob(
            organization_id=org_id,
            connector_id=integration_id,
            started_by=user_id,
            trigger_type=TriggerType.MANUAL,
            status=SyncJobStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        self.session.add(job)
        await self.session.flush() # Flush to get job.id without committing
        
        # 4. Enqueue background work
        from app.integrations.worker import enqueue_sync_job
        enqueue_sync_job(org_id, job.id, connector.provider)
        
        return job

    async def list_sync_jobs(self, org_id: uuid.UUID, limit: int = 20):
        from sqlalchemy import select
        stmt = select(SyncJob, Connector.provider).join(
            Connector, SyncJob.connector_id == Connector.id
        ).where(
            SyncJob.organization_id == org_id
        ).order_by(SyncJob.created_at.desc()).limit(limit)
        
        result = await self.session.execute(stmt)
        # Returns tuples of (SyncJob, provider_string)
        return result.all()

    async def get_sync_job(self, org_id: uuid.UUID, job_id: uuid.UUID):
        job = await self.session.get(SyncJob, job_id)
        if not job or job.organization_id != org_id:
            raise ValueError("Sync job not found")
        
        # We also need the provider to construct response
        connector = await self.session.get(Connector, job.connector_id)
        return job, connector.provider
