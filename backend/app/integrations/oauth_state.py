import time
import uuid
import jwt
from typing import Any

from app.core.config import get_settings

class OAuthStateError(Exception):
    pass

def create_oauth_state(org_id: uuid.UUID, user_id: uuid.UUID, provider: str) -> str:
    """Creates a signed JWT state token for OAuth flow."""
    settings = get_settings()
    
    payload = {
        "org_id": str(org_id),
        "user_id": str(user_id),
        "provider": provider,
        "nonce": str(uuid.uuid4()),
        "issued_at": int(time.time()),
        "exp": int(time.time()) + 3600, # 1 hour expiry
    }
    
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")

def parse_oauth_state(state: str) -> dict[str, Any]:
    """Validates and parses the OAuth state."""
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            state,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise OAuthStateError("OAuth state has expired")
    except jwt.InvalidTokenError:
        raise OAuthStateError("Invalid OAuth state token")
