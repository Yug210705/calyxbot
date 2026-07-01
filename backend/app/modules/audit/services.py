"""Audit log service to capture domain events."""

import uuid
from typing import Any, Dict
from datetime import datetime, timezone
import structlog

from app.shared.events import EventBus, DomainEvent
from app.core.database import AsyncSessionLocal
from app.core.logging import request_id_var, correlation_id_var
from app.modules.audit.models import AuditLog
from app.modules.audit.repositories import SQLAlchemyAuditLogRepository

logger = structlog.get_logger(__name__)


class AuditLogService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def setup_subscriptions(self) -> None:
        """Register event handlers with the event bus."""
        # Subscribe to all events we care about
        self.event_bus.subscribe("organization.created", self.handle_event)
        self.event_bus.subscribe("invitation.created", self.handle_event)
        self.event_bus.subscribe("invitation.accepted", self.handle_event)

    async def handle_event(self, event: DomainEvent) -> None:
        """Generic handler to translate domain events into audit logs."""
        try:
            req_id = request_id_var.get()
            corr_id = correlation_id_var.get()
            
            payload = event.payload
            
            organization_id_str = payload.get("organization_id")
            if not organization_id_str:
                logger.error("Domain event missing organization_id", domain_event=event.name)
                return
                
            organization_id = uuid.UUID(organization_id_str)
            
            # Determine actor. If not present in payload, we might need a contextvar.
            # Usually events contain the actor id (created_by, inviter_id, user_id).
            actor_id_str = payload.get("created_by") or payload.get("inviter_id") or payload.get("user_id")
            if not actor_id_str:
                logger.warning("Domain event missing explicit actor_id", domain_event=event.name)
                # Fallback to system user or a dummy UUID in a real enterprise app,
                # but for Calyx, mutations must provide an actor.
                actor_id = uuid.UUID(int=0)
            else:
                actor_id = uuid.UUID(actor_id_str)
                
            # Determine resource.
            resource_type = event.name.split(".")[0]
            resource_id_str = payload.get(f"{resource_type}_id")
            if not resource_id_str:
                # Fallback
                resource_id = organization_id
            else:
                resource_id = uuid.UUID(resource_id_str)

            audit_log = AuditLog(
                id=uuid.uuid4(),
                organization_id=organization_id,
                actor_id=actor_id,
                action=event.name,
                resource_type=resource_type,
                resource_id=resource_id,
                before=None,
                after=payload,
                created_at=datetime.now(timezone.utc),
                ip_address=None, # In a real app, this comes from a contextvar set in middleware
                user_agent=None, # Same here
                request_id=req_id if req_id else None,
                correlation_id=corr_id if corr_id else None,
            )

            async with AsyncSessionLocal() as session:
                repo = SQLAlchemyAuditLogRepository(session)
                await repo.create(audit_log)
                await session.commit()
                
            logger.debug("Audit log created", domain_event=event.name, corr_id=corr_id)

        except Exception as e:
            logger.exception("Failed to handle domain event for audit logging", domain_event=event.name, error=str(e))
