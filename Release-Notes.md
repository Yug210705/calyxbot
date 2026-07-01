# Release Notes - v1.0.0

We are thrilled to announce the v1.0.0 release of the Calyx application, marking our very first production deployment! 

## What's New
- **Production Infrastructure**: The frontend is now live on Vercel and the backend is live on Render.
- **Supabase Integration**: Migrated from local SQLite to a robust, scalable Supabase PostgreSQL database.
- **Transaction Pooling**: Configured advanced connection pooling for seamless scale-down-to-zero support in our serverless environments.
- **Authentication Resilience**: Full end-to-end support for Supabase ES256 asymmetric JWT tokens in the FastAPI backend, ensuring secure and scalable authorization.

## Known Issues
- Very rapid successive signups (like those executed during stress tests) might occasionally trigger rate limit warnings on the UI. This is a limit of the free tier and does not affect normal usage.

## Coming Up
In Sprint 3, we will focus on **Organizations**, adding multi-tenant support for creating organizations and inviting team members.
