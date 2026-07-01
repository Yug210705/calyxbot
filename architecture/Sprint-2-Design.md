# Sprint 2 Design: Organization & Access Platform

## 1. Goal
End of Sprint 2: A company can Signup -> Create Organization -> Invite Employees -> Accept Invite -> Assign Roles -> Enforce Permissions -> Audit Logs Generated.

## 2. Organization Domain Model

Organizations are the root of tenancy in Calyx. Every resource (except global user accounts) belongs to an Organization.
Memberships map Users to Organizations and hold the RBAC Roles. All core mutations publish Domain Events (e.g., `OrganizationCreated`) via an in-process event bus to handle side-effects cleanly.

## 3. Database Design (Updated ER Diagram)

```mermaid
erDiagram
    USERS ||--o{ MEMBERSHIPS : has
    USERS ||--o{ AUDIT_LOGS : performs
    ORGANIZATIONS ||--o{ MEMBERSHIPS : contains
    ORGANIZATIONS ||--o{ INVITATIONS : sends
    ORGANIZATIONS ||--o{ AUDIT_LOGS : records
    ROLES ||--o{ MEMBERSHIPS : grants
    ROLES ||--o{ ROLE_PERMISSIONS : defines
    PERMISSIONS ||--o{ ROLE_PERMISSIONS : maps
    
    USERS {
        uuid id PK
        string email
        string full_name
        timestamp created_at
    }
    
    ORGANIZATIONS {
        uuid id PK
        string name
        string slug UK "Unique constraint for subdomains"
        string logo_url
        string plan
        string status
        uuid created_by FK
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at "Soft delete"
    }
    
    MEMBERSHIPS {
        uuid id PK
        uuid user_id FK
        uuid organization_id FK
        uuid role_id FK
        string status "ACTIVE, INVITED, SUSPENDED, REMOVED"
        timestamp created_at
        timestamp deleted_at "Soft delete"
    }
    
    ROLES {
        uuid id PK
        string name "owner, admin, billing_admin, manager, employee, viewer"
    }
    
    PERMISSIONS {
        uuid id PK
        string permission "e.g., organization.read, invitation.create"
    }
    
    ROLE_PERMISSIONS {
        uuid role_id FK
        uuid permission_id FK
    }
    
    INVITATIONS {
        uuid id PK
        uuid organization_id FK
        uuid role_id FK
        string email
        string status "pending, accepted, expired, revoked"
        string token_hash "Hashed token, never plaintext"
        uuid invited_by FK
        timestamp expires_at
        timestamp accepted_at
        timestamp revoked_at
        timestamp created_at
        timestamp deleted_at "Soft delete"
    }
    
    AUDIT_LOGS {
        uuid id PK
        uuid organization_id FK
        uuid actor_id FK
        string action
        string resource_type
        uuid resource_id
        json before "Snapshot prior to mutation"
        json after "Snapshot after mutation"
        timestamp created_at
        string ip_address
        string user_agent
        string request_id
    }
```
**Database Constraints:**
- `organization.slug`: UNIQUE
- `membership (user_id, organization_id)`: UNIQUE
- `invitation (email, organization_id)`: UNIQUE WHERE `status='pending'`

## 4. Invitation State Machine

```mermaid
stateDiagram-v2
    [*] --> Pending : Owner/Admin invites user
    Pending --> Accepted : User clicks link & registers
    Pending --> Expired : Time > expires_at
    Pending --> Revoked : Admin cancels invite
    Accepted --> [*]
    Expired --> [*]
    Revoked --> [*]
```

## 5. RBAC Permission Matrix

System Roles: Owner, Admin, Billing Admin, Manager, Employee, Viewer
Granular String-Based Permissions

| Permission | Owner | Admin | Billing Admin | Manager | Employee | Viewer |
|------------|-------|-------|---------------|---------|----------|--------|
| `organization.read` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `organization.update` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `organization.delete` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `organization.billing` | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `organization.settings` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `invitation.create` | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| `invitation.read` | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| `invitation.revoke` | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| `membership.read` | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| `membership.update` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `membership.remove` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `audit.read` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `memory.read` (Future)| ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| `memory.create` (Future)| ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| `memory.delete` (Future)| ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |

## 6. Authorization Service Design

The `AuthorizationService` resolves RBAC dynamically without hardcoding role enums in business logic. It relies on an `AuthorizationContext`.

**Context Model:**
```python
class AuthorizationContext:
    user: User
    membership: Membership
    organization: Organization
    permissions: List[str]
```

**Core Function Signature:**
`AuthorizationService.authorize(context: AuthorizationContext, resource: str, action: str) -> None`
*Note: Translates `resource` and `action` to `{resource}.{action}` string format, or directly accepts `permission: str`.*

## 7. Audit Log Specification

Every sensitive mutation creates an immutable Audit Log with exact state transitions.

**Trigger Events:**
- Organization created/updated
- User invited, accepted invite, or revoked
- Role changed for a membership
- User removed from organization

**Log Structure:**
- `actor_id`: UUID
- `action`: e.g., `role.updated`
- `resource_type`: e.g., `membership`
- `resource_id`: UUID
- `before`: JSON blob (e.g., `{ "role": "employee" }`)
- `after`: JSON blob (e.g., `{ "role": "admin" }`)
- `ip_address`, `user_agent`, `request_id`: For robust traceability.

## 8. API Contracts & Rules

**Strict Standard Rules:**
- All endpoints prefixed with `/api/v1/`.
- No route contains business logic (`Router -> Service -> Repository -> Database`).
- **Idempotency:** `POST /organizations` supports the `Idempotency-Key` header.
- **Rate Limiting:**
  - `POST /organizations/:id/invitations`: 10 requests / minute / organization
  - `POST /invitations/:id/accept`: 5 requests / minute / IP

**Standardized API Responses:**
Success:
```json
{
  "success": true,
  "data": { ... },
  "meta": { ... }
}
```
Error:
```json
{
  "success": false,
  "error": {
    "code": "INVITATION_EXPIRED",
    "message": "Invitation has expired.",
    "details": {},
    "request_id": "req-12345",
    "timestamp": "2026-07-01T10:00:00Z"
  }
}
```

## 9. Sequence Diagrams

### Invitation Flow
```mermaid
sequenceDiagram
    participant Admin
    participant Router
    participant InvitationService
    participant AuthContext
    participant Repository
    participant EventBus
    participant Email

    Admin->>Router: POST /org/{id}/invitations
    Router->>AuthContext: Build Context
    Router->>InvitationService: create_invite(Context, email, role)
    InvitationService->>AuthContext: authorize(context, "invitation", "create")
    AuthContext-->>InvitationService: OK
    InvitationService->>Repository: Check Rate Limit & DB Constraint
    InvitationService->>Repository: Create Invitation (status: pending, hashed_token)
    InvitationService->>EventBus: publish(InvitationSent)
    EventBus->>Email: Async Send Magic Link
    InvitationService-->>Router: Return Invite ID
    Router-->>Admin: 200 OK
```

### Permission Check Flow
```mermaid
sequenceDiagram
    participant Client
    participant Middleware
    participant Router
    participant Service
    participant AuthService
    participant Repository
    participant DB

    Client->>Middleware: Request with JWT
    Middleware->>Middleware: Verify JWT & extract user
    Middleware->>Router: Forward Request
    Router->>Service: Call execute(user, org_id)
    Service->>Repository: Get Membership & Org
    Repository->>DB: Fetch data
    DB-->>Repository: Data
    Repository-->>Service: Return Objects
    Service->>AuthService: build_context(user, org, membership)
    Service->>AuthService: authorize(context, "organization.update")
    AuthService-->>Service: Raises 403 if unauthorized, else Pass
    Service->>Repository: Perform Business Logic
    Repository->>DB: UPDATE organizations
    DB-->>Repository: OK
    Repository-->>Service: OK
    Service-->>Router: Updated Data
    Router-->>Client: 200 OK (Standard Envelope)
```

## 10. Sprint Backlog & Implementation Plan

**Epic 1: DB Schema, Repositories, & Constraints**
- Create migrations for 8 tables with `deleted_at` soft deletes.
- Add unique constraints (Slug, Memberships, Pending Invites).
- Implement abstract `Repository` interfaces (`OrganizationRepository`, etc.).

**Epic 2: Core Domain & Authorization Engine**
- Implement `AuthorizationContext` and `AuthorizationService`.
- Establish standard API Envelope formatting and Error classes.
- Setup in-process Domain Event Bus.

**Epic 3: Organization Management**
- Implement `OrganizationService`.
- Expose `/api/v1/organizations` with `Idempotency-Key` support.

**Epic 4: Invitation & Membership System**
- Implement `InvitationService` (hashing tokens, expiry, revocation).
- Implement Rate Limiting.
- Ensure Domain Events are fired upon acceptance/revocation.

**Epic 5: Audit Log Engine**
- Hook Audit Logging into the Event Bus to capture `before` and `after` states globally.

> [!IMPORTANT]
> Please review the completely revised Design Package, incorporating Granular RBAC, Billing Admin, Repository interfaces, Domain Events, Rate Limiting, and Idempotency.
> - Once approved, I will begin implementing Epic 1 (DB Schema).
