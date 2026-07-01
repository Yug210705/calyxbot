import uuid
from typing import Optional
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.events import EventBus, DomainEvent
from app.modules.members.repositories import MembershipRepository, RoleRepository
from app.modules.members.models import Membership
from .models import Organization
from .repositories import OrganizationRepository
from .schemas import OrganizationCreate

@dataclass
class OrganizationCreatedEvent(DomainEvent):
    pass

class OrganizationService:
    def __init__(
        self,
        session: AsyncSession,
        org_repo: OrganizationRepository,
        membership_repo: MembershipRepository,
        role_repo: RoleRepository,
        event_bus: EventBus
    ):
        self.session = session
        self.org_repo = org_repo
        self.membership_repo = membership_repo
        self.role_repo = role_repo
        self.event_bus = event_bus

    async def create_organization(self, user_id: uuid.UUID, data: OrganizationCreate) -> Organization:
        # Check if slug exists to provide a friendly error (though DB constraint will also catch this)
        existing = await self.org_repo.get_by_slug(data.slug)
        if existing:
            raise ValueError(f"Organization with slug '{data.slug}' already exists")

        # 1. Create Organization
        org = Organization(
            name=data.name,
            slug=data.slug,
            created_by=user_id,
            # Other fields use defaults
        )
        org = await self.org_repo.create(org)

        # 2. Get Owner Role
        owner_role = await self.role_repo.get_by_name("owner")

        # 3. Create Membership for creator as Owner
        membership = Membership(
            user_id=user_id,
            organization_id=org.id,
            role_id=owner_role.id,
            status="ACTIVE"
        )
        await self.membership_repo.create(membership)
        
        # Commit the transaction to persist all changes
        await self.session.commit()

        # 4. Publish Domain Event
        event = OrganizationCreatedEvent(
            name="organization.created",
            payload={
                "organization_id": str(org.id),
                "created_by": str(user_id),
                "slug": org.slug
            }
        )
        await self.event_bus.publish(event)

        return org
