# Sprint 2 Retrospective: Enterprise Foundation

## What Went Well
- **Technical Wins:** Transitioned from a single tenant MVP to a multi-tenant enterprise system with a solid RBAC matrix.
- **Architecture Wins:** Event-driven architecture with `InProcessEventBus` decoupling business logic from audit logging. Repositories no longer own transactions.
- **Testing Wins:** Exhaustive RBAC matrix testing added. Test suites made 100% network-independent with the `FakeJWKSProvider`.
- **Developer Experience:** Mocks and fixtures are robust and allow offline unit testing.

## What Went Wrong
- **Auth Network Dependency Bug:** `security.py` instantiated a live Supabase JWKS client at the module level.
  - **Cause:** Overlooking network boundaries during module loading.
  - **Detection:** Tests were failing due to Supabase rate-limiting / network timeouts.
  - **Resolution:** Introduced `JWKSProvider` abstraction (ADR-021).
  - **Prevention:** Ban live HTTP clients at module level.
- **Transaction Ownership Bug:** Repositories were committing sessions (`session.commit()`).
  - **Cause:** Misunderstanding of Unit of Work pattern in initial repository implementation.
  - **Detection:** Discovered during architectural review. Services lacked atomic guarantees across multiple repo calls.
  - **Resolution:** Removed `.commit()` from repositories. Services and routers now own the transaction explicitly.
  - **Prevention:** Enforce architectural linting / rules that Repositories must not import or call `session.commit()`.

## Root Cause Analysis
- **Auth Test Flakiness:** Tests were depending on live Supabase endpoints for JWT verification. This was fixed by ADR-021.
- **Transaction Atomicity Risk:** Since `OrganizationRepository` committed before `MembershipRepository`, a failure in the latter would leave an orphaned Organization. This is solved by service-owned transactions.

## Architecture Changes
- **ADR-021:** Authentication Provider Abstraction introduced to decouple JWT signature verification from network access in tests.
- **Dependency Inversion in Event Bus:** Handlers are now strictly isolated and wrapped in try-catch to prevent domain transaction rollbacks on listener failure.

## Technical Debt
- **Priority: Medium** - Explicit Unit of Work (`uow`) pattern implementation is pending. Currently relying on the injected `AsyncSession` to track the transaction.
- **Priority: Low** - Permission versioning (e.g., `v1` vs `v2` permission sets).
- **Priority: Low** - Complete mapping of role strings to relational tables using Alembic seeds for all environments.

## Lessons Learned
- Enterprise boundaries require explicit abstractions for external services (Auth, EventBus).
- Mocks must cover all I/O to guarantee deterministic local development.

## Sprint Metrics
- **Story Completion:** 100% (Organizations, Memberships, RBAC, Invitations, Audit Logs)
- **Defect Count:** 2 critical (resolved during stabilization)
- **Test Count:** 10+ new tests.
- **Coverage:** High across domain services.
- **Average Latency:** Benchmarks setup. Baseline <50ms for domain operations.
- **Critical Bugs:** 0 open.
