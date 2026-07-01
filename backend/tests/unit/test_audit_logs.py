import pytest
import uuid
import asyncio
from unittest.mock import AsyncMock, patch

from app.shared.events import event_bus
from app.modules.organizations.services import OrganizationCreatedEvent
from app.modules.audit.services import AuditLogService

@pytest.mark.asyncio
@patch("app.modules.audit.services.AsyncSessionLocal")
async def test_audit_log_created_on_event(mock_async_session_local):
    org_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    # Mock the context manager for AsyncSessionLocal
    mock_session = AsyncMock()
    mock_async_session_local.return_value.__aenter__.return_value = mock_session
    
    # Set up the service
    audit_service = AuditLogService(event_bus)
    audit_service.setup_subscriptions()
    
    event = OrganizationCreatedEvent(
        name="organization.created",
        payload={
            "organization_id": str(org_id),
            "created_by": str(user_id),
            "slug": "test-audit-org"
        }
    )
    
    # Publish event
    await event_bus.publish(event)
    
    # Since event_bus.publish is async and InProcessEventBus awaits handlers directly,
    # the handler should have been executed.
    
    # Verify the session was used
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    
    # Verify the AuditLog passed to session.add
    audit_log = mock_session.add.call_args[0][0]
    assert audit_log.actor_id == user_id
    assert audit_log.resource_type == "organization"
    assert audit_log.resource_id == org_id
    assert audit_log.action == "organization.created"
    assert audit_log.after["slug"] == "test-audit-org"
