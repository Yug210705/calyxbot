import abc
import uuid
from datetime import UTC

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Organization


class OrganizationRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, organization: Organization) -> Organization:
        """Create a new organization."""
        pass

    @abc.abstractmethod
    async def get_by_id(self, org_id: uuid.UUID) -> Organization | None:
        """Get an organization by ID."""
        pass

    @abc.abstractmethod
    async def get_by_slug(self, slug: str) -> Organization | None:
        """Get an organization by slug."""
        pass

    @abc.abstractmethod
    async def delete(self, org_id: uuid.UUID) -> bool:
        """Soft delete an organization."""
        pass

    @abc.abstractmethod
    async def restore(self, org_id: uuid.UUID) -> bool:
        """Restore a soft-deleted organization."""
        pass

class SQLAlchemyOrganizationRepository(OrganizationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, organization: Organization) -> Organization:
        try:
            self.session.add(organization)
            await self.session.flush()
            await self.session.refresh(organization)
            return organization
        except IntegrityError as e:
            await self.session.rollback()
            # If slug is not unique, we could raise a custom domain exception here.
            # We'll just re-raise for now and let the service handle it or wrap it.
            raise e

    async def get_by_id(self, org_id: uuid.UUID) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.id == org_id, Organization.deleted_at.is_(None))
        )
        return result.scalars().first()

    async def get_by_slug(self, slug: str) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.slug == slug, Organization.deleted_at.is_(None))
        )
        return result.scalars().first()

    async def delete(self, org_id: uuid.UUID) -> bool:
        from datetime import datetime
        result = await self.session.execute(
            select(Organization).where(Organization.id == org_id, Organization.deleted_at.is_(None))
        )
        org = result.scalars().first()
        if org:
            org.deleted_at = datetime.now(UTC)
            await self.session.flush()
            return True
        return False

    async def restore(self, org_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(Organization).where(Organization.id == org_id, Organization.deleted_at.is_not(None))
        )
        org = result.scalars().first()
        if org:
            org.deleted_at = None
            await self.session.flush()
            return True
        return False
