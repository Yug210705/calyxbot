# Sprint 2 Final Verification & Sprint 3 Planning

This plan outlines how we will execute the final 8-point Verification Checklist for Sprint 2 and formally accept the recommendation for Sprint 3 (Connectors + Memory Ingestion).

## User Review Required
> [!WARNING]
> **Deployment Credentials Needed**
> Item 7 requires deploying the Backend and Frontend to a free tier (e.g., Vercel, Render) and configuring Supabase. To do this automatically, I will need access to deployment credentials/CLIs (e.g., `vercel login`, `render login`). If you prefer, I can generate the deployment configuration files (e.g., `render.yaml`, `vercel.json`) and we can deploy manually, after which I can run the Playwright suite against the provided URLs. **Please confirm how you would like to handle the live deployment step.**

## Open Questions
- **Load Testing Tool:** I plan to use `locust` for load testing the backend (100 concurrent users). Let me know if you prefer a different tool like `k6`.
- **Sprint 3 Scope:** You outlined Connectors and Memory Ingestion as Sprint 3. I will set up the Sprint 3 Backlog and Architecture artifacts for this once the verification passes. Does this sound correct?

## Proposed Changes

### 1. Verification Scripts & Tooling
I will create a suite of verification scripts under the `scripts/verify/` directory to automate the checklist:
- `generate_coverage.py`: Runs pytest with `--cov` and outputs the exact percentage metrics.
- `verify_architecture.py`: Uses AST parsing to trace `router -> service -> repo` imports and explicitly fails if any circular dependencies or layer-skipping occurs.
- `verify_api_contract.py`: Runs automated requests against all endpoints to assert the `{ success, data, meta }` envelope and exact error schemas.
- `run_security_scan.sh`: Executes `bandit -r backend/`, `npm audit`, and `pip-audit`.
- `load_test.py`: A Locust script defining the concurrent user flow (Signup -> Create Org -> Invite) and capturing P95/P99 latency and throughput.
- `measure_cold_start.py`: Profiles memory consumption and connection counts during FastAPI startup.

### 2. Demo Scripts Documentation
I will generate:
- `architecture/demos/Investor-Demo.md` (3-minute flow)
- `architecture/demos/Founder-Demo.md` (10-minute flow)
- `architecture/demos/Technical-Demo.md` (30-minute click-by-click flow)

### 3. Deployment Configuration (Pending Feedback)
- `backend/render.yaml` or Dockerfile for free-tier backend hosting.
- `frontend/vercel.json` for Next.js frontend deployment.
- A script to execute the existing Playwright E2E suite against `BASE_URL=https://<deployed-url>`.

## Verification Plan

### Automated Execution
Once approved, I will run the verification pipeline:
1. Generate and log Coverage.
2. Run Architecture Linter.
3. Assert API Contracts.
4. Run Security Audits.
5. Execute Load Tests locally.
6. Generate Demo Scripts.

If all gates pass (and deployment strategy is aligned), I will formally declare Sprint 2 complete and transition to Sprint 3: **Connectors + Memory Ingestion Foundation**.
