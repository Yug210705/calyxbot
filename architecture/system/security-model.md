# Security & Authentication Model

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [RBAC](../system/rbac.md)

---

## 4.1 Authentication Strategy

Calyx delegates identity management to **Supabase Auth**. This gives us:

- Battle-tested JWT issuance and validation
- Built-in email verification and password reset flows
- Google OAuth support out of the box
- Refresh token rotation
- Session management

Our application layer adds:

- Organization context resolution (which org is the user operating in?)
- Custom JWT claims for RBAC (role, org_id)
- Membership validation

## 4.2 Email Signup Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Next.js Frontend
    participant Supabase as Supabase Auth
    participant Backend as FastAPI Backend
    participant DB as PostgreSQL

    User->>Frontend: Fill signup form (name, email, password)
    Frontend->>Frontend: Client-side validation
    Frontend->>Supabase: supabase.auth.signUp({email, password, metadata: {name}})
    Supabase->>Supabase: Create user record
    Supabase->>User: Send verification email
    Supabase-->>Frontend: Return user (email_confirmed = false)
    Frontend->>Frontend: Show "Check your email" screen

    User->>Supabase: Click verification link
    Supabase->>Supabase: Mark email_confirmed = true
    Supabase-->>Frontend: Redirect to app with session

    Frontend->>Backend: POST /api/v1/auth/complete-signup (with JWT)
    Backend->>Backend: Validate JWT, extract user info
    Backend->>DB: Create user profile record
    Backend->>DB: Check for pending org invitations by email
    alt Has pending invitation
        Backend->>DB: Create membership record, mark invitation accepted
        Backend-->>Frontend: Return {user, organization, role}
    else No invitation
        Backend-->>Frontend: Return {user, organization: null}
        Frontend->>Frontend: Redirect to "Create or Join Organization" flow
    end
```

## 4.3 Google OAuth Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Next.js Frontend
    participant Supabase as Supabase Auth
    participant Google as Google OAuth
    participant Backend as FastAPI Backend
    participant DB as PostgreSQL

    User->>Frontend: Click "Continue with Google"
    Frontend->>Supabase: supabase.auth.signInWithOAuth({provider: 'google'})
    Supabase->>Google: Redirect to Google consent screen
    User->>Google: Grant consent
    Google->>Supabase: Return authorization code
    Supabase->>Google: Exchange code for tokens
    Supabase->>Supabase: Create or link user, set email_confirmed = true
    Supabase-->>Frontend: Redirect to app with session tokens

    Frontend->>Backend: POST /api/v1/auth/complete-signup (with JWT)
    Note over Backend: Same flow as email signup from here
    Backend->>DB: Upsert user profile (idempotent)
    Backend->>DB: Check for pending invitations
    Backend-->>Frontend: Return {user, organization}
```

## 4.4 Login Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Next.js Frontend
    participant Supabase as Supabase Auth
    participant Backend as FastAPI Backend

    User->>Frontend: Enter email + password
    Frontend->>Supabase: supabase.auth.signInWithPassword({email, password})
    alt Valid credentials
        Supabase-->>Frontend: Return {access_token, refresh_token, user}
        Frontend->>Frontend: Store tokens (httpOnly cookie via Supabase client)
        Frontend->>Backend: GET /api/v1/auth/me (with access_token)
        Backend->>Backend: Validate JWT, load user profile + memberships
        Backend-->>Frontend: Return {user, organizations, current_org}
        Frontend->>Frontend: Redirect to dashboard
    else Invalid credentials
        Supabase-->>Frontend: Return error
        Frontend->>Frontend: Show error message (generic: "Invalid email or password")
    end
```

## 4.5 Session Lifecycle

| Event | Behavior |
|---|---|
| **Login** | Supabase issues an access token (JWT, ~1 hour TTL) and a refresh token (~30 days TTL, rotated on use). |
| **Authenticated request** | Frontend attaches access token as `Authorization: Bearer <token>`. Backend validates signature, expiry, and claims. |
| **Token expiry** | Supabase client SDK automatically uses the refresh token to obtain a new access token. This is transparent to the user. |
| **Refresh token rotation** | Each time a refresh token is used, Supabase issues a new one and invalidates the old one. This limits the window of a stolen refresh token. |
| **Logout** | Frontend calls `supabase.auth.signOut()`. Supabase invalidates the refresh token. Frontend clears local state. |
| **Forced logout** | Org Admin deactivates a user → backend revokes their sessions via Supabase Admin API → user is forced to re-authenticate on next request. |
| **Inactivity timeout** | Handled by access token expiry. If the user is inactive beyond the refresh token lifetime, they must re-authenticate. |

## 4.6 Password Reset Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Next.js Frontend
    participant Supabase as Supabase Auth

    User->>Frontend: Click "Forgot Password"
    Frontend->>Frontend: Show email input form
    User->>Frontend: Enter email
    Frontend->>Supabase: supabase.auth.resetPasswordForEmail(email)
    Supabase-->>Frontend: Return success (always, to prevent email enumeration)
    Frontend->>Frontend: Show "Check your email" message

    Note over Supabase: Only sends email if account exists

    User->>Supabase: Click reset link in email
    Supabase-->>Frontend: Redirect to /reset-password with recovery token
    Frontend->>Frontend: Show new password form
    User->>Frontend: Enter new password
    Frontend->>Supabase: supabase.auth.updateUser({password: newPassword})
    Supabase->>Supabase: Update password, invalidate old sessions
    Supabase-->>Frontend: Return success
    Frontend->>Frontend: Redirect to login
```

## 4.7 Email Verification

- **On signup:** Supabase sends a verification email automatically. The user cannot access protected routes until email is verified.
- **Resend:** The frontend provides a "Resend verification email" action, which calls `supabase.auth.resend()`.
- **Enforcement:** The backend middleware checks the `email_confirmed` claim in the JWT. Unverified users receive a `403 Forbidden` with a clear message.
- **Google OAuth:** Email is automatically verified (Google has already verified it).

---
