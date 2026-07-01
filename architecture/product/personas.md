# User Personas

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [RBAC](../system/rbac.md)

---

## 2.1 Role Definitions

### Super Admin

**Who:** Calyx platform operators (our internal team).

**Scope:** Platform-wide. Operates *across* all organizations.

| Responsibility | Detail |
|---|---|
| Platform health | Monitor system metrics, error rates, database performance |
| Organization management | Create, suspend, or delete organizations |
| Incident response | Investigate cross-tenant issues, security incidents |
| Feature flags | Enable/disable features per organization |
| Compliance | Access audit logs across all tenants for legal/compliance requests |

**Permissions:** All platform-level operations. Cannot access organization *content* (documents, memories) without explicit legal authorization and an audit trail entry.

> [!IMPORTANT]
> Super Admin is a **platform role**, not an organization role. It exists outside the tenant boundary. Super Admin access to tenant data must be logged, justified, and reviewable.

---

### Organization Admin

**Who:** The person who created the organization, or someone they promoted. Typically a CTO, VP of Engineering, Head of Operations, or Knowledge Manager.

**Scope:** Single organization.

| Responsibility | Detail |
|---|---|
| Organization settings | Name, branding, security policies, data retention rules |
| Member management | Invite, remove, change roles, deactivate accounts |
| Workspace management | Create, archive, delete workspaces |
| Knowledge oversight | View all knowledge within the org, manage visibility |
| Billing (future) | Manage subscription, payment methods |
| Audit review | Review audit logs for their organization |
| Ownership transfer | Transfer org ownership to another admin |

**Permissions:** Full CRUD on all resources within their organization. Cannot access other organizations. Cannot access platform-level operations.

---

### Manager

**Who:** Team leads, project managers, department heads. Responsible for a team's knowledge.

**Scope:** Their assigned workspaces and their team members' content within the organization.

| Responsibility | Detail |
|---|---|
| Team knowledge | Ensure their team's knowledge is captured and up to date |
| Workspace management | Manage workspaces they own or are assigned to |
| Member oversight | View activity and contributions of team members in their workspaces |
| Knowledge review | Approve, tag, and organize knowledge within their scope |
| Departure workflow | Initiate knowledge transfer when a team member leaves |

**Permissions:** CRUD on workspaces they own. Read access to all org-shared content. Write access to content within their workspaces. Can invite members to their workspaces. Cannot change organization settings or manage billing.

---

### Employee

**Who:** Individual contributors — engineers, designers, product managers, support staff. The primary knowledge creators.

**Scope:** Their own content and content shared with them.

| Responsibility | Detail |
|---|---|
| Knowledge creation | Document decisions, workflows, client context, technical details |
| Knowledge maintenance | Keep their own documents current |
| Search & retrieval | Use Calyx to find organizational knowledge |
| Collaboration | Contribute to shared workspaces |

**Permissions:** CRUD on their own content. Read access to content shared with them or with the org. Can join workspaces they're invited to. Cannot manage other users or organization settings.

---

### Viewer

**Who:** Stakeholders, executives, contractors, or external auditors who need read access but should not create or modify knowledge.

**Scope:** Content explicitly shared with them.

| Responsibility | Detail |
|---|---|
| Knowledge consumption | Read documents, search the knowledge base |
| Feedback (future) | Flag inaccurate or outdated content |

**Permissions:** Read-only access to content shared with them or marked org-visible. Cannot create, edit, or delete any content. Cannot manage users or settings.

---

## 2.2 Permission Summary Matrix

| Capability | Super Admin | Org Admin | Manager | Employee | Viewer |
|---|---|---|---|---|---|
| Platform management | ✅ | ❌ | ❌ | ❌ | ❌ |
| Organization settings | ⚠️ Audited | ✅ | ❌ | ❌ | ❌ |
| Member management | ⚠️ Audited | ✅ | ⚠️ Own workspaces | ❌ | ❌ |
| Create workspaces | ❌ | ✅ | ✅ | ❌ | ❌ |
| Create documents | ❌ | ✅ | ✅ | ✅ | ❌ |
| Edit own documents | ❌ | ✅ | ✅ | ✅ | ❌ |
| Edit others' documents | ❌ | ✅ | ⚠️ In own workspaces | ❌ | ❌ |
| Delete documents | ❌ | ✅ | ⚠️ In own workspaces | ⚠️ Own only | ❌ |
| Search knowledge | ❌ | ✅ | ✅ | ✅ | ✅ |
| View audit logs | ✅ All | ✅ Own org | ❌ | ❌ | ❌ |
| Manage integrations (future) | ❌ | ✅ | ❌ | ❌ | ❌ |

---
