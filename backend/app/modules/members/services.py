import uuid

from app.modules.members.models import Membership
from app.modules.members.repositories import MembershipRepository, RoleRepository


class MembershipService:
    def __init__(
        self,
        membership_repo: MembershipRepository,
        role_repo: RoleRepository
    ):
        self.membership_repo = membership_repo
        self.role_repo = role_repo

    async def get_organization_members(self, org_id: uuid.UUID, limit: int = 50, offset: int = 0) -> list[Membership]:
        return await self.membership_repo.list_by_organization(str(org_id), limit, offset)

    async def check_permission(self, user_id: uuid.UUID, org_id: uuid.UUID, required_permission: str) -> bool:
        """
        Check if a user has a specific permission in an organization.
        """
        membership = await self.membership_repo.get_by_user_and_org(str(user_id), str(org_id))
        if not membership:
            return False
        # We rely on the role relationship being eagerly loaded (selectin)
        # as configured in the Membership model.
        if not membership.role:
            return False

        for perm in membership.role.permissions:
            if perm.permission == required_permission:
                return True

        return False
