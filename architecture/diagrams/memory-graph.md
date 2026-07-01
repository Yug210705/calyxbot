# Memory Graph Diagrams

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [Memory Engine](../system/memory-engine.md)

---

```mermaid
graph BT
    D["Raw Data"] --> I["Information"]
    I --> K["Knowledge"]
    K --> M["Memory"]
    M --> W["Wisdom"]

    style D fill:#1e293b,stroke:#475569,color:#94a3b8
    style I fill:#1e293b,stroke:#475569,color:#94a3b8
    style K fill:#1e293b,stroke:#3b82f6,color:#93c5fd
    style M fill:#1e293b,stroke:#8b5cf6,color:#c4b5fd
    style W fill:#1e293b,stroke:#475569,color:#94a3b8
```

```mermaid
graph TB
    M["Memory Unit"]
    M --> Content["Content Facet<br/>What is known"]
    M --> Provenance["Provenance Facet<br/>Where it came from"]
    M --> Temporal["Temporal Facet<br/>When it was/is true"]
    M --> Confidence["Confidence Facet<br/>How reliable it is"]
    M --> Graph["Graph Facet<br/>What it connects to"]

    style M fill:#1e1b4b,stroke:#6366f1,color:#c7d2fe
    style Content fill:#1e293b,stroke:#3b82f6,color:#93c5fd
    style Provenance fill:#1e293b,stroke:#10b981,color:#6ee7b7
    style Temporal fill:#1e293b,stroke:#f59e0b,color:#fcd34d
    style Confidence fill:#1e293b,stroke:#ef4444,color:#fca5a5
    style Graph fill:#1e293b,stroke:#8b5cf6,color:#c4b5fd
```

```mermaid
stateDiagram-v2
    [*] --> Draft : Create
    Draft --> Active : Publish
    Draft --> Discarded : Discard

    Active --> Active : Update (new version)
    Active --> Verified : Human verification
    Verified --> Active : Modification invalidates verification
    Active --> Stale : Decay threshold exceeded
    Verified --> Stale : Decay threshold exceeded
    Stale --> Active : Refresh / re-verify
    Stale --> Deprecated : Confirm obsolescence
    Active --> Deprecated : Explicitly superseded
    Verified --> Deprecated : Explicitly superseded
    Deprecated --> Archived : Retention period ends
    Archived --> [*] : Hard delete (compliance only)

    Discarded --> [*] : Purge
```

```mermaid
graph LR
    subgraph "Source Categories"
        direction TB
        D["Authored Content<br/>Docs, Wikis, READMEs"]
        C["Communication<br/>Slack, Email, Chat"]
        T["Tooling<br/>GitHub, Jira, Linear"]
        V["Verbal<br/>Meetings, Calls"]
        M["Manual<br/>Direct Input"]
    end

    subgraph "Ingestion Layer"
        A["Source Adapter"]
        E["Knowledge Extractor"]
        N["Normalizer"]
    end

    subgraph "Memory Layer"
        Mem["Memory Unit"]
    end

    D --> A
    C --> A
    T --> A
    V --> A
    M --> N

    A --> E
    E --> N
    N --> Mem
```

```mermaid
graph TB
    Q["User Query"]
    Q --> R["Retrieval Layer"]
    R --> S1["Semantic Search<br/>(embedding similarity)"]
    R --> S2["Graph Traversal<br/>(relationship-based)"]
    R --> S3["Keyword Search<br/>(exact match fallback)"]

    S1 --> C["Candidate Memories"]
    S2 --> C
    S3 --> C

    C --> F["Evidence Filter"]
    F --> |"Remove stale, low-confidence,<br/>out-of-scope"| E["Evidence Set"]

    E --> Rank["Evidence Ranker"]
    Rank --> |"Sort by composite score:<br/>relevance × confidence × freshness"| Final["Ranked Evidence Chain"]

    Final --> Gen["Answer Generator"]
    Gen --> A["Answer + Citations"]
```

```mermaid
graph TB
    subgraph "Decision Lifecycle"
        direction TB
        Problem["Problem<br/>What prompted the decision?"]
        Discussion["Discussion<br/>Where was it debated?"]
        Alternatives["Alternatives<br/>What options were considered?"]
        Decision["Decision<br/>What was chosen and why?"]
        Implementation["Implementation<br/>How was it executed?"]
        Outcome["Outcome<br/>What happened?"]
        Revision["Revision<br/>Was it changed later?"]
        Rollback["Rollback<br/>Was it reversed?"]
    end

    Problem --> Discussion
    Discussion --> Alternatives
    Alternatives --> Decision
    Decision --> Implementation
    Implementation --> Outcome
    Outcome --> Revision
    Outcome --> Rollback
    Revision --> Decision
```

```mermaid
graph LR
    U["User Interaction"] --> E["Event Collector"]
    E --> A["Analytics Pipeline"]
    A --> M["Metrics Store"]
    M --> D["Dashboard<br/>(Search Quality, Gap Analysis)"]
    M --> T["Tuning Recommendations"]
    T --> R["Human Review"]
    R --> S["System Parameters"]
    S --> |"Updated weights,<br/>thresholds"| Sys["Retrieval Engine"]
```

```mermaid
graph TB
    subgraph "Agent Layer (Future)"
        A1["Knowledge Assistant<br/>Answers questions"]
        A2["Onboarding Agent<br/>Guides new employees"]
        A3["Decay Detector Agent<br/>Proactively identifies stale knowledge"]
        A4["Decision Analyst<br/>Reconstructs decision history"]
        A5["Gap Finder<br/>Identifies undocumented areas"]
    end

    subgraph "Memory Platform (Current Architecture)"
        API["Memory API"]
        Search["Search Engine"]
        Graph["Memory Graph"]
        Evidence["Evidence Engine"]
        Confidence["Confidence Engine"]
    end

    A1 --> API
    A2 --> API
    A3 --> API
    A4 --> API
    A5 --> API

    API --> Search
    API --> Graph
    API --> Evidence
    API --> Confidence
```
