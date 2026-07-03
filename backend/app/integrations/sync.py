import uuid
from typing import Dict, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.models import SyncJob, TriggerType
from app.integrations.repositories import SyncJobRepository
from app.core.queue import TaskQueue

class SyncJobService:
    def __init__(self, session: AsyncSession, queue: TaskQueue):
        self.session = session
        self.repo = SyncJobRepository(session)
        self.queue = queue

    async def trigger_sync(self, org_id: uuid.UUID, connector_id: uuid.UUID, trigger_type: TriggerType) -> SyncJob:
        """Create a new SyncJob and enqueue it."""
        job = SyncJob(
            organization_id=org_id,
            connector_id=connector_id,
            trigger_type=trigger_type,
        )
        job = await self.repo.create_job(job)
        
        # Enqueue for background processing
        payload = {
            "job_id": str(job.id),
            "org_id": str(org_id),
            "connector_id": str(connector_id)
        }
        await self.queue.enqueue("sync_job", payload)
        
        return job
