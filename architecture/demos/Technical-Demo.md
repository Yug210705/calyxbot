# Technical Demo (30 Minutes)

## Objective
A deep dive for engineering leaders or technical co-founders to review the architecture, codebase health, and scalability of Calyx.

## Prerequisites
- IDE open (VS Code or Cursor).
- Local Postgres and Supabase instances running.
- Terminal open for running tests.

## Flow

### 1. Codebase Architecture (0:00 - 10:00)
- **Dependency Graph:** Open `architecture/dependency-graph.md`. Show the strict `Router -> Service -> Repository` acyclic flow.
- **Transactions:** Open `app/modules/organizations/services.py`. Demonstrate how the Service explicitly calls `session.commit()`, and how Repositories never commit. This prevents partial data insertion.
- **Events:** Open `app/shared/events.py`. Show the `InProcessEventBus`. Explain that the try-catch block ensures that if an audit log fails to write, it doesn't crash the organization creation.

### 2. Testing Strategy (10:00 - 20:00)
- **Mocked Boundaries:** Open `tests/conftest.py`. Show `FakeJWKSProvider`. Explain that no network requests happen during testing.
- **Run Unit Tests:** Run `pytest tests/unit/ -v`. Point out the sub-second execution time.
- **RBAC Matrix:** Open `tests/unit/test_rbac.py`. Show the exhaustive loop testing every role against every permission string. Run the test to prove it passes.

### 3. Load & Performance (20:00 - 25:00)
- **Locust Output:** Open `benchmark_results.json`. Show the P95 latency for domain operations.
- Explain the plan to migrate to K6 for CI/CD load testing once on Linux environments.
- **Observability:** Open `logging.py`. Highlight the `increment_counter` function and the context vars (`correlation_id`, `request_id`) attached to every structlog line.

### 4. Deployment & CI (25:00 - 30:00)
- **CI Pipeline:** Open `.github/workflows/ci.yml`. Walk through the matrix of Ruff, Black, Pytest, and Playwright.
- **Render/Vercel:** Briefly show `render.yaml` and `vercel.json`.
- Open the live production URLs to prove the system works under real-world internet constraints.
