# Sprint 1 Backlog

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [PRD](../product/prd.md)

---

# Sprint 1 Backlog — Calyx v1.0

**Sprint Goal:** Establish the complete project foundation — backend, frontend, authentication, organization management, and RBAC — so that feature development can begin in Sprint 2 with zero infrastructure debt.

**Sprint Duration:** 2 weeks
**Total Tickets:** 62
**Start Date:** TBD (upon approval)

---

# Epic 1: Backend Foundation (BF)

> **Epic Goal:** A fully configured FastAPI backend with production-grade infrastructure — configuration, database, logging, error handling, middleware, and standard response patterns.

---

### BF-001: Initialize FastAPI Project

**Title:** Initialize FastAPI project with modular monolith folder structure

**Description:**
Create the FastAPI project with the folder structure defined in the Design Review (§10.1). Set up `pyproject.toml` with dependencies, configure `uvicorn` as the ASGI server, and create the app factory in `main.py`. The app factory should register routers, middleware, and exception handlers.

**Business Value:** Every backend ticket depends on this. No backend work can proceed without a runnable project skeleton.

**Acceptance Criteria:**
- [ ] `pyproject.toml` exists with FastAPI, uvicorn, pydantic, and python-dotenv as dependencies
- [ ] `app/main.py` creates a FastAPI app instance with title, version, and description
- [ ] `app/modules/` directory exists with placeholder `__init__.py` for each module (auth, organizations, members, workspaces, documents, memories, search, conversations, audit)
- [ ] `app/core/` directory exists with placeholder files (config, security, exceptions, middleware, logging, dependencies)
- [ ] `app/shared/` directory exists with placeholder files (pagination, response, validators)
- [ ] `app/integrations/` directory exists with `base.py` placeholder
- [ ] Running `uvicorn app.main:app --reload` starts the server on port 8000
- [ ] `GET /` returns `{"status": "ok", "service": "calyx-api", "version": "0.1.0"}`

**Dependencies:** None

**Complexity:** S

**Priority:** P0 — Critical Path

**Definition of Done:** Server starts, root endpoint responds, folder structure matches the approved architecture.

---

### BF-002: Configuration Management

**Title:** Implement Pydantic BaseSettings for environment configuration

**Description:**
Create `app/core/config.py` with a `Settings` class extending Pydantic `BaseSettings`. All environment variables (Supabase URL, keys, database URL, app environment, log level, CORS origins) must be loaded from environment variables with sensible defaults for development. Create `.env.example` with all required variables documented.

**Business Value:** Centralized, type-safe configuration prevents misconfiguration bugs and makes deployment to staging/production reliable.

**Acceptance Criteria:**
- [ ] `Settings` class loads all required env vars with type validation
- [ ] Missing required vars raise a clear error at startup (not at request time)
- [ ] `.env.example` documents every variable with comments
- [ ] `.env` is in `.gitignore`
- [ ] `get_settings()` dependency function provides cached settings instance
- [ ] `APP_ENV` supports `development`, `staging`, `production` with behavioral differences (e.g., debug mode)

**Dependencies:** BF-001

**Complexity:** S

**Priority:** P0

**Definition of Done:** App starts with valid `.env`, fails with clear error if required vars are missing.

---

### BF-003: Database Connection and Session Management

**Title:** Configure async database connection with session lifecycle

**Description:**
Set up async database connectivity using `asyncpg` and `SQLAlchemy` (async mode) or the Supabase Python client. Create a `get_db()` dependency that provides a database session per request. Ensure sessions are committed on success and rolled back on failure. Connection pooling should be configured appropriately.

**Business Value:** Every data operation depends on a reliable database connection. Session-per-request with automatic cleanup prevents connection leaks.

**Acceptance Criteria:**
- [ ] `get_db()` FastAPI dependency yields a usable database session
- [ ] Session commits on successful request completion
- [ ] Session rolls back on exception
- [ ] Connection pool size is configurable via environment variables
- [ ] Database connectivity is verified at startup (fail-fast if DB is unreachable)
- [ ] Connection string is loaded from `Settings`, never hardcoded

**Dependencies:** BF-001, BF-002

**Complexity:** M

**Priority:** P0

**Definition of Done:** Database session can be injected into a route handler and used to execute a simple query.

---

### BF-004: Custom Exception Hierarchy

**Title:** Define the Calyx exception class hierarchy

**Description:**
Create `app/core/exceptions.py` with the exception hierarchy defined in the Design Review (§10.9): `CalyxException` base class, `AuthenticationError` (401), `AuthorizationError` (403), `NotFoundError` (404), `ConflictError` (409), `ValidationError` (422), `RateLimitError` (429), `IntegrationError` (502). Each exception should carry an error code, a user-safe message, and optional details.

**Business Value:** Consistent, typed exceptions ensure every error path produces a predictable, well-formatted response. No raw 500 errors leak to clients.

**Acceptance Criteria:**
- [ ] `CalyxException` base class with `status_code`, `error_code`, `message`, `details` attributes
- [ ] Subclasses for each HTTP error type map to correct status codes
- [ ] Each exception can be instantiated with a custom message and optional details list
- [ ] Error codes are uppercase snake_case strings (e.g., `DOCUMENT_NOT_FOUND`)
- [ ] Exceptions are importable from `app.core.exceptions`

**Dependencies:** BF-001

**Complexity:** S

**Priority:** P0

**Definition of Done:** All exception classes exist, are importable, and carry structured error data.

---

### BF-005: Global Exception Handler

**Title:** Register global exception handlers for structured error responses

**Description:**
Create exception handlers in `app/core/middleware.py` (or a dedicated `exception_handlers.py`) that catch `CalyxException` subclasses, Pydantic `ValidationError`, and unhandled `Exception`. Each handler transforms the exception into the standard error response format (§8.3) with the correct HTTP status code. Unhandled exceptions produce a generic 500 response and are logged with full context.

**Business Value:** Guarantees every API error — expected or unexpected — produces a consistent, parseable JSON response that the frontend can handle uniformly.

**Acceptance Criteria:**
- [ ] `CalyxException` subclasses return the standard error format with correct status code
- [ ] Pydantic validation errors return 422 with per-field error details
- [ ] Unhandled exceptions return 500 with a generic message (no stack trace in response)
- [ ] Unhandled exceptions are logged with full traceback, request ID, and user context
- [ ] `request_id` is included in every error response
- [ ] Response content type is always `application/json`

**Dependencies:** BF-004, BF-007

**Complexity:** M

**Priority:** P0

**Definition of Done:** Throwing any exception from a route handler produces the correct standard error response. Verified with test requests.

---

### BF-006: Structured Logging

**Title:** Configure structured JSON logging with contextual fields

**Description:**
Set up `structlog` for structured JSON logging in `app/core/logging.py`. Configure log processors to include `request_id`, `user_id`, `org_id`, `timestamp`, `level`, and `module` in every log entry. Configure log level from environment. Ensure no sensitive data (passwords, tokens, emails) is logged.

**Business Value:** Structured logs are searchable, filterable, and parseable by log aggregation tools. Contextual fields enable tracing a request across the entire backend.

**Acceptance Criteria:**
- [ ] Logs are emitted as JSON in production, human-readable in development
- [ ] `request_id` is included in every log entry (after middleware sets it)
- [ ] `user_id` and `org_id` are included when available
- [ ] Log level is configurable via `LOG_LEVEL` env var
- [ ] A `get_logger()` utility returns a contextualized logger
- [ ] Sensitive fields are redacted (passwords, tokens, API keys)

**Dependencies:** BF-001, BF-002

**Complexity:** S

**Priority:** P1

**Definition of Done:** Log output is structured JSON with all contextual fields populated for an authenticated request.

---

### BF-007: Request ID Middleware

**Title:** Add middleware that assigns a unique request ID to every request

**Description:**
Create middleware that generates a UUID for each incoming request, attaches it to the request state, includes it in the response headers (`X-Request-ID`), and makes it available to the logging context. If the client sends an `X-Request-ID` header, use it (for request tracing across frontend and backend).

**Business Value:** Request IDs enable correlating logs, errors, and support tickets to specific API calls. Essential for debugging in production.

**Acceptance Criteria:**
- [ ] Every response includes `X-Request-ID` header
- [ ] If the client sends `X-Request-ID`, the backend uses it
- [ ] If no client header, a new UUID is generated
- [ ] The request ID is accessible via `request.state.request_id`
- [ ] The request ID is injected into the structlog context

**Dependencies:** BF-001

**Complexity:** S

**Priority:** P0

**Definition of Done:** Every response has a request ID. Logs for that request include the same ID.

---

### BF-008: CORS Middleware

**Title:** Configure CORS with environment-based origin allowlisting

**Description:**
Add CORS middleware to the FastAPI app. Allowed origins are loaded from the `CORS_ORIGINS` environment variable (comma-separated list). In development, allow `localhost:3000`. In production, only allow the deployed frontend domain. Credentials must be allowed for cookie-based auth flows.

**Business Value:** CORS misconfiguration either blocks the frontend entirely or creates a security vulnerability. This must be correct from day one.

**Acceptance Criteria:**
- [ ] CORS middleware is registered on the FastAPI app
- [ ] Allowed origins are loaded from environment, not hardcoded
- [ ] `allow_credentials` is `True`
- [ ] `allow_methods` includes GET, POST, PUT, PATCH, DELETE, OPTIONS
- [ ] `allow_headers` includes Authorization, Content-Type, X-Org-Id, X-Request-ID
- [ ] Requests from non-allowed origins are rejected

**Dependencies:** BF-001, BF-002

**Complexity:** S

**Priority:** P0

**Definition of Done:** Frontend on `localhost:3000` can call the backend without CORS errors. Requests from unknown origins are blocked.

---

### BF-009: Standard Response Builders

**Title:** Create utility functions for consistent API response formatting

**Description:**
Create `app/shared/response.py` with helper functions that produce responses in the standard format (§8.2): `success_response(data, meta)` for single resources, `list_response(data, pagination, meta)` for collections, `created_response(data, meta)` for 201s. Each includes `request_id` and `timestamp` in `meta`.

**Business Value:** Consistent response formatting across all endpoints. No developer needs to manually construct the response envelope — they call a builder.

**Acceptance Criteria:**
- [ ] `success_response()` returns `{"data": ..., "meta": {"request_id": ..., "timestamp": ...}}`
- [ ] `list_response()` includes `pagination` with `cursor`, `has_more`, `total_count`
- [ ] `created_response()` returns HTTP 201 with the same envelope
- [ ] `no_content_response()` returns HTTP 204 with empty body
- [ ] All builders accept a FastAPI `Request` object to extract the request ID
- [ ] Response models are defined as Pydantic generics for type safety

**Dependencies:** BF-001, BF-007

**Complexity:** S

**Priority:** P1

**Definition of Done:** Route handlers use response builders. All responses match the approved API format.

---

### BF-010: Health Check Endpoint

**Title:** Create a health check endpoint with dependency verification

**Description:**
Create `GET /api/v1/health` that verifies database connectivity and returns system health status. This endpoint is unauthenticated (used by load balancers and monitoring). Return service name, version, uptime, and dependency status.

**Business Value:** Enables automated monitoring, load balancer health checks, and deployment verification.

**Acceptance Criteria:**
- [ ] `GET /api/v1/health` returns 200 when all dependencies are healthy
- [ ] Response includes `{"status": "healthy", "version": "...", "dependencies": {"database": "connected"}}`
- [ ] Returns 503 if database is unreachable
- [ ] No authentication required
- [ ] Response time < 500ms (health checks must be fast)

**Dependencies:** BF-001, BF-003

**Complexity:** S

**Priority:** P1

**Definition of Done:** Health endpoint responds correctly when DB is up and returns 503 when DB is down.

---

### BF-011: Cursor-Based Pagination Utilities

**Title:** Implement reusable cursor-based pagination helpers

**Description:**
Create `app/shared/pagination.py` with utilities for cursor-based pagination as defined in §8.4. Implement cursor encoding/decoding (opaque base64-encoded `(created_at, id)` tuples), a `paginate()` helper that applies cursor filtering and limit to a query, and Pydantic models for pagination request parameters and response metadata.

**Business Value:** Every list endpoint uses pagination. Building it once as a shared utility ensures consistency and prevents each endpoint from reimplementing cursor logic.

**Acceptance Criteria:**
- [ ] `PaginationParams` Pydantic model accepts `cursor` (optional string) and `limit` (int, default 25, max 100)
- [ ] `encode_cursor(created_at, id)` returns an opaque base64 string
- [ ] `decode_cursor(cursor_string)` returns `(created_at, id)` tuple
- [ ] `PaginationMeta` model includes `cursor`, `has_more`, `total_count`
- [ ] Invalid cursor strings raise a `ValidationError` with a clear message
- [ ] Pagination works with any table that has `created_at` and `id` columns

**Dependencies:** BF-001, BF-004

**Complexity:** M

**Priority:** P1

**Definition of Done:** Pagination helper can be used in a sample query to page through test data correctly.

---

# Epic 2: Frontend Foundation (FF)

> **Epic Goal:** A fully configured Next.js application with layouts, Supabase integration, API client, auth context, and route protection.

---

### FF-001: Initialize Next.js Project

**Title:** Create Next.js project with TypeScript and App Router

**Description:**
Initialize a Next.js project using `create-next-app` with TypeScript, App Router, ESLint, and `src/` directory. Configure `tsconfig.json` with strict mode. Set up path aliases (`@/` maps to `src/`). Verify the dev server starts cleanly.

**Business Value:** Foundation for all frontend work. Must be correctly configured from the start to avoid cascading issues.

**Acceptance Criteria:**
- [ ] Next.js project created with App Router and TypeScript
- [ ] `tsconfig.json` has `strict: true`
- [ ] Path alias `@/` resolves to `src/`
- [ ] ESLint configured with `@typescript-eslint` and `next/core-web-vitals`
- [ ] Prettier configured with consistent formatting rules
- [ ] `npm run dev` starts the dev server on port 3000
- [ ] `npm run build` produces no errors
- [ ] `npm run lint` passes with no warnings

**Dependencies:** None

**Complexity:** S

**Priority:** P0

**Definition of Done:** Dev server runs, build succeeds, lint passes.

---

### FF-002: Tailwind CSS and shadcn/ui Setup

**Title:** Configure Tailwind CSS and install shadcn/ui component system

**Description:**
Configure Tailwind CSS with the project. Initialize shadcn/ui with the default theme. Install foundational primitive components: Button, Input, Label, Card, Dialog, Dropdown Menu, Separator, Avatar, Badge, Skeleton, Tooltip, Sonner (toast). Configure the `components.json` for shadcn/ui path resolution.

**Business Value:** Design system foundation. All UI components build on top of shadcn/ui primitives and Tailwind utilities. Must be set up before any UI work.

**Acceptance Criteria:**
- [ ] Tailwind CSS compiles and applies styles correctly
- [ ] shadcn/ui initialized with `components.json` configured
- [ ] All listed primitive components are installed in `src/components/ui/`
- [ ] Components render correctly in a test page
- [ ] `tailwind.config.ts` extends the default theme with Calyx brand colors
- [ ] CSS variables for theming are defined in `globals.css`
- [ ] Dark mode support configured via `class` strategy

**Dependencies:** FF-001

**Complexity:** S

**Priority:** P0

**Definition of Done:** shadcn/ui components render correctly with Tailwind styling. Dark mode toggles work.

---

### FF-003: Design Tokens and Global Styles

**Title:** Define Calyx design tokens, typography, and global CSS

**Description:**
Establish the visual identity: color palette (brand colors, semantic colors, surface colors for light and dark modes), typography scale (using Inter from Google Fonts), spacing scale, border radius tokens, and shadow tokens. Define these as CSS custom properties in `globals.css` and as Tailwind theme extensions.

**Business Value:** A consistent design language across the entire app. Every component uses the same tokens — no ad-hoc color values.

**Acceptance Criteria:**
- [ ] Color tokens defined for: brand primary/secondary, success/warning/error/info, surface/background, text levels
- [ ] Light and dark mode color sets defined via CSS custom properties
- [ ] Inter font loaded from Google Fonts and set as default
- [ ] Typography scale defined (h1–h4, body, small, caption)
- [ ] Spacing, radius, and shadow tokens defined in Tailwind config
- [ ] A reference page exists (temporarily) showing all tokens

**Dependencies:** FF-002

**Complexity:** S

**Priority:** P1

**Definition of Done:** Tokens are defined, theme is consistent between Tailwind config and CSS variables, reference page renders correctly.

---

### FF-004: Root Layout with Providers

**Title:** Create the root layout with global providers

**Description:**
Create `src/app/layout.tsx` — the root layout wrapping the entire application. It should set up: HTML lang attribute, font loading, metadata (title, description), the Supabase auth provider (from FF-008), the React Query provider (TanStack Query), the toast provider (Sonner), and the theme provider.

**Business Value:** Global providers must wrap the entire app once. Doing this correctly in the root layout prevents provider duplication and context issues.

**Acceptance Criteria:**
- [ ] Root layout sets `<html lang="en">` with dark mode class
- [ ] Meta tags set for default title, description, and viewport
- [ ] Font (Inter) is loaded and applied
- [ ] React Query `QueryClientProvider` wraps children
- [ ] Toast provider (Sonner `Toaster`) is included
- [ ] Theme provider supports light/dark mode
- [ ] No layout shift on initial page load

**Dependencies:** FF-001, FF-002, FF-003

**Complexity:** S

**Priority:** P0

**Definition of Done:** App renders with all providers active. React Query devtools accessible in development.

---

### FF-005: Auth Layout (Public Pages)

**Title:** Create the (auth) route group layout for public authentication pages

**Description:**
Create `src/app/(auth)/layout.tsx` — a minimal, centered layout for login, signup, forgot-password, and related pages. This layout should have no sidebar, no navigation — just a centered card with the Calyx logo. If the user is already authenticated, redirect to the dashboard.

**Business Value:** Clean, distraction-free authentication experience. Authenticated users are redirected away to prevent confusion.

**Acceptance Criteria:**
- [ ] `(auth)/layout.tsx` renders a centered container with Calyx branding
- [ ] Layout is visually distinct from the platform layout (no sidebar, no header)
- [ ] If user has a valid session, redirect to `/dashboard`
- [ ] Layout is responsive (works on mobile widths)
- [ ] Placeholder pages exist: `login/page.tsx`, `signup/page.tsx`, `forgot-password/page.tsx`, `reset-password/page.tsx`, `verify-email/page.tsx`

**Dependencies:** FF-001, FF-004

**Complexity:** S

**Priority:** P0

**Definition of Done:** Auth layout renders correctly. Placeholder pages are accessible at their routes.

---

### FF-006: Platform Layout (Protected Pages)

**Title:** Create the (platform) route group layout for the authenticated application

**Description:**
Create `src/app/(platform)/layout.tsx` — the main application layout with sidebar navigation, header with user avatar and org switcher, and a content area. This layout requires authentication — unauthenticated users are redirected to `/login`. The layout must also validate that the user has an active organization context.

**Business Value:** The primary application shell that every authenticated page renders within. Consistent navigation and org context across all platform pages.

**Acceptance Criteria:**
- [ ] `(platform)/layout.tsx` renders sidebar + header + content area
- [ ] Unauthenticated users are redirected to `/login`
- [ ] Users without an organization are redirected to `/create-org`
- [ ] Sidebar includes navigation links (Dashboard, Workspaces, Search, Members, Settings) — can link to placeholder pages
- [ ] Header shows user avatar, display name, and organization name
- [ ] Layout is responsive (sidebar collapses on mobile)
- [ ] Placeholder pages exist: `dashboard/page.tsx`, `settings/page.tsx`

**Dependencies:** FF-004, FF-005, FF-008, FF-010, SC-008

**Complexity:** L

**Priority:** P0

**Definition of Done:** Platform layout renders with sidebar and header. Auth redirects work. Responsive on mobile.

---

### FF-007: Onboarding Layout

**Title:** Create the (onboarding) route group layout for post-signup flows

**Description:**
Create `src/app/(onboarding)/layout.tsx` — a focused layout for the "Create Organization" and "Join Organization" flows. Requires authentication but does not require an organization context (the user doesn't have one yet). Minimal UI — centered content with a step indicator.

**Business Value:** New users need a dedicated flow to create or join their first organization. This layout separates the onboarding UX from the main app.

**Acceptance Criteria:**
- [ ] `(onboarding)/layout.tsx` renders a centered, focused container
- [ ] Requires authentication (redirect to `/login` if not authenticated)
- [ ] Does NOT require org context
- [ ] Placeholder pages exist: `create-org/page.tsx`, `join-org/page.tsx`
- [ ] Back navigation returns to login (user can sign out)
- [ ] Layout is responsive

**Dependencies:** FF-004, FF-008

**Complexity:** S

**Priority:** P1

**Definition of Done:** Onboarding layout renders correctly. Auth is required, org context is not.

---

### FF-008: Supabase Client Configuration

**Title:** Configure Supabase client for browser and server contexts

**Description:**
Create `src/lib/supabase/client.ts` for the browser Supabase client and `src/lib/supabase/server.ts` for the server-side client (used in Server Components and Route Handlers). Both must use environment variables for Supabase URL and anon key. The browser client handles token storage and refresh automatically.

**Business Value:** Supabase client is the foundation for authentication, and eventually for direct database queries from Server Components. Must work correctly in both client and server contexts.

**Acceptance Criteria:**
- [ ] Browser client created with `createBrowserClient()` from `@supabase/ssr`
- [ ] Server client created with `createServerClient()` using cookies
- [ ] Environment variables `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` are used
- [ ] Browser client is a singleton (not recreated on every render)
- [ ] Server client reads/writes cookies correctly for session management
- [ ] TypeScript types are generated for the Supabase schema (or placeholder types defined)

**Dependencies:** FF-001

**Complexity:** M

**Priority:** P0

**Definition of Done:** `supabase.auth.getSession()` works in both browser and server contexts.

---

### FF-009: API Client with Interceptors

**Title:** Create a typed API client for backend communication

**Description:**
Create `src/lib/api/client.ts` — a fetch-based API client that communicates with the FastAPI backend. The client must: attach the `Authorization` header (Bearer token from Supabase session), attach the `X-Org-Id` header (from org context), attach `X-Request-ID`, handle token refresh on 401 responses, and parse error responses into typed error objects.

**Business Value:** Every frontend-to-backend call goes through this client. Centralized auth header injection and error handling prevents bugs in every feature.

**Acceptance Criteria:**
- [ ] `apiClient.get()`, `.post()`, `.put()`, `.patch()`, `.delete()` methods exist
- [ ] `Authorization: Bearer <token>` header is automatically attached
- [ ] `X-Org-Id` header is automatically attached from current org context
- [ ] `X-Request-ID` header is attached (UUID per request)
- [ ] 401 responses trigger token refresh and retry
- [ ] Error responses are parsed into a typed `ApiError` object
- [ ] Base URL is configurable via environment variable
- [ ] Request/response types are generic for type safety

**Dependencies:** FF-001, FF-008

**Complexity:** M

**Priority:** P0

**Definition of Done:** API client can make authenticated requests to the backend. 401 retry logic works.

---

### FF-010: Auth Context Provider

**Title:** Create React context for authentication state

**Description:**
Create `src/lib/hooks/use-auth.tsx` with an `AuthProvider` component and `useAuth()` hook. The provider listens to Supabase auth state changes, stores the current user and session, and provides `signOut()`, `isLoading`, `isAuthenticated`, and `user` to the component tree.

**Business Value:** Auth state must be globally accessible. Components need to know who's logged in, whether loading is in progress, and how to sign out — without each component calling Supabase directly.

**Acceptance Criteria:**
- [ ] `AuthProvider` wraps children and listens to `onAuthStateChange`
- [ ] `useAuth()` returns `{ user, session, isLoading, isAuthenticated, signOut }`
- [ ] `isLoading` is true during initial session check
- [ ] `user` is null when not authenticated
- [ ] `signOut()` calls `supabase.auth.signOut()` and clears state
- [ ] Auth state updates trigger re-renders in consuming components
- [ ] Provider is mounted in the root layout (FF-004)

**Dependencies:** FF-008

**Complexity:** M

**Priority:** P0

**Definition of Done:** `useAuth()` returns correct state in both authenticated and unauthenticated scenarios.

---

### FF-011: Next.js Route Protection Middleware

**Title:** Implement Next.js middleware for route-level auth checks

**Description:**
Create `src/middleware.ts` that intercepts all requests and: checks for a valid Supabase session, redirects unauthenticated users to `/login` for `(platform)` routes, redirects authenticated users away from `(auth)` routes, and allows unauthenticated access to public routes (landing page, health).

**Business Value:** Route protection at the middleware level prevents unauthenticated users from even reaching protected pages. Faster than checking in each page component.

**Acceptance Criteria:**
- [ ] Unauthenticated requests to `/dashboard`, `/workspaces`, `/settings`, etc. redirect to `/login`
- [ ] Authenticated requests to `/login`, `/signup` redirect to `/dashboard`
- [ ] `/api/*` routes are not affected by middleware (API handles its own auth)
- [ ] Public routes (`/`, `/health`) are accessible without auth
- [ ] Middleware refreshes the Supabase session (extends token if valid)
- [ ] Middleware runs on edge (no heavy imports)

**Dependencies:** FF-008

**Complexity:** M

**Priority:** P0

**Definition of Done:** Route protection works for all route groups. Manual testing confirms redirect behavior.

---

### FF-012: Shared TypeScript Types

**Title:** Define shared TypeScript interfaces for API contracts

**Description:**
Create `src/types/` with TypeScript interfaces for all domain objects: `User`, `Organization`, `Membership`, `Role`, `Permission`, `Workspace`, `Document`, `Memory`, `AuditLog`, `ApiError`, `PaginatedResponse<T>`, `ApiResponse<T>`. These types are shared across all frontend modules.

**Business Value:** Type safety across the frontend. Every component and API call uses the same type definitions, preventing type mismatches and runtime errors.

**Acceptance Criteria:**
- [ ] `src/types/index.ts` exports all shared types
- [ ] Types match the database schema from the Design Review (§7)
- [ ] `ApiResponse<T>` wraps `{ data: T, meta: {...} }`
- [ ] `PaginatedResponse<T>` includes `pagination: { cursor, has_more, total_count }`
- [ ] `ApiError` matches the error response format (§8.3)
- [ ] Enum types defined for: `MembershipStatus`, `Visibility`, `LifecycleState`, `MemoryType`
- [ ] No `any` types

**Dependencies:** FF-001

**Complexity:** S

**Priority:** P1

**Definition of Done:** Types compile, are importable from `@/types`, and match the approved API contract.

---

# Epic 3: Shared Components (SC)

> **Epic Goal:** A library of reusable UI components built on shadcn/ui primitives, providing the building blocks for every feature page.

---

### SC-001: Form Components System

**Title:** Create a composable form system with validation

**Description:**
Build form components using `react-hook-form` and `zod` for validation, integrated with shadcn/ui inputs. Create: `FormField`, `FormLabel`, `FormMessage` (error display), `FormDescription`. The system should work with shadcn's `Input`, `Select`, `Textarea`, and `Checkbox` components.

**Business Value:** Every feature has forms (signup, login, create org, create workspace, create document). A unified form system with validation prevents per-form reimplementation.

**Acceptance Criteria:**
- [ ] `react-hook-form` and `zod` are installed and configured
- [ ] `FormField` component connects `react-hook-form` to shadcn/ui `Input`
- [ ] Validation errors display below the field via `FormMessage`
- [ ] Form submission handles loading state (disables submit button)
- [ ] Zod schemas can be passed to forms for type-safe validation
- [ ] Works with `Input`, `Textarea`, `Select`, `Checkbox`

**Dependencies:** FF-002

**Complexity:** M

**Priority:** P0

**Definition of Done:** A sample form with 3 fields validates correctly, shows errors, and submits.

---

### SC-002: Toast Notification System

**Title:** Configure toast notifications for user feedback

**Description:**
Set up Sonner (already installed via shadcn) with a `toast` utility that provides `toast.success()`, `toast.error()`, `toast.info()`, and `toast.warning()`. Position at bottom-right. Style consistent with Calyx design tokens.

**Business Value:** User feedback for async actions (save, delete, error) must be immediate and consistent across the app.

**Acceptance Criteria:**
- [ ] `toast.success("Saved")` displays a green-accented toast
- [ ] `toast.error("Failed")` displays a red-accented toast
- [ ] Toasts auto-dismiss after 5 seconds (configurable)
- [ ] Toasts are stackable (multiple can display)
- [ ] Toasts have a dismiss button
- [ ] Styling matches Calyx design tokens (colors, radius, font)

**Dependencies:** FF-002, FF-004

**Complexity:** S

**Priority:** P1

**Definition of Done:** All four toast variants render correctly and auto-dismiss.

---

### SC-003: Error Boundary Component

**Title:** Create a React error boundary for graceful crash recovery

**Description:**
Build a reusable `ErrorBoundary` component that catches rendering errors, displays a user-friendly error message with a "Try Again" button, and logs the error. Create a `ErrorFallback` component for the error UI. Wrap each major layout with an error boundary.

**Business Value:** Prevents a crash in one component from white-screening the entire app. Users see a recoverable error state instead of a blank page.

**Acceptance Criteria:**
- [ ] `ErrorBoundary` catches render errors in children
- [ ] Error fallback shows a message, error details (in dev), and "Try Again" button
- [ ] "Try Again" re-renders the children (resets the error state)
- [ ] Error is logged to console (and to an error reporting service in the future)
- [ ] Works with both Server Components and Client Components
- [ ] Styled with Calyx design tokens

**Dependencies:** FF-002

**Complexity:** S

**Priority:** P1

**Definition of Done:** Intentionally thrown error renders the fallback UI. "Try Again" recovers.

---

### SC-004: Empty State Component

**Title:** Create a reusable empty state component

**Description:**
Build an `EmptyState` component that displays when a list or page has no content. Accepts: `icon`, `title`, `description`, and optional `action` (a CTA button). Used in: empty workspace list, empty document list, empty search results, etc.

**Business Value:** Empty states are the first thing users see in a new account. A polished empty state with a clear CTA drives activation.

**Acceptance Criteria:**
- [ ] `EmptyState` accepts `icon`, `title`, `description`, `action` props
- [ ] `action` renders a Button with an onClick or href
- [ ] Component is centered in its container
- [ ] Responsive and readable at all widths
- [ ] Styled with Calyx design tokens
- [ ] Variant for "no search results" with different messaging

**Dependencies:** FF-002

**Complexity:** S

**Priority:** P2

**Definition of Done:** Component renders correctly with and without an action. Responsive.

---

### SC-005: Loading Skeleton Components

**Title:** Create loading skeleton components for content placeholders

**Description:**
Build skeleton variants for common UI patterns: `SkeletonCard`, `SkeletonList` (multiple rows), `SkeletonText` (text block placeholder), `SkeletonAvatar`. These display while data is loading, preventing layout shift.

**Business Value:** Loading skeletons provide perceived performance. Users see the page structure immediately, even before data arrives.

**Acceptance Criteria:**
- [ ] Skeletons use shadcn/ui's `Skeleton` primitive with animation
- [ ] `SkeletonCard` matches the dimensions of a typical content card
- [ ] `SkeletonList` accepts `count` prop to render N skeleton rows
- [ ] `SkeletonText` accepts `lines` prop to render N text-width bars
- [ ] Animation is subtle (pulse, not bounce)
- [ ] Skeletons match the layout of the actual content they replace

**Dependencies:** FF-002

**Complexity:** S

**Priority:** P2

**Definition of Done:** Skeletons render correctly and match the layout of their corresponding real components.

---

### SC-006: Page Shell Component

**Title:** Create a page shell component with title, breadcrumbs, and actions

**Description:**
Build a `PageShell` component that standardizes every platform page's header area. Includes: page title (h1), optional breadcrumbs, optional description, and optional action buttons (top-right). Every `(platform)` page wraps its content in `PageShell`.

**Business Value:** Consistent page structure across the app. No page has a different header pattern. Breadcrumbs improve navigation.

**Acceptance Criteria:**
- [ ] `PageShell` accepts `title`, `description`, `breadcrumbs`, `actions` props
- [ ] Title renders as `<h1>` for accessibility and SEO
- [ ] Breadcrumbs render as a horizontal trail with clickable links
- [ ] Actions render in the top-right area (e.g., "Create Workspace" button)
- [ ] Responsive — actions wrap below title on mobile
- [ ] Consistent padding and spacing

**Dependencies:** FF-002

**Complexity:** S

**Priority:** P1

**Definition of Done:** Page shell renders correctly with all prop combinations. Responsive.

---

### SC-007: Sidebar Navigation Component

**Title:** Build the sidebar navigation for the platform layout

**Description:**
Create a `Sidebar` component with: Calyx logo at the top, navigation links with icons (Dashboard, Workspaces, Search, Members, Settings), active state highlighting based on current route, collapse/expand functionality, and an org switcher at the bottom (placeholder until ORG-005).

**Business Value:** The sidebar is the primary navigation for the entire app. It must be functional, accessible, and visually polished.

**Acceptance Criteria:**
- [ ] Sidebar renders vertically with navigation links
- [ ] Active route is visually highlighted
- [ ] Each nav item has an icon (Lucide icons) and label
- [ ] Sidebar is collapsible to icon-only mode
- [ ] Collapsed state persists (localStorage)
- [ ] Mobile: sidebar is a slide-out drawer
- [ ] Org switcher placeholder at the bottom
- [ ] Keyboard accessible (arrow keys, enter to navigate)

**Dependencies:** FF-002, FF-003

**Complexity:** M

**Priority:** P0

**Definition of Done:** Sidebar renders, routes highlight correctly, collapses, works on mobile.

---

### SC-008: Header Component

**Title:** Build the header bar for the platform layout

**Description:**
Create a `Header` component with: mobile menu toggle (hamburger for sidebar), search input (placeholder — navigates to `/search`), notification bell (placeholder), user avatar with dropdown (profile, settings, sign out).

**Business Value:** The header provides quick access to search, notifications, and user account actions from any page.

**Acceptance Criteria:**
- [ ] Header renders horizontally at the top of the content area
- [ ] Mobile menu button toggles sidebar visibility
- [ ] Search input placeholder navigates to `/search` on submit
- [ ] User avatar dropdown includes: user name, email, "Profile", "Settings", separator, "Sign Out"
- [ ] "Sign Out" calls `signOut()` from `useAuth()`
- [ ] Header is responsive

**Dependencies:** FF-002, FF-010

**Complexity:** M

**Priority:** P0

**Definition of Done:** Header renders, dropdown works, sign out logs the user out.

---

# Epic 4: Identity (ID)

> **Epic Goal:** Complete authentication flow — signup, login, OAuth, email verification, password reset, and session management.

---

### ID-001: Supabase Auth Configuration

**Title:** Configure Supabase project for authentication

**Description:**
Configure the Supabase project (via Supabase dashboard or CLI): enable email/password auth, enable Google OAuth provider, configure email templates (verification, password reset, invitation), set redirect URLs for OAuth callbacks, configure JWT expiry and refresh token settings. Document all configuration steps.

**Business Value:** Auth must be correctly configured in Supabase before any auth flow can work. Misconfiguration causes silent failures.

**Acceptance Criteria:**
- [ ] Email/password auth is enabled in Supabase dashboard
- [ ] Google OAuth provider is configured with client ID and secret
- [ ] Redirect URLs are set for local development (`localhost:3000`)
- [ ] Email templates are customized with Calyx branding (logo, colors, copy)
- [ ] JWT expiry is set to 1 hour
- [ ] Refresh token rotation is enabled
- [ ] Configuration steps are documented in a setup guide
- [ ] Test: signup with email/password creates a Supabase user

**Dependencies:** None (Supabase project exists)

**Complexity:** M

**Priority:** P0

**Definition of Done:** Email signup and Google OAuth work in the Supabase dashboard test UI.

---

### ID-002: Email Signup Page

**Title:** Build the email signup page with form validation

**Description:**
Create `src/app/(auth)/signup/page.tsx` with a signup form: full name, email, password, confirm password. Validate with zod (password strength, email format, matching passwords). On submit, call `supabase.auth.signUp()`. Show "Check your email" message on success. Show errors on failure. Include a link to login.

**Business Value:** First touchpoint for new users. Must be polished, fast, and error-free.

**Acceptance Criteria:**
- [ ] Form fields: Full Name, Email, Password, Confirm Password
- [ ] Client-side validation: email format, password min 8 chars with complexity, passwords match
- [ ] Submit calls `supabase.auth.signUp()` with email, password, and `data: { full_name }`
- [ ] On success: show "Verification email sent" message
- [ ] On error: show user-friendly error (e.g., "Email already registered")
- [ ] Loading state on submit button
- [ ] "Already have an account? Log in" link
- [ ] "Continue with Google" button (links to OAuth flow, ID-005)
- [ ] Page is accessible (labels, focus management, screen reader support)

**Dependencies:** FF-005, FF-008, SC-001, ID-001

**Complexity:** M

**Priority:** P0

**Definition of Done:** User can sign up with email. Verification email is received. Errors display correctly.

---

### ID-003: Complete Signup Backend Endpoint

**Title:** Create POST /api/v1/auth/complete-signup endpoint

**Description:**
Create the backend endpoint that the frontend calls after Supabase Auth confirms the user's identity. This endpoint: validates the JWT, creates a user profile record in the `users` table (idempotent — if profile exists, return it), checks for pending invitations by email, and returns the user profile and any matching organization.

**Business Value:** Bridges Supabase Auth (identity) and Calyx (application profile). Without this, authenticated users have no profile data.

**Acceptance Criteria:**
- [ ] `POST /api/v1/auth/complete-signup` requires a valid Supabase JWT
- [ ] Creates a user record with `id` (from JWT sub), `email`, `full_name`, `avatar_url`
- [ ] Idempotent — calling twice with the same JWT does not create a duplicate
- [ ] Checks `invitations` table for pending invitations matching the user's email
- [ ] If invitation exists: creates a membership, marks invitation as accepted, returns `{ user, organization, role }`
- [ ] If no invitation: returns `{ user, organization: null }`
- [ ] Returns standard response format
- [ ] Logs the signup event

**Dependencies:** BF-001, BF-002, BF-003, BF-004, BF-005, BF-009

**Complexity:** M

**Priority:** P0

**Definition of Done:** Endpoint creates a user profile from a valid JWT. Invitation matching works. Idempotent.

---

### ID-004: Email Login Page

**Title:** Build the email login page with error handling

**Description:**
Create `src/app/(auth)/login/page.tsx` with a login form: email and password. On submit, call `supabase.auth.signInWithPassword()`. On success, redirect to `/dashboard` (or `/create-org` if no org). Show generic error on failure ("Invalid email or password" — never reveal which is wrong).

**Business Value:** Primary entry point for returning users. Must be fast, secure, and impossible to misuse for email enumeration.

**Acceptance Criteria:**
- [ ] Form fields: Email, Password
- [ ] Submit calls `supabase.auth.signInWithPassword()`
- [ ] On success: call `POST /api/v1/auth/complete-signup` (idempotent), then redirect
- [ ] Redirect to `/dashboard` if user has an org, `/create-org` if not
- [ ] On error: show "Invalid email or password" (generic)
- [ ] Loading state on submit button
- [ ] "Forgot password?" link to `/forgot-password`
- [ ] "Don't have an account? Sign up" link
- [ ] "Continue with Google" button
- [ ] No email enumeration (same error for wrong email vs. wrong password)

**Dependencies:** FF-005, FF-008, SC-001, ID-001

**Complexity:** M

**Priority:** P0

**Definition of Done:** User can log in with valid credentials. Invalid credentials show a generic error. Redirects work correctly.

---

### ID-005: Google OAuth Flow

**Title:** Implement Google OAuth sign-in

**Description:**
Add a "Continue with Google" button on both login and signup pages. Clicking it calls `supabase.auth.signInWithOAuth({ provider: 'google' })`. Handle the OAuth callback redirect. After Google auth completes, call `complete-signup` to ensure a Calyx profile exists.

**Business Value:** Google OAuth reduces signup friction. Enterprise users often prefer OAuth over passwords.

**Acceptance Criteria:**
- [ ] "Continue with Google" button on login and signup pages
- [ ] Button triggers `supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo } })`
- [ ] OAuth callback URL is configured in Supabase dashboard
- [ ] After redirect, `complete-signup` is called to ensure Calyx profile exists
- [ ] Works for both new users (signup) and existing users (login)
- [ ] User's Google name and avatar are stored in the profile
- [ ] Error handling for denied consent or OAuth failures

**Dependencies:** ID-001, ID-002, ID-004, ID-003

**Complexity:** M

**Priority:** P0

**Definition of Done:** User can sign up and log in with Google. Profile is created with Google name/avatar.

---

### ID-006: Email Verification Page

**Title:** Build the email verification confirmation page

**Description:**
Create `src/app/(auth)/verify-email/page.tsx` that handles the verification callback from Supabase email links. Also create a "Check your email" interstitial page shown after signup with a "Resend verification email" button.

**Business Value:** Verified emails are required for account security and prevent spam signups.

**Acceptance Criteria:**
- [ ] Verification link from email redirects to `/verify-email` with token
- [ ] Page confirms verification status and redirects to login (or auto-logs in)
- [ ] "Resend verification email" button calls `supabase.auth.resend()`
- [ ] Clear messaging: "Your email has been verified" / "Verification failed, try again"
- [ ] Rate limiting on resend (disable button for 60 seconds after click)
- [ ] Handles expired verification links gracefully

**Dependencies:** FF-005, FF-008, ID-001

**Complexity:** M

**Priority:** P1

**Definition of Done:** Clicking the verification link in the email confirms the account. Resend works.

---

### ID-007: Forgot Password Page

**Title:** Build the forgot password request page

**Description:**
Create `src/app/(auth)/forgot-password/page.tsx` with an email input. On submit, call `supabase.auth.resetPasswordForEmail()`. Always show success ("If an account exists, we sent a reset link") to prevent email enumeration.

**Business Value:** Users will forget passwords. This flow must be self-service and secure.

**Acceptance Criteria:**
- [ ] Form field: Email
- [ ] Submit calls `supabase.auth.resetPasswordForEmail(email, { redirectTo })`
- [ ] Always shows success message (even if email doesn't exist)
- [ ] "Back to login" link
- [ ] Loading state during submission
- [ ] Rate limiting: disable button for 60 seconds after submission

**Dependencies:** FF-005, FF-008, SC-001, ID-001

**Complexity:** S

**Priority:** P1

**Definition of Done:** Password reset email is sent for valid accounts. No email enumeration.

---

### ID-008: Reset Password Page

**Title:** Build the password reset confirmation page

**Description:**
Create `src/app/(auth)/reset-password/page.tsx`. This page is reached via the reset link in the email. Shows a form with "New Password" and "Confirm Password". On submit, calls `supabase.auth.updateUser({ password })`. Redirects to login on success.

**Business Value:** Completes the password reset flow. Without this, users are locked out after forgetting their password.

**Acceptance Criteria:**
- [ ] Form fields: New Password, Confirm Password
- [ ] Password validation: min 8 chars, complexity requirements, passwords match
- [ ] Submit calls `supabase.auth.updateUser({ password: newPassword })`
- [ ] On success: show confirmation, redirect to `/login` after 3 seconds
- [ ] On error: show user-friendly message
- [ ] Handles invalid/expired reset tokens gracefully

**Dependencies:** FF-005, FF-008, SC-001, ID-001

**Complexity:** S

**Priority:** P1

**Definition of Done:** User can reset their password via the email link. Invalid tokens show a clear error.

---

### ID-009: Logout Functionality

**Title:** Implement logout across frontend and backend

**Description:**
Implement `signOut()` in the `useAuth()` hook: call `supabase.auth.signOut()`, clear all client state (React Query cache, org context), and redirect to `/login`. Ensure the session is fully invalidated.

**Business Value:** Users must be able to sign out. Incomplete logout is a security vulnerability (stale sessions).

**Acceptance Criteria:**
- [ ] `signOut()` calls `supabase.auth.signOut()`
- [ ] React Query cache is cleared on logout
- [ ] Org context is cleared on logout
- [ ] User is redirected to `/login`
- [ ] After logout, navigating to a protected route redirects to `/login` (no stale session)
- [ ] Sign out button in the header dropdown (SC-008) triggers this flow

**Dependencies:** FF-010, SC-008

**Complexity:** S

**Priority:** P0

**Definition of Done:** User signs out, all state is cleared, protected routes are inaccessible.

---

### ID-010: Session Refresh Handling

**Title:** Handle automatic token refresh and expired session edge cases

**Description:**
Ensure the Supabase client automatically refreshes tokens before expiry. Handle the edge case where a refresh token has expired (user inactive > 30 days): detect the expired session, show a "Session expired, please log in again" message, and redirect to login. Handle multi-tab scenarios (session refresh in one tab should be reflected in others).

**Business Value:** Seamless session continuity for active users. Clear recovery path for expired sessions. Prevents cryptic 401 errors.

**Acceptance Criteria:**
- [ ] Active sessions are refreshed automatically (no user action required)
- [ ] Expired refresh tokens redirect to `/login` with a "Session expired" message
- [ ] No infinite redirect loops on expired sessions
- [ ] Token refresh in one tab updates the session in other tabs (via Supabase's `onAuthStateChange`)
- [ ] API client (FF-009) retries failed requests after a successful token refresh

**Dependencies:** FF-008, FF-009, FF-010

**Complexity:** M

**Priority:** P1

**Definition of Done:** Token refresh works silently. Expired sessions redirect to login with a clear message.

---

### ID-011: Get Current User Endpoint

**Title:** Create GET /api/v1/auth/me endpoint

**Description:**
Create an endpoint that returns the current user's profile, their organization memberships, and their current organization context. This is called after login and on page load to hydrate the frontend state.

**Business Value:** The frontend needs the full user context (profile + orgs + role) to render the application correctly. This endpoint provides it in a single call.

**Acceptance Criteria:**
- [ ] `GET /api/v1/auth/me` requires a valid JWT
- [ ] Returns `{ user: {...}, memberships: [{org, role}], current_org: {...} | null }`
- [ ] `current_org` is determined by the `X-Org-Id` header (if provided and valid)
- [ ] If `X-Org-Id` is not provided, returns the user's first/default org
- [ ] Returns 401 if JWT is invalid
- [ ] Returns standard response format

**Dependencies:** BF-001, BF-003, BF-009, ID-003

**Complexity:** M

**Priority:** P0

**Definition of Done:** Endpoint returns complete user context. Frontend can hydrate auth state from this response.

---

### ID-012: Backend JWT Validation Dependency

**Title:** Create get_current_user() FastAPI dependency for JWT validation

**Description:**
Create `app/core/security.py` with a `get_current_user()` dependency that: extracts the Bearer token from the Authorization header, validates it against Supabase's JWKS (public key), extracts user claims (sub, email, email_confirmed), and returns a `CurrentUser` object. Raise `AuthenticationError` if the token is invalid or missing.

**Business Value:** Every protected endpoint depends on this. JWT validation must be correct, fast, and reusable.

**Acceptance Criteria:**
- [ ] `get_current_user()` is a FastAPI `Depends()` dependency
- [ ] Extracts Bearer token from Authorization header
- [ ] Validates JWT signature using Supabase's JWT secret or JWKS
- [ ] Validates `exp` (expiry), `iss` (issuer) claims
- [ ] Returns a `CurrentUser` dataclass with `id`, `email`, `email_confirmed`
- [ ] Raises `AuthenticationError` (401) if token is missing, expired, or invalid
- [ ] Raises `AuthorizationError` (403) if `email_confirmed` is false

**Dependencies:** BF-001, BF-002, BF-004

**Complexity:** M

**Priority:** P0

**Definition of Done:** Dependency correctly validates Supabase JWTs. Invalid tokens produce 401.

---

# Epic 5: Organizations (ORG)

> **Epic Goal:** Organization creation, membership management, context resolution, and invitation flow.

---

### ORG-001: Organizations Database Schema

**Title:** Create organizations and memberships tables in Supabase

**Description:**
Create the database tables for organizations, memberships, roles, permissions, role_permissions, and invitations as defined in the Design Review ER diagram (§7). Create RLS policies for tenant isolation. Seed the system roles and permissions.

**Business Value:** The data layer for multi-tenancy. Every other feature stores data within an organization.

**Acceptance Criteria:**
- [ ] `organizations` table created with all columns from the ER diagram
- [ ] `memberships` table with foreign keys to users, organizations, and roles
- [ ] `roles` table with system roles seeded (org_admin, manager, employee, viewer)
- [ ] `permissions` table with all permissions from the RBAC catalog (§5.4)
- [ ] `role_permissions` junction table populated for all system role-permission mappings
- [ ] `invitations` table with status enum (pending, accepted, expired, revoked)
- [ ] RLS policies on all tables: filter by `org_id` from JWT claims or membership
- [ ] Unique constraint on `memberships(user_id, org_id)`
- [ ] Unique constraint on `organizations(slug)`

**Dependencies:** ID-001 (Supabase project configured)

**Complexity:** L

**Priority:** P0

**Definition of Done:** Tables exist, RLS policies are active, system roles and permissions are seeded.

---

### ORG-002: Create Organization Backend

**Title:** Create POST /api/v1/organizations endpoint

**Description:**
Create the endpoint for creating a new organization. Accepts `name` and optional `slug` (auto-generated from name if not provided). Creates the organization record and a membership record for the creator with `org_admin` role. Returns the created organization.

**Business Value:** First thing a new user does after signup. Must work flawlessly.

**Acceptance Criteria:**
- [ ] `POST /api/v1/organizations` requires authentication
- [ ] Request body: `{ "name": "Acme Inc", "slug": "acme-inc" }`
- [ ] Slug is auto-generated from name if not provided (lowercase, hyphenated)
- [ ] Slug uniqueness is enforced (return 409 Conflict if duplicate)
- [ ] Creates organization record
- [ ] Creates membership record with `org_admin` role for the authenticated user
- [ ] Returns 201 with the created organization
- [ ] Audit log entry created

**Dependencies:** BF-001 through BF-009, ORG-001, ID-012

**Complexity:** M

**Priority:** P0

**Definition of Done:** User can create an org. They are automatically assigned as org_admin.

---

### ORG-003: Create Organization Frontend Page

**Title:** Build the "Create Organization" onboarding page

**Description:**
Create `src/app/(onboarding)/create-org/page.tsx` with a form for organization name. On submit, call `POST /api/v1/organizations`. On success, set the org context and redirect to `/dashboard`. This is the first page new users see after signup if they have no org.

**Business Value:** The critical conversion step — a user without an org cannot use Calyx. This page must be simple and fast.

**Acceptance Criteria:**
- [ ] Form field: Organization Name (required, 2–100 chars)
- [ ] Optional: slug preview (auto-generated, editable)
- [ ] Submit calls `POST /api/v1/organizations`
- [ ] On success: set org context, redirect to `/dashboard`
- [ ] On error: show error message (e.g., "Organization name already taken")
- [ ] Loading state during submission
- [ ] Link to "Join an existing organization" (placeholder)

**Dependencies:** FF-007, FF-009, SC-001, ORG-002

**Complexity:** M

**Priority:** P0

**Definition of Done:** User creates an org and lands on the dashboard.

---

### ORG-004: Organization Context Middleware (Backend)

**Title:** Create backend middleware for resolving and validating organization context

**Description:**
Create middleware (or a FastAPI dependency) that: reads `X-Org-Id` from the request header, validates that the authenticated user is an active member of that organization, loads the user's role in that org, and injects an `OrgContext` (org_id, org_name, user_role) into the request state. Raise `AuthorizationError` if the user is not a member.

**Business Value:** Every tenant-scoped endpoint depends on knowing which org the request is for and whether the user has access. This middleware centralizes that check.

**Acceptance Criteria:**
- [ ] `get_current_org()` dependency reads `X-Org-Id` header
- [ ] Validates the user has an active membership in the org
- [ ] Returns `OrgContext` with `org_id`, `org_name`, `user_role`, `membership_id`
- [ ] Raises `AuthorizationError` (403) if user is not a member
- [ ] Raises `ValidationError` (400) if `X-Org-Id` header is missing (on endpoints that require it)
- [ ] Caches membership lookup per request (not per session)

**Dependencies:** BF-001, BF-003, ORG-001, ID-012

**Complexity:** M

**Priority:** P0

**Definition of Done:** Dependency correctly resolves org context. Non-members get 403.

---

### ORG-005: Organization Switcher Component

**Title:** Build the organization switcher in the sidebar

**Description:**
Create an `OrgSwitcher` component that: shows the current org name and logo, opens a dropdown listing all orgs the user belongs to, allows switching between orgs, and includes a "Create new organization" option. Switching orgs updates the org context (stored in a React context or localStorage) and reloads the page data.

**Business Value:** Users who belong to multiple organizations need a way to switch between them. This is a core multi-tenancy UX requirement.

**Acceptance Criteria:**
- [ ] Displays current org name in the sidebar
- [ ] Dropdown lists all orgs the user is a member of (from `/api/v1/auth/me`)
- [ ] Clicking an org switches the active org context
- [ ] Switching invalidates React Query cache (data must reload for new org)
- [ ] "Create new organization" option navigates to `/create-org`
- [ ] Active org is persisted in localStorage (survives page refresh)
- [ ] If persisted org is no longer valid (user removed), fallback to first available org

**Dependencies:** FF-009, FF-010, SC-007, ID-011

**Complexity:** M

**Priority:** P1

**Definition of Done:** User can switch between orgs. Data reloads for the selected org.

---

### ORG-006: Invite Member Backend

**Title:** Create POST /api/v1/organizations/{org_id}/invitations endpoint

**Description:**
Create an endpoint for inviting new members to an organization. Accepts `email` and `role_id`. Creates an invitation record with status `pending` and an expiry (7 days). If the email already belongs to a Calyx user, the invitation can be accepted immediately. If not, it waits for signup.

**Business Value:** Organizations grow by inviting members. This is the primary user acquisition mechanism after the first user.

**Acceptance Criteria:**
- [ ] `POST /api/v1/organizations/{org_id}/invitations` requires `org_admin` or `manager` role
- [ ] Request body: `{ "email": "bob@acme.com", "role_id": "<uuid>" }`
- [ ] Creates invitation record with `pending` status and 7-day expiry
- [ ] Prevents duplicate invitations (same email, same org, still pending)
- [ ] Prevents inviting existing members (return 409)
- [ ] Role validation: cannot invite with a role higher than the inviter's own
- [ ] Returns 201 with the created invitation
- [ ] Audit log entry created
- [ ] (Future: trigger invitation email — for now, return the invitation token)

**Dependencies:** BF-001 through BF-009, ORG-001, ORG-004, ID-012, RBAC-003

**Complexity:** M

**Priority:** P1

**Definition of Done:** Org admin can create invitations. Duplicate and privilege escalation attempts are blocked.

---

### ORG-007: Accept Invitation Backend

**Title:** Create POST /api/v1/invitations/{invitation_id}/accept endpoint

**Description:**
Create an endpoint for accepting an organization invitation. Validates the invitation (exists, pending, not expired, email matches authenticated user). Creates a membership record. Marks the invitation as accepted.

**Business Value:** Completes the invitation flow. Invited users become org members.

**Acceptance Criteria:**
- [ ] `POST /api/v1/invitations/{invitation_id}/accept` requires authentication
- [ ] Validates invitation exists and is in `pending` status
- [ ] Validates invitation has not expired
- [ ] Validates authenticated user's email matches the invitation email
- [ ] Creates membership record with the invited role
- [ ] Updates invitation status to `accepted`
- [ ] Returns the created membership and organization
- [ ] Audit log entry created

**Dependencies:** BF-001 through BF-009, ORG-001, ID-012

**Complexity:** M

**Priority:** P1

**Definition of Done:** User with a valid invitation can accept it and become an org member.

---

### ORG-008: List Organization Members Backend

**Title:** Create GET /api/v1/organizations/{org_id}/members endpoint

**Description:**
Create an endpoint listing all members of the current organization. Returns paginated list of members with their user profile, role, and membership status. Supports filtering by role and status.

**Business Value:** Org admins and managers need to see who's in the organization and what roles they have.

**Acceptance Criteria:**
- [ ] `GET /api/v1/organizations/{org_id}/members` requires `member:list` permission
- [ ] Returns paginated list of `{ user: {...}, role: {...}, status, joined_at }`
- [ ] Supports cursor-based pagination
- [ ] Supports filtering by `role_id` and `status` query params
- [ ] Only returns members of the authenticated user's current org (enforced by middleware + RLS)
- [ ] Returns standard paginated response format

**Dependencies:** BF-001 through BF-011, ORG-001, ORG-004, ID-012, RBAC-003

**Complexity:** M

**Priority:** P1

**Definition of Done:** Endpoint returns the correct member list, paginated and filtered.

---

### ORG-009: Organization Settings Page

**Title:** Build the organization settings page

**Description:**
Create `src/app/(platform)/settings/organization/page.tsx` with a form showing org name and slug (editable by Org Admin). Include a danger zone with "Delete Organization" (behind a confirmation dialog). Display current member count and plan info (placeholder).

**Business Value:** Org admins need to manage basic organization settings. The settings page also hosts the danger zone for destructive actions.

**Acceptance Criteria:**
- [ ] Displays org name and slug in editable form fields
- [ ] Save button calls `PATCH /api/v1/organizations/{org_id}`
- [ ] Only `org_admin` can edit (other roles see read-only view)
- [ ] Danger zone: "Delete Organization" button behind a type-to-confirm dialog
- [ ] Shows current member count
- [ ] Success/error toasts on save
- [ ] Page uses `PageShell` component

**Dependencies:** FF-006, FF-009, SC-001, SC-002, SC-006, ORG-004

**Complexity:** M

**Priority:** P2

**Definition of Done:** Org admin can update org name. Delete confirmation works. Read-only for non-admins.

---

# Epic 6: RBAC

> **Epic Goal:** Permission checking infrastructure — backend dependency and frontend guard — that enforces the approved RBAC model.

---

### RBAC-001: Permission Checking Dependency (Backend)

**Title:** Create require_permission() FastAPI dependency

**Description:**
Create a parameterized FastAPI dependency `require_permission(permission_name)` that: loads the current user's role in the current org (from `get_current_org()`), loads the permissions for that role, and raises `AuthorizationError` (403) if the required permission is not in the set. This is the primary authorization gate for every protected endpoint.

**Business Value:** Every endpoint that performs a restricted action must check permissions. A reusable dependency ensures no endpoint forgets the check.

**Acceptance Criteria:**
- [ ] `require_permission("document:create")` is usable as `Depends(require_permission("document:create"))`
- [ ] Loads permissions from the `role_permissions` join based on the user's role
- [ ] Raises `AuthorizationError` with message "Insufficient permissions" on failure
- [ ] Permission check is O(1) — load permissions once per request, check set membership
- [ ] Works with all permissions in the catalog (§5.4)
- [ ] Cacheable — permission set for a role doesn't change within a request

**Dependencies:** BF-001, BF-003, BF-004, ORG-001, ORG-004, ID-012

**Complexity:** M

**Priority:** P0

**Definition of Done:** Endpoints using `require_permission()` reject users without the required permission.

---

### RBAC-002: Role Assignment Service

**Title:** Create service for assigning and updating member roles

**Description:**
Create a service method for changing a member's role within an organization. Validates: the caller has `member:update_role` permission, the target role is not higher than the caller's role (no privilege escalation), and the last `org_admin` cannot be demoted (the org must always have at least one admin).

**Business Value:** Role changes are a critical admin action. The business rules (no privilege escalation, protect last admin) must be enforced in the service layer.

**Acceptance Criteria:**
- [ ] `update_member_role(org_id, membership_id, new_role_id)` service method
- [ ] Validates caller has `member:update_role` permission
- [ ] Validates new role hierarchy is not above the caller's role
- [ ] Prevents demoting the last `org_admin` (returns 409 Conflict)
- [ ] Updates the membership record
- [ ] Audit log entry records the role change (old role → new role)
- [ ] Returns the updated membership

**Dependencies:** BF-001, BF-003, ORG-001, RBAC-001

**Complexity:** M

**Priority:** P1

**Definition of Done:** Role changes work. Privilege escalation and last-admin demotion are blocked.

---

### RBAC-003: Permission Guard Frontend Hook

**Title:** Create usePermission() hook for conditional UI rendering

**Description:**
Create `src/lib/hooks/use-permission.ts` with a `usePermission(permissionName)` hook that returns `{ hasPermission: boolean, isLoading: boolean }`. The hook checks the current user's role's permissions (loaded from the `/auth/me` response). Use this to conditionally render UI elements (e.g., hide "Invite Member" button if user lacks `member:invite` permission).

**Business Value:** UI must reflect the user's permissions. Showing buttons for actions the user can't perform creates frustration and wastes clicks (the backend would reject the request anyway).

**Acceptance Criteria:**
- [ ] `usePermission("member:invite")` returns `{ hasPermission: true/false, isLoading }`
- [ ] Permissions are derived from the user's current role and the role-permission mapping
- [ ] `isLoading` is true while the role/permission data is being fetched
- [ ] Role-permission data is cached (not re-fetched on every call)
- [ ] Works with all permissions in the catalog
- [ ] Optional: `<PermissionGate permission="member:invite">` component that conditionally renders children

**Dependencies:** FF-010, FF-012, ID-011

**Complexity:** M

**Priority:** P1

**Definition of Done:** UI elements are conditionally rendered based on the user's permissions.

---

### RBAC-004: Protect All Sprint 1 Endpoints

**Title:** Add permission checks to all existing endpoints

**Description:**
Review every endpoint created in Sprint 1 and add the appropriate `require_permission()` dependency. Create a matrix mapping endpoints to required permissions. Verify that unauthenticated requests return 401 and unauthorized requests return 403.

**Business Value:** No endpoint should be accessible without proper authorization. This ticket ensures the RBAC system is applied, not just built.

**Acceptance Criteria:**
- [ ] Every endpoint in the `organizations` module has permission checks
- [ ] Every endpoint in the `members` module has permission checks
- [ ] `complete-signup` and `auth/me` require only authentication (no role check)
- [ ] Health check requires no authentication
- [ ] Endpoint-permission matrix is documented
- [ ] Manual testing confirms 401 for no token, 403 for wrong role

**Dependencies:** RBAC-001, ORG-002 through ORG-008, ID-003, ID-011

**Complexity:** M

**Priority:** P0

**Definition of Done:** All endpoints enforce the correct permissions. Documented matrix.

---

### RBAC-005: Contextual Permission Utility

**Title:** Create shared utilities for contextual scope checks

**Description:**
Create `app/shared/authorization.py` with utility functions for common contextual checks: `is_workspace_member(user_id, workspace_id)`, `is_resource_owner(user_id, resource)`, `is_org_admin(user_id, org_id)`. These are used by services alongside `require_permission()` to enforce scope-level access control (ADR-010).

**Business Value:** Contextual checks are needed by multiple services. Centralizing them prevents inconsistent implementations.

**Acceptance Criteria:**
- [ ] `is_workspace_member()` queries workspace_members table
- [ ] `is_resource_owner()` checks `created_by` field on any resource
- [ ] `is_org_admin()` checks membership role
- [ ] All functions accept a database session and return boolean
- [ ] Functions are async-compatible
- [ ] Reusable across document, workspace, and memory services

**Dependencies:** BF-003, ORG-001

**Complexity:** S

**Priority:** P1

**Definition of Done:** Utility functions work correctly and are importable from `app.shared.authorization`.

---

# Epic 7: Testing (TEST)

> **Epic Goal:** Test infrastructure and foundational test suites that ensure quality from day one.

---

### TEST-001: Backend Test Infrastructure

**Title:** Set up pytest with async support and test database

**Description:**
Configure `pytest` with `pytest-asyncio` for async test support. Set up a test database (separate Supabase project or local PostgreSQL) with automatic schema setup and teardown. Create base test fixtures: `test_client` (async httpx client), `test_db` (database session), `test_settings` (test-specific configuration).

**Business Value:** Without test infrastructure, no tests can be written. This unblocks all backend testing.

**Acceptance Criteria:**
- [ ] `pytest` and `pytest-asyncio` configured in `pyproject.toml`
- [ ] `conftest.py` provides `test_client` fixture (FastAPI TestClient)
- [ ] `test_db` fixture provides a clean database session per test
- [ ] Test database is isolated from development database
- [ ] `pytest` runs from the project root and discovers all test files
- [ ] At least one smoke test passes: `test_health_check_returns_200`
- [ ] Coverage reporting configured with `pytest-cov`

**Dependencies:** BF-001, BF-002, BF-003, BF-010

**Complexity:** M

**Priority:** P0

**Definition of Done:** `pytest` runs, health check test passes, coverage report generates.

---

### TEST-002: Frontend Test Infrastructure

**Title:** Set up Vitest with React Testing Library

**Description:**
Configure Vitest as the test runner for the Next.js frontend. Set up React Testing Library for component testing. Configure jsdom environment. Create a test utilities file with common render helpers (render with providers, mock router, mock auth context).

**Business Value:** Without test infrastructure, no frontend tests can be written. This unblocks all frontend testing.

**Acceptance Criteria:**
- [ ] Vitest configured in `vitest.config.ts`
- [ ] React Testing Library installed and configured
- [ ] `@testing-library/jest-dom` matchers available
- [ ] Test utilities file provides `renderWithProviders()` that wraps with QueryClient, AuthProvider, etc.
- [ ] At least one smoke test passes: a component renders without crashing
- [ ] `npm run test` runs all tests
- [ ] Coverage reporting configured

**Dependencies:** FF-001, FF-004

**Complexity:** M

**Priority:** P1

**Definition of Done:** Vitest runs, smoke test passes, coverage report generates.

---

### TEST-003: Auth Flow Integration Tests

**Title:** Write integration tests for authentication endpoints

**Description:**
Write integration tests for: `POST /api/v1/auth/complete-signup` (create profile, idempotent), `GET /api/v1/auth/me` (returns user context), unauthenticated access (returns 401), invalid JWT (returns 401). Test with valid and invalid JWTs.

**Business Value:** Authentication is the security perimeter. Bugs here compromise the entire system. Integration tests catch regressions.

**Acceptance Criteria:**
- [ ] Test: `complete-signup` with valid JWT creates a user profile
- [ ] Test: `complete-signup` is idempotent (calling twice returns the same profile)
- [ ] Test: `auth/me` returns the correct user profile and memberships
- [ ] Test: request without Authorization header returns 401
- [ ] Test: request with expired JWT returns 401
- [ ] Test: request with malformed JWT returns 401
- [ ] All tests pass in CI

**Dependencies:** TEST-001, ID-003, ID-011, ID-012

**Complexity:** M

**Priority:** P0

**Definition of Done:** All auth integration tests pass. No false positives or negatives.

---

### TEST-004: Multi-Tenant Isolation Tests

**Title:** Write security tests proving cross-tenant isolation

**Description:**
Write tests that prove tenant isolation is enforced. Create two orgs with two users. Verify that User A cannot: read Org B's data, list Org B's members, create resources in Org B, or access Org B's audit logs. Test at both the API and RLS levels.

**Business Value:** Cross-tenant data leaks are a critical severity security vulnerability. These tests are a permanent safety net.

**Acceptance Criteria:**
- [ ] Test: User in Org A cannot list members of Org B (returns 403)
- [ ] Test: User in Org A cannot create resources in Org B
- [ ] Test: User in Org A cannot read Org B's organization details
- [ ] Test: Direct database query with wrong `org_id` returns empty (RLS test)
- [ ] Test: Omitting `X-Org-Id` header returns 400
- [ ] Test: Sending `X-Org-Id` for an org the user is not a member of returns 403
- [ ] All tests pass in CI

**Dependencies:** TEST-001, ORG-001, ORG-002, ORG-004

**Complexity:** L

**Priority:** P0

**Definition of Done:** All isolation tests pass. Zero cross-tenant data leaks detectable.

---

### TEST-005: RBAC Permission Tests

**Title:** Write tests for every role-permission boundary

**Description:**
Write tests verifying that each role can only perform its authorized actions. For each endpoint with a permission check, verify: `org_admin` can access, `viewer` cannot (for write endpoints), `employee` cannot access admin endpoints, etc. Test privilege escalation prevention.

**Business Value:** RBAC bugs are authorization vulnerabilities. Comprehensive tests ensure every permission boundary holds.

**Acceptance Criteria:**
- [ ] Test: `org_admin` can invite members
- [ ] Test: `employee` cannot invite members (returns 403)
- [ ] Test: `viewer` cannot create resources (returns 403)
- [ ] Test: `manager` cannot change org settings (returns 403)
- [ ] Test: cannot assign a role higher than the caller's own role
- [ ] Test: cannot demote the last org_admin
- [ ] At least one test per unique permission boundary
- [ ] All tests pass in CI

**Dependencies:** TEST-001, RBAC-001 through RBAC-004, ORG-006

**Complexity:** L

**Priority:** P0

**Definition of Done:** All RBAC tests pass. Every permission boundary is tested.

---

# Epic 8: Documentation (DOC)

> **Epic Goal:** Developer-facing documentation that enables any engineer to set up, contribute to, and understand the project.

---

### DOC-001: Project README

**Title:** Write the root README.md

**Description:**
Create a comprehensive README for the project root. Include: project description, tech stack, prerequisites, setup instructions (quick start), how to run (frontend + backend), how to run tests, project structure overview, link to ADRs and design docs, and contributing guidelines link.

**Business Value:** The README is the first thing any new contributor reads. A clear README reduces onboarding friction.

**Acceptance Criteria:**
- [ ] Project name, description, and mission statement
- [ ] Tech stack summary with versions
- [ ] Prerequisites (Node.js version, Python version, Supabase account)
- [ ] Quick start: step-by-step from clone to running app
- [ ] How to run frontend (`npm run dev`)
- [ ] How to run backend (`uvicorn` command)
- [ ] How to run tests (frontend + backend)
- [ ] Project structure overview (top-level directories explained)
- [ ] Links to design documents and ADRs
- [ ] License placeholder

**Dependencies:** BF-001, FF-001

**Complexity:** S

**Priority:** P1

**Definition of Done:** A new engineer can follow the README to run the project from scratch.

---

### DOC-002: Environment Setup Guide

**Title:** Write a detailed environment setup guide

**Description:**
Create `docs/setup.md` with step-by-step instructions for setting up the development environment: Supabase project creation, environment variable configuration, database schema setup, Google OAuth configuration, and common troubleshooting steps.

**Business Value:** Environment setup is the most common source of developer friction. A detailed guide prevents hours of debugging.

**Acceptance Criteria:**
- [ ] Supabase project creation steps with screenshots or descriptions
- [ ] Environment variable setup for both frontend and backend
- [ ] Database schema initialization steps
- [ ] Google OAuth setup in Google Cloud Console + Supabase
- [ ] How to verify each dependency (DB connection, auth, storage)
- [ ] Troubleshooting section (common errors and solutions)
- [ ] Platform-specific notes (Windows, macOS, Linux)

**Dependencies:** BF-002, FF-008, ID-001

**Complexity:** S

**Priority:** P1

**Definition of Done:** A developer on a fresh machine can follow the guide to a working environment.

---

### DOC-003: API Documentation Setup

**Title:** Configure FastAPI auto-generated API documentation

**Description:**
Ensure FastAPI's auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`) are accessible in development and staging. Configure API metadata (title, description, version, contact). Verify that all endpoints appear with correct request/response schemas.

**Business Value:** Auto-generated API docs reduce documentation maintenance and serve as a live reference for frontend developers.

**Acceptance Criteria:**
- [ ] `/docs` (Swagger UI) is accessible in development
- [ ] `/redoc` (ReDoc) is accessible in development
- [ ] API metadata shows "Calyx API", version, and description
- [ ] All endpoints appear with correct HTTP methods and paths
- [ ] Request bodies show Pydantic model schemas with field descriptions
- [ ] Response models show the standard response format
- [ ] Auth endpoints are marked with security requirements
- [ ] Docs are disabled in production (configurable via `APP_ENV`)

**Dependencies:** BF-001, BF-002

**Complexity:** S

**Priority:** P2

**Definition of Done:** Swagger UI and ReDoc render all endpoints with correct schemas.

---

### DOC-004: Contributing Guide

**Title:** Write CONTRIBUTING.md with development workflow

**Description:**
Create `CONTRIBUTING.md` documenting: branch naming conventions, commit message format (Conventional Commits), PR process, code review expectations, how to run linters and formatters, testing requirements before merge, and the Definition of Done checklist.

**Business Value:** Establishes engineering culture from day one. Every contributor follows the same process.

**Acceptance Criteria:**
- [ ] Branch strategy documented (trunk-based with short-lived feature branches)
- [ ] Commit format documented (Conventional Commits with examples)
- [ ] PR template referenced or included
- [ ] Code review expectations (what reviewers look for)
- [ ] How to run linters: `ruff` (Python), `eslint` (TypeScript), `prettier` (formatting)
- [ ] Testing requirements: what tests must pass before merge
- [ ] Definition of Done checklist (from §13.8 of the Design Review)

**Dependencies:** None

**Complexity:** S

**Priority:** P2

**Definition of Done:** A new contributor can read this and submit a properly formatted PR.

---

# Sprint Summary

## Ticket Count by Epic

| Epic | Tickets | P0 | P1 | P2 |
|---|---|---|---|---|
| Backend Foundation (BF) | 11 | 6 | 5 | 0 |
| Frontend Foundation (FF) | 12 | 7 | 4 | 1 |
| Shared Components (SC) | 8 | 2 | 4 | 2 |
| Identity (ID) | 12 | 7 | 4 | 1 |
| Organizations (ORG) | 9 | 4 | 4 | 1 |
| RBAC | 5 | 2 | 3 | 0 |
| Testing (TEST) | 5 | 3 | 1 | 1 |
| Documentation (DOC) | 4 | 0 | 2 | 2 |
| **Total** | **66** | **31** | **27** | **8** |

## Critical Path

```
BF-001 → BF-002 → BF-003 ──────────────────────────┐
  │                                                   │
  ├→ BF-004 → BF-005                                 │
  │                                                   │
  ├→ BF-007 → BF-009                                 │
  │                                                   │
  └→ BF-006                                          │
                                                      ▼
FF-001 → FF-008 → FF-010 → FF-009 ──→ ID-012 → ORG-004 → RBAC-001
  │                  │                    │
  ├→ FF-002 → FF-003 │                   ├→ ID-003 → ID-011
  │                  │                    │
  ├→ FF-005          ├→ FF-011           └→ ORG-002 → ORG-003
  │                  │
  └→ FF-004 ─────────┘
```

## Suggested Execution Order

1. **Days 1–2:** BF-001 through BF-009, FF-001 through FF-003 (in parallel, backend + frontend)
2. **Days 3–4:** BF-010, BF-011, FF-004 through FF-008, ID-001, SC-001 through SC-003
3. **Days 5–6:** FF-009 through FF-012, ID-012, SC-006 through SC-008, TEST-001
4. **Days 7–8:** ID-002 through ID-005, ORG-001, ORG-002, ID-003, ID-011
5. **Days 9–10:** ID-006 through ID-010, ORG-003 through ORG-005, RBAC-001
6. **Days 11–12:** ORG-006 through ORG-008, RBAC-002 through RBAC-005, TEST-002
7. **Days 13–14:** TEST-003 through TEST-005, DOC-001 through DOC-004, SC-004, SC-005, ORG-009

---

*End of Sprint 1 Backlog.*
