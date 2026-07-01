# Calyx Testing Strategy

## Overview
Calyx ensures enterprise-grade reliability by strictly adhering to the test pyramid. We prioritize deterministic, fast-executing offline tests over flaky end-to-end (E2E) tests.

## Test Pyramid

1. **Unit Tests (Backend & Frontend)**
   - Must run completely offline. No network requests are allowed (enforced by `FakeJWKSProvider` and mocked repositories).
   - Domain logic and services are tested in isolation using Pytest and AsyncMock.
   - Required to pass 100% locally and in CI.

2. **Integration Tests**
   - Test the interaction between the Router, Service, and Repository layers.
   - Use in-memory SQLite (or a disposable Postgres container) to test actual SQL queries.
   - Transaction boundaries must be verified.

3. **E2E Tests (Playwright)**
   - Test the critical user flows (Signup, Login, Create Organization, Invite Members).
   - Must not contain race conditions. All wait statements must be deterministic (wait for network idle / selector).
   - Executed against a staging environment or a fully spun-up local stack in CI.

## RBAC Exhaustive Verification
- The RBAC matrix is exhaustively tested in `test_rbac.py`. Every combination of Role and Permission is mathematically verified against the source of truth matrix.

## Observability & Metrics
- Tests ensure that metrics counters are correctly emitted upon domain actions.

## Anti-Patterns Ban List
- NO `time.sleep()` in Playwright tests.
- NO `mock_session.commit()` assertions in repositories (repositories must not own transactions).
- NO external HTTP requests during unit tests (e.g., Supabase JWKS fetching).
