# Entity-Relationship Diagram

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [Database Design](../system/database-design.md)

---

```mermaid
erDiagram
    organizations ||--o{ memberships : "has members"
    organizations ||--o{ workspaces : "contains"
    organizations ||--o{ knowledge_sources : "connects"
    organizations ||--o{ audit_logs : "records"
    organizations ||--o{ invitations : "sends"

    users ||--o{ memberships : "belongs to orgs"
    users ||--o{ documents : "creates"
    users ||--o{ memories : "generates"
    users ||--o{ conversations : "initiates"
    users ||--o{ audit_logs : "triggers"

    memberships }o--|| roles : "has role"

    roles ||--o{ role_permissions : "grants"
    permissions ||--o{ role_permissions : "assigned via"

    workspaces ||--o{ workspace_members : "has members"
    workspaces ||--o{ documents : "contains"

    documents ||--o{ memories : "produces"

    knowledge_sources ||--o{ documents : "imports to"

    conversations ||--o{ conversation_messages : "contains"
    conversations }o--o{ memories : "references"

    memories ||--o{ embeddings : "vectorized as"
    memories ||--o{ memory_tags : "tagged with"

    tags ||--o{ memory_tags : "applied to"

    organizations {
        uuid id PK
        string name
        string slug
        jsonb settings
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    users {
        uuid id PK
        string email
        string full_name
        string avatar_url
        timestamp created_at
        timestamp updated_at
    }

    memberships {
        uuid id PK
        uuid user_id FK
        uuid org_id FK
        uuid role_id FK
        string status
        timestamp joined_at
        timestamp deactivated_at
    }

    roles {
        uuid id PK
        uuid org_id FK
        string name
        string description
        boolean is_system
        int hierarchy_level
        timestamp created_at
    }

    permissions {
        uuid id PK
        string resource
        string action
        string description
    }

    role_permissions {
        uuid role_id FK
        uuid permission_id FK
    }

    invitations {
        uuid id PK
        uuid org_id FK
        uuid invited_by FK
        string email
        uuid role_id FK
        string status
        timestamp expires_at
        timestamp created_at
    }

    workspaces {
        uuid id PK
        uuid org_id FK
        string name
        string description
        string visibility
        uuid created_by FK
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    workspace_members {
        uuid workspace_id FK
        uuid user_id FK
        string role
        timestamp joined_at
    }

    documents {
        uuid id PK
        uuid org_id FK
        uuid workspace_id FK
        uuid created_by FK
        string title
        text content
        string content_type
        string status
        string visibility
        jsonb metadata
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    knowledge_sources {
        uuid id PK
        uuid org_id FK
        string source_type
        jsonb config
        string status
        uuid created_by FK
        timestamp last_synced_at
        timestamp created_at
    }

    conversations {
        uuid id PK
        uuid org_id FK
        uuid user_id FK
        string title
        jsonb context
        timestamp created_at
        timestamp updated_at
    }

    conversation_messages {
        uuid id PK
        uuid conversation_id FK
        string role
        text content
        jsonb metadata
        timestamp created_at
    }

    memories {
        uuid id PK
        uuid org_id FK
        string source_type
        uuid source_id
        text content
        string memory_type
        jsonb metadata
        uuid created_by FK
        string visibility
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }

    embeddings {
        uuid id PK
        uuid memory_id FK
        uuid org_id FK
        vector embedding
        string model
        timestamp created_at
    }

    tags {
        uuid id PK
        uuid org_id FK
        string name
        string color
    }

    memory_tags {
        uuid memory_id FK
        uuid tag_id FK
    }

    audit_logs {
        uuid id PK
        uuid org_id FK
        uuid user_id FK
        string action
        string resource_type
        uuid resource_id
        jsonb changes
        string ip_address
        string user_agent
        timestamp created_at
    }
```
