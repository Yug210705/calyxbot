<div align="center">
  <img src="https://raw.githubusercontent.com/Yug210705/calyxbot/main/docs/assets/logo.png" alt="Calyx Logo" width="120" height="120" />
  <h1>Calyx</h1>
  <p><strong>The Enterprise-Grade Organizational Brain</strong></p>
  
  <p>
    <a href="https://github.com/Yug210705/calyxbot/actions"><img src="https://img.shields.io/github/actions/workflow/status/Yug210705/calyxbot/ci.yml?branch=main" alt="CI Status" /></a>
    <a href="https://github.com/Yug210705/calyxbot/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" /></a>
    <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12" /></a>
    <a href="https://nextjs.org/"><img src="https://img.shields.io/badge/next.js-14-black.svg" alt="Next.js" /></a>
  </p>
</div>

---

## 📖 Overview

**Calyx** is a robust, multi-tenant B2B platform designed to act as an organizational knowledge engine. Built from the ground up with enterprise-grade architecture, strict Role-Based Access Control (RBAC), and deterministic audit logging, Calyx connects your company's dispersed knowledge silos securely.

This repository serves as the foundation (Sprint 2) before we integrate AI ingestion pipelines and Large Language Models.

---

## ✨ Features

- **Robust Multi-Tenancy:** Strict isolation of data at the organization level via slugs and aggregate boundaries.
- **Granular RBAC:** Mathematical validation of permissions instead of hardcoded roles.
- **Immutable Audit Logging:** Every action (e.g., invitation sent, org created) is immutably logged with `correlation_id` tracking.
- **Event-Driven Resilience:** Core domain transactions are decoupled from background tasks via `InProcessEventBus`.
- **Fault-Tolerant Tests:** 100% offline unit tests with injected `FakeJWKSProvider`, eliminating test flakiness.

---

## 🏗 Architecture

Calyx uses a strictly layered **Modular Monolith** architecture:

- **Frontend:** Next.js (React), Tailwind CSS
- **Backend:** FastAPI (Python), SQLAlchemy Async
- **Database & Auth:** PostgreSQL + Supabase (GoTrue)

> See the full [Dependency Graph](./architecture/dependency-graph.md) and [Architecture Health Report](./architecture/Architecture-Health-Report.md) for more details.

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.12+](https://www.python.org/)
- [Node.js 20+](https://nodejs.org/)
- [Supabase CLI](https://supabase.com/docs/guides/cli) (or a hosted Supabase project)

### 1. Clone the Repository

```bash
git clone https://github.com/Yug210705/calyxbot.git
cd calyxbot
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows

pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```
Ensure your `.env` is populated with your Supabase credentials:
```ini
SUPABASE_URL="http://localhost:54321"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
SUPABASE_JWT_SECRET="your-jwt-secret"
DATABASE_URL="postgresql://postgres:postgres@localhost:54322/postgres"
```

Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install

# Copy environment variables
cp .env.example .env.local
```
Start the Next.js development server:
```bash
npm run dev
```

---

## 🧪 Testing Strategy

Our tests adhere to strict deterministic rules (no `time.sleep()`, no live network requests in unit tests).

**Run Backend Unit Tests:**
```bash
cd backend
pytest tests/unit -v --cov=app
```

**Run End-to-End Tests:**
```bash
cd frontend
npx playwright test
```

> Read the comprehensive [Testing Strategy](./architecture/Testing-Strategy.md).

---

## 📦 Deployment

Calyx is deployment-ready for **Render** (Backend) and **Vercel** (Frontend).
- **Backend:** Refer to `backend/render.yaml`
- **Frontend:** Refer to `frontend/vercel.json`

For detailed production guidelines, see the [Deployment Guide](./architecture/deployment/Deployment-Guide.md) and [Release Runbook](./architecture/deployment/Release-Runbook.md).

---

## 📚 Documentation & Runbooks

- [Sprint 2 Retrospective](./architecture/retrospectives/Sprint-2-Retrospective.md)
- [Technical Debt Report](./architecture/Technical-Debt.md)
- [Demo Scripts](./architecture/demos/)

---

## 🛡 Security

If you discover a security vulnerability, please do not disclose it publicly. Review our [Security Guidelines](SECURITY.md) and report responsibly.

---

<div align="center">
  <i>Built with precision. Ready for the enterprise.</i>
</div>
