import uuid
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dashboard.schemas import (
    DashboardResponse,
    DashboardStatsResponse,
    DashboardActivityItemResponse,
    DashboardChecklistItemResponse,
)

from app.integrations.models import Connector, SyncJob, SyncJobStatus, ConnectorState
from app.modules.documents.models import Document, DocumentChunk

class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dashboard(self, org_id: uuid.UUID) -> DashboardResponse:
        # 1. Stats
        # Active connectors
        stmt_connectors = select(func.count(Connector.id)).where(
            Connector.organization_id == org_id,
            Connector.deleted_at.is_(None)
        )
        connected_sources = await self.session.scalar(stmt_connectors) or 0

        # Total documents
        stmt_docs = select(func.count(Document.id)).where(
            Document.organization_id == org_id,
            Document.deleted_at.is_(None)
        )
        documents_total = await self.session.scalar(stmt_docs) or 0

        # Knowledge objects (chunks mapped to active documents)
        stmt_chunks = (
            select(func.count(DocumentChunk.id))
            .join(Document, Document.id == DocumentChunk.document_id)
            .where(
                Document.organization_id == org_id,
                DocumentChunk.deleted_at.is_(None)
            )
        )
        knowledge_objects_total = await self.session.scalar(stmt_chunks) or 0

        # Last sync
        stmt_last_sync = select(func.max(SyncJob.finished_at)).where(
            SyncJob.organization_id == org_id,
            SyncJob.status == SyncJobStatus.SUCCESS
        )
        last_sync_at = await self.session.scalar(stmt_last_sync)

        stats = DashboardStatsResponse(
            connected_sources=connected_sources,
            documents_total=documents_total,
            knowledge_objects_total=knowledge_objects_total,
            last_sync_at=last_sync_at
        )

        # 2. Activity Feed
        stmt_jobs = select(SyncJob).where(
            SyncJob.organization_id == org_id
        ).order_by(SyncJob.started_at.desc().nullslast()).limit(5)
        
        result_jobs = await self.session.execute(stmt_jobs)
        recent_jobs = result_jobs.scalars().all()
        
        activity_items = []
        recent_failed_jobs = 0
        has_successful_sync = False
        
        for job in recent_jobs:
            if job.status == SyncJobStatus.FAILED:
                recent_failed_jobs += 1
                job_type = "sync_failed"
                title = "Sync Failed"
                description = job.error_message or "Sync job encountered an error"
            else:
                if job.status == SyncJobStatus.SUCCESS:
                    has_successful_sync = True
                job_type = "sync_success"
                title = "Sync Completed"
                description = f"{job.documents_changed} documents changed, {job.documents_skipped} skipped"
                
            activity_items.append(DashboardActivityItemResponse(
                id=str(job.id),
                type=job_type,
                title=title,
                description=description,
                created_at=job.started_at or job.created_at,
                status=job.status.value
            ))

        # Check if there are any successful sync jobs historically if none in recent 5
        if not has_successful_sync:
            stmt_any_success = select(SyncJob.id).where(
                SyncJob.organization_id == org_id,
                SyncJob.status == SyncJobStatus.SUCCESS
            ).limit(1)
            any_success = await self.session.scalar(stmt_any_success)
            if any_success:
                has_successful_sync = True

        # 3. Checklist
        checklist = [
            DashboardChecklistItemResponse(
                id="connect_drive",
                label="Connect Google Drive",
                completed=connected_sources > 0,
                href="/integrations"
            ),
            DashboardChecklistItemResponse(
                id="run_sync",
                label="Run first sync",
                completed=has_successful_sync,
                href="/integrations"
            ),
            DashboardChecklistItemResponse(
                id="open_documents",
                label="Open Documents",
                completed=documents_total > 0,
                href="/documents"
            )
        ]

        # 4. System Health
        health = {
            "search": "ready" if documents_total > 0 else "empty",
            "ingestion": "connected" if connected_sources > 0 else "not_connected",
            "sync": "healthy" if recent_failed_jobs == 0 else "attention"
        }

        return DashboardResponse(
            stats=stats,
            activity=activity_items,
            checklist=checklist,
            system_health=health
        )
