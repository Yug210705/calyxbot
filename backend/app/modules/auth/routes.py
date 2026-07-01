"""Authentication API routes."""

import uuid
from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, verify_jwt
from app.modules.auth.models import User
from app.modules.auth.schemas import (
    AuthBootstrapResponse,
    CompleteSignupRequest,
    UserBase,
)
from app.shared.response import SuccessResponse, create_success_response

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/complete-signup", response_model=SuccessResponse[AuthBootstrapResponse])
async def complete_signup(
    payload: CompleteSignupRequest,
    jwt_payload: Annotated[dict, Depends(verify_jwt)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> SuccessResponse[AuthBootstrapResponse]:
    """
    Called by the frontend after a successful Supabase signup or OAuth login.
    Syncs the user profile into the Calyx database.
    """
    user_id_str = jwt_payload.get("sub")
    email = jwt_payload.get("email")

    if not user_id_str or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JWT payload missing required 'sub' or 'email' claims."
        )

    user_id = uuid.UUID(user_id_str)

    # Check if user already exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        # Create new user in our DB
        user = User(
            id=user_id,
            email=email,
            full_name=payload.full_name or jwt_payload.get("user_metadata", {}).get("name"),
            is_active=True
        )
        db.add(user)
        # Commit manually here since the dependency doesn't auto-commit anymore
        await db.commit()
        await db.refresh(user)
        logger.info("New user synchronized from Auth provider", user_id=str(user_id), email=email)
    else:
        # User already exists (e.g. repeated OAuth login), this is fine.
        logger.debug("User already exists during complete-signup", user_id=str(user_id))

    # In the future, this is where we would check for pending invitations by email
    # and automatically attach them to an organization.

    user_base = UserBase.model_validate(user)

    bootstrap_data = AuthBootstrapResponse(
        user=user_base,
        current_organization=None, # No org context at signup yet
        permissions=[],
        feature_flags={},
        api_version="v1.0"
    )

    return create_success_response(data=bootstrap_data)


@router.get("/me", response_model=SuccessResponse[AuthBootstrapResponse])
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> SuccessResponse[AuthBootstrapResponse]:
    """
    Returns the current user profile, organization context, and permissions.
    Acts as the frontend bootstrap endpoint.
    """
    user_base = UserBase.model_validate(current_user)

    # Determine current organization context (simplified for MVP: just grab the first one, or none)
    # This will be expanded in the Organizations ticket.

    bootstrap_data = AuthBootstrapResponse(
        user=user_base,
        current_organization=None,
        permissions=[],
        feature_flags={},
        api_version="v1.0"
    )

    return create_success_response(data=bootstrap_data)
