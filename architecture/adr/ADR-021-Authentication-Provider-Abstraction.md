# ADR 021: Authentication Provider Abstraction

## Status
Accepted

## Context
During the implementation of the Auth module in Sprint 1, our JWT validation relied on `jwt.PyJWKClient` being instantiated at the module level in `security.py`. This tightly coupled our authentication layer to Supabase and made live network requests to fetch the JSON Web Key Set (JWKS) during offline unit tests. This resulted in flaky tests, network errors in CI/CD, and a violation of our architectural principle that infrastructure concerns should be isolated. Furthermore, as an enterprise application, Calyx may need to support multiple identity providers (Auth0, Keycloak, Azure AD) in the future.

## Decision
We will introduce an Authentication Provider abstraction.
1. Create a `JWKSProvider` interface.
2. Implement a `SupabaseJWKSProvider` that wraps the `PyJWKClient` logic for production.
3. Implement a `FakeJWKSProvider` that returns a static secret for testing environments.
4. Update `security.py` to accept the `JWKSProvider` as an injected dependency (`Depends(get_jwks_provider)`).
5. In our test suite (`conftest.py`), use FastAPI's `dependency_overrides` to inject the `FakeJWKSProvider`.

## Consequences
- **Positive:** Unit tests are now completely network-isolated and deterministic.
- **Positive:** We can seamlessly swap identity providers by writing a new provider class.
- **Negative:** Slightly more boilerplate in `security.py` dependency injection.
