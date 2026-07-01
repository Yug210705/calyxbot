import pytest
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock

from app.modules.members.invitation_service import (
    InvitationService,
    InvitationAlreadyAcceptedError,
    InvitationExpiredError,
    InvitationRevokedError,
    InvitationError
)
from app.modules.members.repositories import InvitationRepository, MembershipRepository, RoleRepository
from app.modules.members.invitation_models import Invitation
from app.modules.members.models import Membership
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.events import EventBus

@pytest.mark.asyncio
async def test_invitation_double_accept():
    session = AsyncMock(spec=AsyncSession)
    inv_repo = AsyncMock(spec=InvitationRepository)
    mem_repo = AsyncMock(spec=MembershipRepository)
    role_repo = AsyncMock(spec=RoleRepository)
    event_bus = AsyncMock(spec=EventBus)
    
    service = InvitationService(session, inv_repo, mem_repo, role_repo, event_bus)
    
    token = "test-token"
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    
    # Setup invitation already accepted
    invitation = Invitation(
        id=uuid.uuid4(),
        organization_id=org_id,
        email="test@example.com",
        role_id=uuid.uuid4(),
        invited_by=uuid.uuid4(),
        token_hash=token_hash,
        status="accepted",  # Already accepted!
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    
    inv_repo.get_by_token.return_value = invitation
    
    with pytest.raises(InvitationAlreadyAcceptedError):
        await service.accept_invitation(token, user_id)

@pytest.mark.asyncio
async def test_invitation_expired():
    session = AsyncMock(spec=AsyncSession)
    inv_repo = AsyncMock(spec=InvitationRepository)
    mem_repo = AsyncMock(spec=MembershipRepository)
    role_repo = AsyncMock(spec=RoleRepository)
    event_bus = AsyncMock(spec=EventBus)
    
    service = InvitationService(session, inv_repo, mem_repo, role_repo, event_bus)
    
    token = "test-token"
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    user_id = uuid.uuid4()
    
    invitation = Invitation(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        email="test@example.com",
        role_id=uuid.uuid4(),
        invited_by=uuid.uuid4(),
        token_hash=token_hash,
        status="pending",
        expires_at=datetime.now(timezone.utc) - timedelta(days=1)  # Expired!
    )
    
    inv_repo.get_by_token.return_value = invitation
    
    with pytest.raises(InvitationExpiredError):
        await service.accept_invitation(token, user_id)

@pytest.mark.asyncio
async def test_invitation_revoked():
    session = AsyncMock(spec=AsyncSession)
    inv_repo = AsyncMock(spec=InvitationRepository)
    mem_repo = AsyncMock(spec=MembershipRepository)
    role_repo = AsyncMock(spec=RoleRepository)
    event_bus = AsyncMock(spec=EventBus)
    
    service = InvitationService(session, inv_repo, mem_repo, role_repo, event_bus)
    
    token = "test-token"
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    user_id = uuid.uuid4()
    
    invitation = Invitation(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        email="test@example.com",
        role_id=uuid.uuid4(),
        invited_by=uuid.uuid4(),
        token_hash=token_hash,
        status="revoked",  # Revoked!
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    
    inv_repo.get_by_token.return_value = invitation
    
    with pytest.raises(InvitationRevokedError):
        await service.accept_invitation(token, user_id)

@pytest.mark.asyncio
async def test_invitation_already_member():
    session = AsyncMock(spec=AsyncSession)
    inv_repo = AsyncMock(spec=InvitationRepository)
    mem_repo = AsyncMock(spec=MembershipRepository)
    role_repo = AsyncMock(spec=RoleRepository)
    event_bus = AsyncMock(spec=EventBus)
    
    service = InvitationService(session, inv_repo, mem_repo, role_repo, event_bus)
    
    token = "test-token"
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    
    invitation = Invitation(
        id=uuid.uuid4(),
        organization_id=org_id,
        email="test@example.com",
        role_id=uuid.uuid4(),
        invited_by=uuid.uuid4(),
        token_hash=token_hash,
        status="pending",
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    
    inv_repo.get_by_token.return_value = invitation
    
    # Mock that membership already exists
    mem_repo.get_by_user_and_org.return_value = Membership(
        id=uuid.uuid4(), user_id=user_id, organization_id=org_id, role_id=uuid.uuid4(), status="ACTIVE"
    )
    
    with pytest.raises(InvitationError, match="You are already a member of this organization"):
        await service.accept_invitation(token, user_id)
