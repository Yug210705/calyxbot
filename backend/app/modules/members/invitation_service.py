"""Invitation service — handles invite creation, acceptance, revocation."""

import uuid
import hashlib
import secrets
from datetime import datetime, timezone, timedelta

from app.modules.members.repositories import (
    InvitationRepository,
    MembershipRepository,
    RoleRepository,
)
from app.modules.members.invitation_models import Invitation
from app.modules.members.models import Membership
from app.shared.events import EventBus, DomainEvent
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession


INVITATION_EXPIRY_HOURS = 72


@dataclass
class InvitationCreatedEvent(DomainEvent):
    pass

@dataclass
class InvitationAcceptedEvent(DomainEvent):
    pass


class InvitationError(Exception):
    """Base class for invitation errors."""
    pass


class InvitationExpiredError(InvitationError):
    pass


class InvitationAlreadyAcceptedError(InvitationError):
    pass


class InvitationRevokedError(InvitationError):
    pass


class InvitationService:
    def __init__(
        self,
        session: AsyncSession,
        invitation_repo: InvitationRepository,
        membership_repo: MembershipRepository,
        role_repo: RoleRepository,
        event_bus: EventBus,
    ):
        self.session = session
        self.invitation_repo = invitation_repo
        self.membership_repo = membership_repo
        self.role_repo = role_repo
        self.event_bus = event_bus

    async def create_invitation(
        self,
        organization_id: uuid.UUID,
        email: str,
        role_name: str,
        inviter_id: uuid.UUID,
    ) -> tuple[Invitation, str]:
        """
        Create an invitation and return (invitation, raw_token).
        The raw_token is what gets sent in the invite link.
        We store the hash of the token for security.
        """
        # Validate role exists
        role = await self.role_repo.get_by_name(role_name)

        # Generate a secure token
        raw_token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        expires_at = datetime.now(timezone.utc) + timedelta(hours=INVITATION_EXPIRY_HOURS)

        invitation = Invitation(
            id=uuid.uuid4(),
            organization_id=organization_id,
            email=email.lower().strip(),
            role_id=role.id,
            invited_by=inviter_id,
            token_hash=token_hash,
            status="pending",
            expires_at=expires_at,
        )

        invitation = await self.invitation_repo.create(invitation)

        # Commit transaction
        await self.session.commit()

        # Publish domain event
        await self.event_bus.publish(InvitationCreatedEvent(
            name="invitation.created",
            payload={
                "invitation_id": str(invitation.id),
                "organization_id": str(organization_id),
                "email": email,
                "inviter_id": str(inviter_id),
                "expires_at": expires_at.isoformat(),
            }
        ))

        return invitation, raw_token

    async def accept_invitation(
        self,
        raw_token: str,
        user_id: uuid.UUID,
    ) -> Membership:
        """
        Accept an invitation using the raw token.
        Creates a Membership for the user in the organization.
        """
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        invitation = await self.invitation_repo.get_by_token(token_hash)

        if not invitation:
            raise InvitationError("Invalid invitation token.")

        # Validate invitation state
        if invitation.status == "accepted":
            raise InvitationAlreadyAcceptedError("This invitation has already been accepted.")

        if invitation.status == "revoked":
            raise InvitationRevokedError("This invitation has been revoked.")

        if invitation.expires_at < datetime.now(timezone.utc):
            raise InvitationExpiredError("This invitation has expired.")

        # Check if user is already a member
        existing = await self.membership_repo.get_by_user_and_org(
            str(user_id), str(invitation.organization_id)
        )
        if existing:
            raise InvitationError("You are already a member of this organization.")

        # Create membership
        membership = Membership(
            id=uuid.uuid4(),
            user_id=user_id,
            organization_id=invitation.organization_id,
            role_id=invitation.role_id,
            status="ACTIVE",
        )
        membership = await self.membership_repo.create(membership)

        # Update invitation status
        invitation.status = "accepted"
        invitation.accepted_at = datetime.now(timezone.utc)
        
        # Commit transaction
        await self.session.commit()

        # Publish domain event
        await self.event_bus.publish(InvitationAcceptedEvent(
            name="invitation.accepted",
            payload={
                "invitation_id": str(invitation.id),
                "organization_id": str(invitation.organization_id),
                "user_id": str(user_id),
                "email": invitation.email,
            }
        ))

        return membership
