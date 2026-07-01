import hashlib
import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.modules.members.invitation_models import Invitation
from app.modules.members.invitation_service import (
    InvitationExpiredError,
    InvitationService,
)
from app.modules.members.models import Role


@pytest.fixture
def mock_invitation_repo():
    return AsyncMock()

@pytest.fixture
def mock_membership_repo():
    return AsyncMock()

@pytest.fixture
def mock_role_repo():
    return AsyncMock()

@pytest.fixture
def mock_event_bus():
    return AsyncMock()

@pytest.fixture
def invitation_service(mock_db_session, mock_invitation_repo, mock_membership_repo, mock_role_repo, mock_event_bus):
    return InvitationService(
        session=mock_db_session,
        invitation_repo=mock_invitation_repo,
        membership_repo=mock_membership_repo,
        role_repo=mock_role_repo,
        event_bus=mock_event_bus,
    )

@pytest.mark.asyncio
async def test_create_invitation(invitation_service, mock_role_repo, mock_invitation_repo, mock_event_bus):
    org_id = uuid.uuid4()
    inviter_id = uuid.uuid4()
    role_id = uuid.uuid4()

    mock_role_repo.get_by_name.return_value = Role(id=role_id, name="employee")

    # Setup mock to return the same invitation object when create is called
    async def mock_create(invitation):
        return invitation
    mock_invitation_repo.create.side_effect = mock_create

    invitation, raw_token = await invitation_service.create_invitation(
        organization_id=org_id,
        email="invitee@example.com",
        role_name="employee",
        inviter_id=inviter_id,
    )

    assert invitation.email == "invitee@example.com"
    assert invitation.role_id == role_id
    assert invitation.status == "pending"
    assert len(raw_token) > 20

    # Ensure token hash matches
    expected_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    assert invitation.token_hash == expected_hash

    # Ensure event was published
    mock_event_bus.publish.assert_called_once()

@pytest.mark.asyncio
async def test_accept_invitation_success(invitation_service, mock_invitation_repo, mock_membership_repo, mock_event_bus):
    raw_token = "some-secure-token"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()

    invitation = Invitation(
        id=uuid.uuid4(),
        organization_id=org_id,
        role_id=uuid.uuid4(),
        email="invitee@example.com",
        status="pending",
        token_hash=token_hash,
        invited_by=uuid.uuid4(),
        expires_at=datetime.now(UTC) + timedelta(hours=24)
    )

    mock_invitation_repo.get_by_token.return_value = invitation
    mock_membership_repo.get_by_user_and_org.return_value = None # Not a member yet

    async def mock_create_membership(m):
        return m
    mock_membership_repo.create.side_effect = mock_create_membership

    membership = await invitation_service.accept_invitation(raw_token, user_id)

    assert membership.user_id == user_id
    assert membership.organization_id == org_id
    assert invitation.status == "accepted"

    mock_event_bus.publish.assert_called_once()

@pytest.mark.asyncio
async def test_accept_invitation_expired(invitation_service, mock_invitation_repo):
    raw_token = "some-secure-token"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    invitation = Invitation(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        role_id=uuid.uuid4(),
        email="invitee@example.com",
        status="pending",
        token_hash=token_hash,
        invited_by=uuid.uuid4(),
        expires_at=datetime.now(UTC) - timedelta(hours=1) # Expired
    )

    mock_invitation_repo.get_by_token.return_value = invitation

    with pytest.raises(InvitationExpiredError):
        await invitation_service.accept_invitation(raw_token, uuid.uuid4())
