# Role-Based Access Control (RBAC)

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [Security Model](../system/security-model.md)
- [User Personas](../product/personas.md)

---

## 5.1 RBAC Design

The authorization system is **Role-Based Access Control (RBAC)** with the following design goals:

- System roles cover MVP needs
- Architecture supports custom roles without schema changes
- Permissions are **resource + action** pairs
- Role-permission mappings are stored in the database, not hardcoded
- Permission checks are centralized in the service layer

## 5.2 Core Concepts

| Concept | Definition |
|---|---|
| **Role** | A named collection of permissions. Assigned to a user within the context of an organization. |
| **Permission** | A specific capability defined as `resource:action` (e.g., `document:create`, `member:invite`). |
| **Membership** | The association between a user, an organization, and a role. |
| **Resource** | An entity type in the system (organization, workspace, document, member, audit_log, etc.). |
| **Action** | An operation on a resource (create, read, update, delete, manage, export). |

## 5.3 System Roles

These roles are seeded into the database on deployment. They cannot be deleted. They can serve as templates for future custom roles.

| Role | Hierarchy Level | Description |
|---|---|---|
| `super_admin` | 0 (highest) | Platform-level role. Not assigned via memberships. |
| `org_admin` | 1 | Full control within an organization. |
| `manager` | 2 | Team and workspace management. |
| `employee` | 3 | Knowledge creation and consumption. |
| `viewer` | 4 (lowest) | Read-only access. |

## 5.4 Permission Catalog

| Permission | org_admin | manager | employee | viewer |
|---|---|---|---|---|
| `org:read` | ✅ | ✅ | ✅ | ✅ |
| `org:update` | ✅ | ❌ | ❌ | ❌ |
| `org:delete` | ✅ | ❌ | ❌ | ❌ |
| `member:invite` | ✅ | ✅ | ❌ | ❌ |
| `member:remove` | ✅ | ❌ | ❌ | ❌ |
| `member:update_role` | ✅ | ❌ | ❌ | ❌ |
| `member:list` | ✅ | ✅ | ✅ | ❌ |
| `workspace:create` | ✅ | ✅ | ❌ | ❌ |
| `workspace:read` | ✅ | ✅ | ✅ | ✅ |
| `workspace:update` | ✅ | ✅* | ❌ | ❌ |
| `workspace:delete` | ✅ | ✅* | ❌ | ❌ |
| `document:create` | ✅ | ✅ | ✅ | ❌ |
| `document:read` | ✅ | ✅ | ✅ | ✅ |
| `document:update` | ✅ | ✅* | ✅** | ❌ |
| `document:delete` | ✅ | ✅* | ✅** | ❌ |
| `knowledge:search` | ✅ | ✅ | ✅ | ✅ |
| `audit:read` | ✅ | ❌ | ❌ | ❌ |
| `integration:manage` | ✅ | ❌ | ❌ | ❌ |

*\* Manager: only within workspaces they own or are assigned to.*
*\*\* Employee: only their own documents.*

> [!NOTE]
> Asterisked permissions require **contextual authorization** — the permission alone is not sufficient. The service layer must also check resource ownership or workspace membership. This is a deliberate design choice: the RBAC system grants the *capability*, and the service layer enforces the *scope*.

## 5.5 Permission Inheritance

Roles form a strict hierarchy. A higher-level role **inherits all permissions** of lower-level roles.

```
org_admin ⊃ manager ⊃ employee ⊃ viewer
```

This is enforced by the permission resolution algorithm:

1. Load the user's role for the current organization
2. Load all permissions associated with that role
3. Permission check: does the loaded set include the required permission?

Inheritance is implemented by assigning the superset of permissions to each role in the database, not by runtime traversal. This keeps permission checks O(1) — a single set membership test.

## 5.6 Future: Custom Roles

The schema supports custom roles without migration:

- An Org Admin creates a new role scoped to their organization (`roles.org_id` = their org)
- They select permissions from the permission catalog
- They assign the custom role to members via the memberships table

**Constraints on custom roles:**
- Cannot exceed the Org Admin's own permissions (no privilege escalation)
- Cannot be assigned the `super_admin` platform permission set
- Custom roles are organization-scoped — they don't leak across tenants

## 5.7 Future: Enterprise Permissions

For enterprise customers, the RBAC system can be extended with:

- **Attribute-Based Access Control (ABAC):** Permissions conditioned on resource attributes (e.g., "can edit documents tagged 'engineering' but not 'legal'"). This would add a `conditions` JSON column to the `role_permissions` table.
- **Workspace-scoped roles:** Different roles per workspace (e.g., Admin in Workspace A, Viewer in Workspace B). This would use the `workspace_members` table's role field.
- **Approval workflows:** Certain actions (e.g., deleting a workspace) require approval from a higher role. This would add a pending actions queue.

These extensions are **additive** — they do not require changes to the core RBAC schema.

---
