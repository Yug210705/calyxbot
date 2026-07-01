# Multi-Tenant Architecture

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [Database Design](../system/database-design.md)

---

## 3.1 Tenancy Model

Calyx uses a **shared database, shared schema** model with **row-level isolation**.

Every table that contains tenant-specific data includes an `org_id` column. This column is the tenant discriminator.

**Why shared schema instead of schema-per-tenant or database-per-tenant?**

| Approach | Pros | Cons | Verdict |
|---|---|---|---|
| **Database per tenant** | Strongest isolation, easy to reason about | Operationally expensive, connection pool explosion, migration complexity | Overkill for MVP |
| **Schema per tenant** | Good isolation, moderate complexity | Migration complexity scales linearly with tenants, Supabase doesn't natively support this well | Poor fit for Supabase |
| **Shared schema + RLS** | Simple operations, single migration path, Supabase-native, scales to thousands of tenants | Requires careful RLS policy design, risk of policy gaps | ✅ **Selected** |

## 3.2 Tenant Isolation Enforcement

Isolation is enforced at **three layers** — defense in depth.

### Layer 1: Database — PostgreSQL Row-Level Security (RLS)

Every tenant-scoped table has RLS policies that filter rows by `org_id`. The `org_id` is derived from the authenticated user's JWT claims (specifically, a custom claim set during authentication that reflects their current organization context).

RLS is the **last line of defense**. Even if the application layer has a bug, the database will refuse to return rows belonging to another tenant.

### Layer 2: Application — Service Layer Enforcement

Every service method receives the authenticated user's context (user ID, current org ID, role). Before performing any operation, the service layer validates that:

- The user is an active member of the target organization
- The user's role permits the requested operation
- The target resource belongs to the user's current organization

This layer exists because RLS alone cannot enforce complex business rules (e.g., "Managers can only edit documents in workspaces they own").

### Layer 3: API — Middleware Enforcement

API middleware extracts the organization context from the request (via a header, subdomain, or path prefix) and injects it into the request context. This ensures:

- Every request has a resolved org context before reaching any route handler
- The org context is set once and propagated consistently
- Cross-org requests are rejected at the edge

### Isolation Summary

```
Request → [API Middleware: resolve org context]
        → [Route Handler: pass context]
        → [Service Layer: validate membership + permissions]
        → [Repository Layer: query with org_id]
        → [PostgreSQL RLS: enforce row-level filter]
```

## 3.3 Cross-Organization Data Leak Prevention

| Vector | Mitigation |
|---|---|
| **Direct object reference** (IDOR) | Every resource lookup includes `org_id` in the query. Even if an attacker guesses a UUID, the RLS policy and service layer reject access. |
| **Search result leakage** | Vector search queries are scoped by `org_id` filter. Embeddings table has RLS. |
| **Audit log leakage** | Audit logs are scoped by `org_id`. Super Admin access is separately authorized and logged. |
| **Bulk export** | Export operations are scoped by `org_id` at the query level and validated in the service layer. |
| **Caching** | Cache keys include `org_id` as a prefix. No shared cache entries across tenants. (Relevant when caching is introduced post-MVP.) |
| **Error messages** | Error responses never include resource details from other tenants. Generic "not found" for any resource outside the user's org. |
| **File storage** | Supabase Storage buckets are organized by `org_id`. Storage policies enforce tenant-scoped access. |

## 3.4 Multi-Organization Membership

A single user (identified by email/auth ID) can belong to multiple organizations. This is essential for consultants, fractional executives, and employees at companies with multiple subsidiaries.

**How it works:**

- The `users` table holds identity data (email, name, avatar). It is **not** tenant-scoped.
- The `memberships` table associates a user with an organization and assigns a role. A user can have multiple membership records — one per organization.
- At any given time, the user operates within a **single active organization context**. The frontend provides an organization switcher (similar to Slack's workspace switcher).
- The active organization is stored client-side and sent with every API request. The backend validates membership on every request.
- A user can have **different roles** in different organizations (e.g., Admin in Org A, Employee in Org B).

**Key constraints:**

- Knowledge created in Org A is **never** visible in Org B, even if the same user is a member of both.
- There is no "merge" or "link" functionality across organizations.
- Deactivating a user in one org does not affect their membership in other orgs.

---
