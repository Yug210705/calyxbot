# Release & Rollback Runbook

## Pre-Release Checklist
- [ ] CI Pipeline is green (All tests passing).
- [ ] Security scans passed (`npm audit`, `pip audit`, `bandit`).
- [ ] Database migrations (`alembic upgrade head`) applied to staging/production successfully.
- [ ] Environment variables verified against `Environment-Matrix.md`.

## Rollback Procedure
If a critical production regression is detected:

### 1. Backend Rollback (Render)
1. Navigate to the Render Dashboard -> `calyx-backend` Web Service.
2. Go to the "Events" tab.
3. Locate the previously successful deployment.
4. Click **"Rollback to this deploy"**.
5. *Note: If a database migration was applied that is incompatible with the rollback code, you must first run `alembic downgrade -1` against the production database before rolling back the web service.*

### 2. Frontend Rollback (Vercel)
1. Navigate to the Vercel Dashboard -> Calyx Project.
2. Go to the "Deployments" tab.
3. Locate the previously successful production deployment.
4. Click the three dots (⋮) and select **"Assign Custom Domain"** or **"Promote to Production"** to instantly revert the production alias to the older build.

### 3. Incident Logging
1. Log the failure in the engineering incident channel.
2. Record the specific error and commit hash that caused the regression.
3. Postmortem required before next release attempt.
