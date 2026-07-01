# Product Vision

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [PRD](../product/prd.md)

---

## 1.1 What Is Calyx?

Calyx is an Enterprise Memory Operating System. It captures, preserves, and surfaces organizational knowledge — decisions, workflows, client history, technical context, and institutional memory — so that when employees leave, their knowledge stays.

Calyx is **not** a chatbot, not a RAG wrapper, and not an LLM shell. It is a structured memory platform with semantic retrieval capabilities.

## 1.2 MVP Inclusions

The MVP delivers the minimum viable surface to prove the core value proposition: *"Your organization's knowledge survives employee turnover."*

| Area | What Ships |
|---|---|
| **Authentication** | Email/password signup, Google OAuth, email verification, password reset, session management |
| **Multi-tenancy** | Organization creation, invitation flow, role assignment, tenant isolation |
| **RBAC** | Five system roles (Super Admin, Org Admin, Manager, Employee, Viewer) with enforced permissions |
| **Knowledge Capture** | Manual document creation (rich text), structured memory extraction, tagging, categorization |
| **Knowledge Organization** | Workspaces, folders, document hierarchy within an organization |
| **Semantic Search** | Vector-based search across an organization's knowledge base using pgvector |
| **Knowledge Retrieval** | Conversational interface to query organizational memory (not a chatbot — a retrieval surface) |
| **Audit Trail** | Immutable log of all create, update, delete, and access operations |
| **User Management** | Invite members, assign roles, deactivate accounts, transfer ownership |
| **Dashboard** | Organization-level overview of knowledge health, coverage gaps, and activity |

## 1.3 MVP Exclusions

These are **intentionally deferred** — not forgotten. Each exclusion has a rationale.

| Excluded | Rationale |
|---|---|
| **Third-party integrations** (Slack, GitHub, Google Drive, Jira, MS 365, Zoom) | Requires stable core platform first. Integration adapter architecture is designed in, but connectors ship post-MVP. |
| **AI Agents** | Depends on mature memory graph and retrieval quality. Foundation is laid; agents are a future layer. |
| **Meeting transcript ingestion** | Requires integration with Zoom/Meet/Teams APIs. Deferred to integration phase. |
| **Custom roles & fine-grained permissions** | System roles cover MVP use cases. Custom role editor adds UX complexity. |
| **Billing & subscription management** | MVP targets design partners and pilots — no payment flow needed yet. |
| **Mobile applications** | Web-first. Responsive design covers mobile access. |
| **Self-hosted / on-premise deployment** | Cloud-only for MVP. On-prem is an enterprise tier feature. |
| **SSO (SAML/OIDC enterprise IdP)** | Important for enterprise sales but not for proving the core product. Designed for, deferred. |
| **Data export / portability** | Required for enterprise trust but deferred to post-MVP. API-first design enables this. |
| **Webhooks & external event system** | Internal event bus is designed in; external webhooks ship later. |
| **Multi-language / i18n** | English-only for MVP. |

## 1.4 MVP Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Knowledge capture rate** | ≥ 50 documents per org within 30 days of onboarding | Database query |
| **Search relevance** | ≥ 80% of top-5 results rated relevant by users | In-app feedback widget |
| **Time to first value** | ≤ 10 minutes from signup to first knowledge query | Funnel analytics |
| **Retention** | ≥ 60% weekly active rate among invited members | Auth session data |
| **Data integrity** | Zero cross-tenant data leaks | Automated security tests + audit log review |
| **Uptime** | ≥ 99.5% | External monitoring |

---
