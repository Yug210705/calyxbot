import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.models import OAuthCredential, SyncJob, Connector

class ConnectorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_credential(self, credential: OAuthCredential) -> OAuthCredential:
        self.session.add(credential)
        await self.session.flush()
        await self.session.refresh(credential)
        return credential

    async def get_credential(self, org_id: uuid.UUID, provider: str) -> OAuthCredential | None:
        stmt = select(OAuthCredential).where(
            OAuthCredential.organization_id == org_id,
            OAuthCredential.connector_provider == provider,
            OAuthCredential.deleted_at.is_(None)
        ).order_by(OAuthCredential.created_at.desc())
        
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_connector(self, connector: Connector) -> Connector:
        self.session.add(connector)
        await self.session.flush()
        await self.session.refresh(connector)
        return connector

    async def get_by_org_and_provider(self, org_id: uuid.UUID, provider: str) -> Connector | None:
        stmt = select(Connector).where(
            Connector.organization_id == org_id,
            Connector.provider == provider,
            Connector.deleted_at.is_(None)
        ).order_by(Connector.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_by_org(self, org_id: uuid.UUID) -> list[Connector]:
        stmt = select(Connector).where(
            Connector.organization_id == org_id,
            Connector.deleted_at.is_(None)
        ).order_by(Connector.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_connector_status(
        self, 
        connector_id: uuid.UUID, 
        org_id: uuid.UUID, 
        status: str, 
        health: str, 
        sync_state: str | None = None
    ) -> Connector | None:
        stmt = select(Connector).where(
            Connector.id == connector_id,
            Connector.organization_id == org_id,
            Connector.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        connector = result.scalar_one_or_none()
        if connector:
            connector.status = status
            connector.health = health
            if sync_state is not None:
                connector.sync_state = sync_state
            await self.session.flush()
            await self.session.refresh(connector)
        return connector

class SyncJobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_job(self, job: SyncJob) -> SyncJob:
        self.session.add(job)
        await self.session.flush()
        await self.session.refresh(job)
        return job

    async def get_job(self, org_id: uuid.UUID, job_id: uuid.UUID) -> SyncJob | None:
        stmt = select(SyncJob).where(
            SyncJob.id == job_id,
            SyncJob.organization_id == org_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def list_jobs_by_connector(self, org_id: uuid.UUID, connector_id: uuid.UUID) -> list[SyncJob]:
        stmt = select(SyncJob).where(
            SyncJob.organization_id == org_id,
            SyncJob.connector_id == connector_id
        ).order_by(SyncJob.created_at.desc())
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
