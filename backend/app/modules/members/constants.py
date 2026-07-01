"""RBAC Constants and Enums."""

from enum import Enum


class SystemRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    BILLING_ADMIN = "billing_admin"
    EMPLOYEE = "employee"
    VIEWER = "viewer"


class Permissions(str, Enum):
    # Organization Permissions
    ORG_READ = "organization.read"
    ORG_UPDATE = "organization.update"
    ORG_DELETE = "organization.delete"
    ORG_SETTINGS = "organization.settings"
    ORG_BILLING = "organization.billing"

    # Invitation Permissions
    INVITE_CREATE = "invitation.create"
    INVITE_READ = "invitation.read"
    INVITE_REVOKE = "invitation.revoke"

    # Membership Permissions
    MEMBER_READ = "membership.read"
    MEMBER_UPDATE = "membership.update"
    MEMBER_REMOVE = "membership.remove"

    # Audit Permissions
    AUDIT_READ = "audit.read"

    # Memory Permissions
    MEMORY_CREATE = "memory.create"
    MEMORY_READ = "memory.read"
    MEMORY_DELETE = "memory.delete"
