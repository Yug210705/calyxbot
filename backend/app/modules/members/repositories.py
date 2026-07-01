import abc
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Membership, Role

class MembershipRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, membership: Membership) -> Membership:
        pass

    @abc.abstractmethod
    async def get_by_user_and_org(self, user_id: str, org_id: str) -> Membership | None:
        pass

    @abc.abstractmethod
    async def list_by_organization(self, org_id: str, limit: int = 50, offset: int = 0) -> list[Membership]:
        pass

class SQLAlchemyMembershipRepository(MembershipRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, membership: Membership) -> Membership:
        self.session.add(membership)
        await self.session.flush()
        await self.session.refresh(membership)
        return membership

    async def get_by_user_and_org(self, user_id: str, org_id: str) -> Membership | None:
        from sqlalchemy import select
        result = await self.session.execute(
            select(Membership).where(
                Membership.user_id == user_id, 
                Membership.organization_id == org_id,
                Membership.deleted_at.is_(None)
            )
        )
        return result.scalars().first()

    async def list_by_organization(self, org_id: str, limit: int = 50, offset: int = 0) -> list[Membership]:
        from sqlalchemy import select
        # In a real app we'd join with User to get emails/names. For MVP, we can lazy load or explicit join.
        from sqlalchemy.orm import joinedload
        result = await self.session.execute(
            select(Membership)
            .options(joinedload(Membership.user), joinedload(Membership.role))
            .where(
                Membership.organization_id == org_id,
                Membership.deleted_at.is_(None)
            )
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

class RoleRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_name(self, name: str) -> Role:
        pass

class SQLAlchemyRoleRepository(RoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_name(self, name: str) -> Role:
        from sqlalchemy import select
        result = await self.session.execute(select(Role).where(Role.name == name))
        role = result.scalars().first()
        if not role:
            raise ValueError(f"Role {name} not found")
        return role

class InvitationRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, invitation: 'Invitation') -> 'Invitation':
        pass

    @abc.abstractmethod
    async def get_by_token(self, token_hash: str) -> 'Invitation | None':
        pass

class SQLAlchemyInvitationRepository(InvitationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, invitation: 'Invitation') -> 'Invitation':
        self.session.add(invitation)
        await self.session.flush()
        await self.session.refresh(invitation)
        return invitation

    async def get_by_token(self, token_hash: str) -> 'Invitation | None':
        from sqlalchemy import select
        from app.modules.members.invitation_models import Invitation
        result = await self.session.execute(
            select(Invitation).where(
                Invitation.token_hash == token_hash,
                Invitation.deleted_at.is_(None)
            )
        )
        return result.scalars().first()
