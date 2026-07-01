"""Authentication provider abstractions."""

import abc

import jwt

from app.core.config import get_settings


class JWKSProvider(abc.ABC):
    """Abstract interface for fetching JWKS signing keys."""

    @abc.abstractmethod
    def get_signing_key(self, token: str) -> str:
        """Fetch the public signing key for a given JWT token."""
        pass

class SupabaseJWKSProvider(JWKSProvider):
    """Production provider that fetches JWKS from Supabase."""

    def __init__(self):
        settings = get_settings()
        jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def get_signing_key(self, token: str) -> str:
        signing_key = self.jwks_client.get_signing_key_from_jwt(token)
        return signing_key.key

class FakeJWKSProvider(JWKSProvider):
    """Fake provider for testing environments."""

    def __init__(self, secret: str = "test-secret"):
        self.secret = secret

    def get_signing_key(self, token: str) -> str:
        # In tests, we often just use HS256 with a static secret,
        # so we return the secret string instead of a public key.
        return self.secret
