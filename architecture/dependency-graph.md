# Dependency Graph

This document illustrates the dependencies between Calyx Backend modules, external services, databases, and message queues.

```mermaid
graph TD
    %% Core Modules
    Auth[Auth Module]
    Orgs[Organizations Module]
    Members[Members Module]
    Audit[Audit Module]

    %% Dependencies
    DB[(PostgreSQL / Supabase)]
    VectorDB[(Vector DB - Future)]
    Queue[Task Queue - Future]
    EventBus[EventBus]
    Redis[(Redis - Future)]

    %% Connections
    Auth --> DB
    Orgs --> DB
    Members --> DB
    Audit --> DB

    Auth --> EventBus
    Orgs --> EventBus
    Members --> EventBus

    EventBus -.-> Queue
    Queue -.-> VectorDB
    EventBus -.-> Redis

    %% Module inter-dependencies
    Members --> Orgs : "Requires Org ID"
    Auth --> Members : "User registration creates Membership (via EventBus)"
    Orgs --> Audit : "Organization actions logged"
```

## Cross-Feature Leakage Check
- **Cyclic Imports**: None. All dependencies flow downwards (Router -> Service -> Repository).
- **Hidden Dependencies**: None. Shared state is entirely handled by `app.core`.
- **Cross-feature leakage**: Strictly prevented. Domain models do not reference cross-domain objects without `EventBus` pub-sub.
