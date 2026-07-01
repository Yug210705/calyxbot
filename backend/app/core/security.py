"""Security utilities.

JWT validation, current user extraction, and permission checking
dependencies for FastAPI route protection.
"""

import uuid
from typing import Annotated

import jwt
import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_providers import JWKSProvider, SupabaseJWKSProvider
from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.modules.auth.models import User

logger = structlog.get_logger(__name__)

security = HTTPBearer()

def get_jwks_provider() -> JWKSProvider:
    """Dependency that provides the JWKS provider."""
    # In production, this returns the Supabase provider.
    # In tests, this dependency is overridden.
    return SupabaseJWKSProvider()

async def verify_jwt(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    settings: Annotated[Settings, Depends(get_settings)],
    jwks_provider: Annotated[JWKSProvider, Depends(get_jwks_provider)]
) -> dict:
    """Validate Supabase JWT and return the payload."""
    token = credentials.credentials
    try:
        # Supabase now uses ES256 for new projects, so we verify using JWKS
        signing_key = jwks_provider.get_signing_key(token)
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["ES256", "RS256", "HS256"],
            audience="authenticated",
            leeway=60
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.PyJWTError as e:
        logger.warning("JWT validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

async def get_current_user(
    payload: Annotated[dict, Depends(verify_jwt)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """Fetch the corresponding application user from a validated JWT."""
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid subject identifier",
        )

    # Fetch user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in application database",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    return user
