import pytest
import uuid
from unittest.mock import AsyncMock

from app.modules.members.models import Role, Permission, Membership
from app.modules.members.services import MembershipService
from app.modules.members.repositories import MembershipRepository, RoleRepository

RBAC_MATRIX = {
    "owner": [
        "organization.update", "organization.delete", "organization.billing", "organization.settings",
        "invitation.create", "invitation.read", "invitation.revoke",
        "membership.read", "membership.update", "membership.remove",
        "audit.read", "memory.create", "memory.read", "memory.delete"
    ],
    "admin": [
        "organization.update", "organization.billing", "organization.settings",
        "invitation.create", "invitation.read", "invitation.revoke",
        "membership.read", "membership.update", "membership.remove",
        "audit.read", "memory.create", "memory.read", "memory.delete"
    ],
    "manager": [
        "organization.settings",
        "invitation.create", "invitation.read", "invitation.revoke",
        "membership.read", "membership.update",
        "memory.create", "memory.read", "memory.delete"
    ],
    "billing_admin": [
        "organization.billing", "membership.read"
    ],
    "employee": [
        "invitation.read", "membership.read",
        "memory.create", "memory.read"
    ],
    "viewer": [
        "invitation.read", "membership.read", "memory.read", "audit.read"
    ]
}

ALL_PERMISSIONS = list(set(perm for perms in RBAC_MATRIX.values() for perm in perms))

@pytest.mark.asyncio
async def test_exhaustive_rbac_matrix():
    # Mock repos
    membership_repo = AsyncMock(spec=MembershipRepository)
    role_repo = AsyncMock(spec=RoleRepository)
    
    service = MembershipService(membership_repo, role_repo)
    
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    
    # We will iterate through each role and test every permission
    for role_name, expected_perms in RBAC_MATRIX.items():
        # Build fake role with permissions
        role = Role(id=uuid.uuid4(), name=role_name)
        role.permissions = [Permission(id=uuid.uuid4(), permission=p) for p in expected_perms]
        
        # Build fake membership
        membership = Membership(
            id=uuid.uuid4(),
            user_id=user_id,
            organization_id=org_id,
            role_id=role.id,
            status="ACTIVE"
        )
        membership.role = role
        
        # Setup mock return value
        membership_repo.get_by_user_and_org.return_value = membership
        
        for permission in ALL_PERMISSIONS:
            has_permission = await service.check_permission(user_id, org_id, permission)
            should_have_permission = permission in expected_perms
            
            assert has_permission == should_have_permission, \
                f"Role '{role_name}' should {'have' if should_have_permission else 'NOT have'} permission '{permission}'"

    # Generate coverage report locally for proof
    with open("rbac_coverage_report.txt", "w") as f:
        f.write("RBAC Permission Coverage Report\n")
        f.write("===============================\n\n")
        for role_name in RBAC_MATRIX.keys():
            f.write(f"Role: {role_name}\n")
            for perm in ALL_PERMISSIONS:
                status = "YES" if perm in RBAC_MATRIX[role_name] else "NO"
                f.write(f"  - {perm}: {status}\n")
            f.write("\n")
