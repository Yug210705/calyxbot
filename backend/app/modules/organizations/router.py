import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.auth.models import User
from app.modules.members.invitation_schemas import (
    InvitationCreate,
    InvitationResponse,
    InvitationWithToken,
)
from app.modules.members.invitation_service import InvitationService
from app.modules.members.repositories import (
    SQLAlchemyInvitationRepository,
    SQLAlchemyMembershipRepository,
    SQLAlchemyRoleRepository,
)
from app.modules.members.schemas import MembershipResponse, PaginatedMembershipResponse
from app.modules.members.services import MembershipService
from app.shared.events import event_bus
from app.shared.response import (
    SuccessResponse,
    create_error_response,
    create_success_response,
)

from .repositories import SQLAlchemyOrganizationRepository
from .schemas import OrganizationCreate, OrganizationResponse
from .services import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])

def get_organization_service(db: AsyncSession = Depends(get_db)) -> OrganizationService:
    org_repo = SQLAlchemyOrganizationRepository(db)
    membership_repo = SQLAlchemyMembershipRepository(db)
    role_repo = SQLAlchemyRoleRepository(db)
    return OrganizationService(db, org_repo, membership_repo, role_repo, event_bus)


@router.post("", response_model=SuccessResponse[OrganizationResponse], status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate,
    user: User = Depends(get_current_user),
    service: OrganizationService = Depends(get_organization_service),
    idempotency_key: Annotated[str | None, Header()] = None
):
    # Note: A real implementation for idempotency_key would check Redis or a DB table
    # to see if this key has already been processed for this user/endpoint.
    # For MVP, we pass it but rely on the unique slug constraint as the primary idempotency fallback.

    try:
        org = await service.create_organization(user.id, data)
        return create_success_response(
            data=OrganizationResponse.model_validate(org).model_dump(),
            meta={"idempotency_key": idempotency_key} if idempotency_key else None
        )
    except ValueError as e:
        # Returning a proper FastAPI exception or returning the error payload directly.
        # But if response_model is dict, returning Pydantic model directly might require model_dump.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                code="ORGANIZATION_CREATION_FAILED",
                message=str(e),
            ).model_dump()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred while creating the organization.",
            ).model_dump()
        )

def get_membership_service(db: AsyncSession = Depends(get_db)) -> MembershipService:
    membership_repo = SQLAlchemyMembershipRepository(db)
    role_repo = SQLAlchemyRoleRepository(db)
    return MembershipService(membership_repo, role_repo)

def get_invitation_service(db: AsyncSession = Depends(get_db)) -> InvitationService:
    invitation_repo = SQLAlchemyInvitationRepository(db)
    membership_repo = SQLAlchemyMembershipRepository(db)
    role_repo = SQLAlchemyRoleRepository(db)
    return InvitationService(db, invitation_repo, membership_repo, role_repo, event_bus)

@router.post("/{org_id}/invitations", response_model=SuccessResponse[InvitationWithToken], status_code=status.HTTP_201_CREATED)
async def create_organization_invitation(
    org_id: uuid.UUID,
    data: InvitationCreate,
    user: User = Depends(get_current_user),
    membership_service: MembershipService = Depends(get_membership_service),
    invitation_service: InvitationService = Depends(get_invitation_service),
    db: AsyncSession = Depends(get_db),
):
    try:
        # Check permissions
        has_access = await membership_service.check_permission(user.id, org_id, "invitation.create")
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=create_error_response(
                    code="FORBIDDEN",
                    message="You do not have permission to invite members to this organization."
                ).model_dump()
            )

        invitation, raw_token = await invitation_service.create_invitation(
            organization_id=org_id,
            email=data.email,
            role_name=data.role,
            inviter_id=user.id,
        )

        return create_success_response(
            data=InvitationWithToken(
                invitation=InvitationResponse.model_validate(invitation),
                # Frontend will generate the actual absolute URL for the email
                invite_url=f"/api/v1/invitations/{raw_token}/accept" # Provide path placeholder for MVP
            )
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                code="INVALID_ROLE",
                message=str(e),
            ).model_dump()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred while creating the invitation.",
            ).model_dump()
        )

@router.get("/{org_id}/members", response_model=SuccessResponse[PaginatedMembershipResponse])
async def get_organization_members(
    org_id: uuid.UUID,
    user: User = Depends(get_current_user),
    service: MembershipService = Depends(get_membership_service),
    limit: int = 50,
    offset: int = 0
):
    try:
        # Check if the user is a member of the organization (basic authorization)
        # In a real app we'd use a dedicated dependency like get_current_user_org_member
        has_access = await service.check_permission(user.id, org_id, "membership.read")
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=create_error_response(
                    code="FORBIDDEN",
                    message="You do not have permission to view members of this organization."
                ).model_dump()
            )

        members = await service.get_organization_members(org_id, limit, offset)

        return create_success_response(
            data=PaginatedMembershipResponse(
                items=[MembershipResponse.model_validate(m) for m in members],
                total=len(members), # Simplification. Real app needs count query
                limit=limit,
                offset=offset
            )
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred while fetching members.",
            ).model_dump()
        )
