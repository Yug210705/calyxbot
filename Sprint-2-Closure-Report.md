# Sprint 2 Closure Report

## Overview
Sprint 2 focused on deploying the Calyx application (Frontend and Backend) to production environments using Vercel and Render respectively. We also migrated from local SQLite to a managed Supabase PostgreSQL database, configured the application to use a Transaction Pooler for robust connection management, and ran E2E Playwright tests against the live production environment.

## Goals Achieved
- **Database Migration**: Successfully migrated the backend from SQLite to a live Supabase PostgreSQL instance.
- **Connection Pooling**: Reconfigured `DATABASE_URL` to use Supabase's Transaction Pooler (port 6543) and disabled SQLAlchemy's internal connection pooling (`poolclass=NullPool`) for maximum stability in serverless/PaaS environments.
- **Backend Deployment (Render)**:
  - Created a `render.yaml` configuration for Infrastructure as Code.
  - Successfully deployed the FastAPI backend to Render.
  - Resolved build failures related to `requirements.txt` location and default build directory.
  - Resolved `cryptography` dependency issue that caused ES256 Supabase JWT verification to fail.
- **Frontend Deployment (Vercel)**:
  - Deployed the Next.js frontend to Vercel.
  - Configured `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_SUPABASE_URL` to point to production infrastructure.
- **Production Verification**:
  - Executed the full Playwright E2E suite against the production endpoints.
  - Fixed test isolation issues that caused `IntegrityError` failures across test workers.
  - Verified authentication, JWT signature validation (ES256), database writes, and API latency in the live environment.

## Open Issues / Technical Debt
- **Playwright Rate Limiting**: The free tier of Supabase may occasionally throttle signups when running concurrent Playwright workers, resulting in transient test failures. This can be mitigated by configuring test users in advance or upgrading the Supabase plan.
- **Email Confirmation**: Email confirmation is currently handled automatically by backend auto-confirm scripts in E2E tests, but real users will need a properly configured SMTP setup for production invites.

## Sign-off
The production deployment is fully functional and all core capabilities (Auth, Security, Unified API responses) operate exactly as they did in the local development environment. Sprint 2 is officially closed.
