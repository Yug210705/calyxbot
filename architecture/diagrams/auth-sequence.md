# Authentication Sequence Diagrams

**Version:** 1.0
**Status:** Approved
**Last Updated:** 2026-06-30
**Owner:** Architecture Team
**Related Documents:**
- [Security Model](../system/security-model.md)

---

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
