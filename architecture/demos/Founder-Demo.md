# Founder Demo (10 Minutes)

## Objective
Showcase the complete onboarding and enterprise administration flow for a prospective B2B client.

## Flow

### Phase 1: Onboarding (0:00 - 3:00)
- **Sign Up:** Walk through the Supabase-powered authentication. Mention secure JWTs.
- **Organization Creation:** Create "Stark Industries". Explain that the slug `stark-industries` is globally unique and serves as the tenant boundary.

### Phase 2: Role Management & Invitations (3:00 - 6:00)
- **Invite Flow:** Navigate to the Members dashboard.
- Invite `tony@stark.com` as Owner.
- Invite `pepper@stark.com` as Admin.
- Invite `happy@stark.com` as Employee.
- Explain the underlying Role-Based Access Control matrix. The backend strictly evaluates permissions like `organization.settings` rather than hardcoded roles.

### Phase 3: Edge Cases & Concurrency (6:00 - 8:00)
- **Revoke Invite:** Revoke Happy's invitation. Explain that the status immediately turns to `revoked`.
- Attempt to accept the revoked invite (show the error).
- Explain that double-accepts are handled gracefully via database unique constraints.

### Phase 4: Audit Logging (8:00 - 10:00)
- Show the backend logs or an internal admin view of the Audit Logs.
- Point out that every action (Organization Created, Invitation Sent, Invitation Revoked) is immutably logged with an `org_id`, `user_id`, and `correlation_id`.
- Conclude the demo by summarizing the enterprise readiness.
