from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.integrations.schemas import IntegrationConnectionResponse, SyncJobResponse
from app.integrations.services import IntegrationService, OAuthCredentialService
from app.integrations.credentials import CredentialEncryptionService, EnvironmentKeyProvider
from app.integrations.models import Connector

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/integrations", tags=["integrations"])

def get_integration_service(db: AsyncSession = Depends(get_db)):
    key_provider = EnvironmentKeyProvider()
    encryption_service = CredentialEncryptionService(key_provider)
    cred_service = OAuthCredentialService(db, encryption_service)
    return IntegrationService(db, cred_service)

@router.get("", response_model=list[IntegrationConnectionResponse])
async def list_integrations(
    request: Request,
    service: IntegrationService = Depends(get_integration_service)
):
    # Fallback org ID for Sprint 5 since full auth might not be wired to frontend yet
    # In a real app, this comes from `get_current_user` dependency
    org_id_str = request.headers.get("X-Organization-Id", "00000000-0000-0000-0000-000000000001")
    try:
        org_id = uuid.UUID(org_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid organization ID")
        
    connectors = await service.list_integrations(org_id)
    return [
        IntegrationConnectionResponse(
            id=c.id,
            provider=c.provider,
            display_name=c.display_name,
            status=c.status,
            health=c.health,
            connected_at=c.connected_at,
            last_sync_at=c.last_sync_at,
            document_count=c.document_count,
            sync_state=c.sync_state
        ) for c in connectors
    ]

@router.post("/google/connect")
async def begin_google_connect(
    request: Request,
    service: IntegrationService = Depends(get_integration_service)
):
    org_id_str = request.headers.get("X-Organization-Id", "00000000-0000-0000-0000-000000000001")
    # Provide a mock user_id for the state payload
    user_id_str = request.headers.get("X-User-Id", "00000000-0000-0000-0000-000000000001")
    
    url = await service.begin_google_connect(uuid.UUID(org_id_str), uuid.UUID(user_id_str))
    return {"success": True, "data": {"authorization_url": url}, "meta": {}}

@router.get("/google/callback")
async def google_callback(
    request: Request,
    state: str = None,
    code: str = None,
    error: str = None,
    service: IntegrationService = Depends(get_integration_service)
):
    # This endpoint can redirect straight back to the frontend
    FRONTEND_URL = "http://localhost:3000/integrations"
    
    if error:
        logger.error("OAuth error returned from provider", error=error)
        return RedirectResponse(f"{FRONTEND_URL}?error=oauth_failed")
        
    if not state or not code:
        return RedirectResponse(f"{FRONTEND_URL}?error=missing_params")
        
    # The org_id is embedded in the signed state, so we extract it there
    # However, complete_google_connect requires org_id. 
    # Let's extract org_id from state first just to pass it, though services could do it.
    from app.integrations.oauth_state import parse_oauth_state
    
    try:
        state_payload = parse_oauth_state(state)
        org_id = uuid.UUID(state_payload["org_id"])
        
        # We need an active session transaction to complete this
        await service.complete_google_connect(org_id, code, state)
        await service.session.commit() # Important to commit the changes!
        return RedirectResponse(f"{FRONTEND_URL}?connected=google_drive")
        
    except Exception as e:
        logger.exception("Failed to complete Google OAuth", error=str(e))
        await service.session.rollback()
        return RedirectResponse(f"{FRONTEND_URL}?error=oauth_failed")

@router.post("/{integration_id}/sync", response_model=SyncJobResponse, status_code=202)
async def trigger_sync(
    integration_id: str,
    request: Request,
    service: IntegrationService = Depends(get_integration_service)
):
    org_id_str = request.headers.get("X-Organization-Id", "00000000-0000-0000-0000-000000000001")
    user_id_str = request.headers.get("X-User-Id", "00000000-0000-0000-0000-000000000001")
    
    try:
        org_id = uuid.UUID(org_id_str)
        integ_id = uuid.UUID(integration_id)
        user_id = uuid.UUID(user_id_str)
        
        job = await service.trigger_sync(org_id, integ_id, user_id)
        await service.session.commit()
        
        # Determine provider via connector ID for response
        # It's slightly cleaner to fetch from service if we wanted, but we know it's queued.
        # Actually trigger_sync checks the connector and we could return provider. 
        # But let's just do a quick fetch since we need provider for the response DTO
        connector = await service.session.get(Connector, integ_id)
        
        return SyncJobResponse(
            id=job.id,
            integration_id=job.connector_id,
            provider=connector.provider,
            status=job.status.value,
            documents_found=job.documents_found,
            documents_changed=job.documents_changed,
            documents_skipped=job.documents_skipped,
            documents_failed=job.documents_failed,
            bytes_processed=job.bytes_processed,
            duration_ms=job.duration_ms,
            error_message=job.error_message,
            created_at=job.created_at,
            started_at=job.started_at,
            finished_at=job.finished_at
        )
    except ValueError as e:
        await service.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await service.session.rollback()
        logger.exception("Trigger sync failed")
        raise e

@router.get("/jobs", response_model=list[SyncJobResponse])
async def list_sync_jobs_route(
    request: Request,
    service: IntegrationService = Depends(get_integration_service)
):
    org_id_str = request.headers.get("X-Organization-Id", "00000000-0000-0000-0000-000000000001")
    try:
        org_id = uuid.UUID(org_id_str)
        jobs_with_providers = await service.list_sync_jobs(org_id)
        
        response = []
        for job, provider in jobs_with_providers:
            response.append(SyncJobResponse(
                id=job.id,
                integration_id=job.connector_id,
                provider=provider,
                status=job.status.value,
                documents_found=job.documents_found,
                documents_changed=job.documents_changed,
                documents_skipped=job.documents_skipped,
                documents_failed=job.documents_failed,
                bytes_processed=job.bytes_processed,
                duration_ms=job.duration_ms,
                error_message=job.error_message,
                created_at=job.created_at,
                started_at=job.started_at,
                finished_at=job.finished_at
            ))
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/jobs/{job_id}", response_model=SyncJobResponse)
async def get_sync_job_route(
    job_id: str,
    request: Request,
    service: IntegrationService = Depends(get_integration_service)
):
    org_id_str = request.headers.get("X-Organization-Id", "00000000-0000-0000-0000-000000000001")
    try:
        org_id = uuid.UUID(org_id_str)
        job_uuid = uuid.UUID(job_id)
        job, provider = await service.get_sync_job(org_id, job_uuid)
        
        return SyncJobResponse(
            id=job.id,
            integration_id=job.connector_id,
            provider=provider,
            status=job.status.value,
            documents_found=job.documents_found,
            documents_changed=job.documents_changed,
            documents_skipped=job.documents_skipped,
            documents_failed=job.documents_failed,
            bytes_processed=job.bytes_processed,
            duration_ms=job.duration_ms,
            error_message=job.error_message,
            created_at=job.created_at,
            started_at=job.started_at,
            finished_at=job.finished_at
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch sync job")

@router.post("/{integration_id}/pause")
async def pause_integration(integration_id: str):
    return {"success": True}

@router.post("/{integration_id}/resume")
async def resume_integration(integration_id: str):
    return {"success": True}

@router.delete("/{integration_id}")
async def disconnect_integration(integration_id: str):
    return {"success": True}

