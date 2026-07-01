# Architecture Dependency Graph

This document proves that Calyx follows a strict acyclic dependency flow, and that business logic is properly isolated.

## Flow Rules
1. **Router Layer** handles HTTP requests, dependencies injection, transaction boundaries, and returns DTOs.
2. **Service Layer** handles business logic, domain events, authorization checks, and orchestrates repositories. Services own the transaction (`session.commit()`).
3. **Repository Layer** ONLY performs persistence. They do not contain business logic, and they do not own transactions.
4. **Database Layer** manages schema, constraints, and data.

## Mermaid Graph

```mermaid
graph TD
    %% Routers (Entrypoints)
    AuthRouter["Auth Router"]
    OrgRouter["Organization Router"]
    InvRouter["Invitation Router"]
    
    %% Services (Business Logic)
    OrgService["Organization Service"]
    MemService["Membership Service"]
    InvService["Invitation Service"]
    AuditService["Audit Log Service"]
    
    %% Repositories (Persistence)
    OrgRepo["Organization Repository"]
    MemRepo["Membership Repository"]
    RoleRepo["Role Repository"]
    InvRepo["Invitation Repository"]
    AuditRepo["Audit Log Repository"]
    
    %% Events
    EventBus["Event Bus (InProcess)"]

    %% Dependencies
    AuthRouter -->|Direct CRUD| Database
    
    OrgRouter --> OrgService
    OrgRouter --> MemService
    
    InvRouter --> InvService
    
    OrgService --> OrgRepo
    OrgService --> MemRepo
    OrgService --> RoleRepo
    OrgService --> EventBus
    
    MemService --> MemRepo
    MemService --> RoleRepo
    
    InvService --> InvRepo
    InvService --> MemRepo
    InvService --> RoleRepo
    InvService --> EventBus
    
    EventBus -->|Async Dispatch| AuditService
    AuditService --> AuditRepo
    
    OrgRepo --> Database
    MemRepo --> Database
    RoleRepo --> Database
    InvRepo --> Database
    AuditRepo --> Database
```

As demonstrated, the architecture is strictly unidirectional.
