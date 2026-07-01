# Technical Debt Report

## Postponed Items (Intentional)

### High Priority
1. **Explicit Unit of Work (UoW):** Currently, services accept the `AsyncSession` directly and call `.commit()`. To fully isolate services from SQLAlchemy dependencies, we should introduce an explicit Unit of Work context manager.
2. **Playwright CI Flakiness:** The UI tests occasionally fail when network responses are delayed. We need to introduce API response mocking within Playwright to guarantee deterministic offline frontend tests.

### Medium Priority
1. **Prometheus Exporter Integration:** We are currently emitting structured logs for metrics. A Prometheus exporter needs to be built to scrape these logs or we need to integrate a statsd client.
2. **Idempotency Keys:** The `create_organization` endpoint accepts an idempotency key header, but does not actually persist the key to Redis to prevent double execution. It currently relies purely on database unique constraints (slug uniqueness).

### Low Priority
1. **Permission Set Versioning:** As requested by the CTO, we should eventually implement `v1`, `v2` permission sets for backward compatibility when scopes change.
2. **Postgres Read Replicas:** We currently query the primary database for both reads and writes.
