from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.auth.models import User
from app.modules.members.invitation_service import (
    InvitationAlreadyAcceptedError,
    InvitationError,
    InvitationExpiredError,
    InvitationRevokedError,
    InvitationService,
)
from app.modules.members.repositories import (
    SQLAlchemyInvitationRepository,
    SQLAlchemyMembershipRepository,
    SQLAlchemyRoleRepository,
)
from app.modules.members.schemas import MembershipResponse
from app.shared.events import event_bus
from app.shared.response import (
    SuccessResponse,
    create_error_response,
    create_success_response,
)

router = APIRouter(prefix="/invitations", tags=["Invitations"])


def get_invitation_service(db: AsyncSession = Depends(get_db)) -> InvitationService:
    invitation_repo = SQLAlchemyInvitationRepository(db)
    membership_repo = SQLAlchemyMembershipRepository(db)
    role_repo = SQLAlchemyRoleRepository(db)
    return InvitationService(db, invitation_repo, membership_repo, role_repo, event_bus)


@router.post("/{token}/accept", response_model=SuccessResponse[MembershipResponse])
async def accept_invitation(
    token: str,
    user: User = Depends(get_current_user),
    service: InvitationService = Depends(get_invitation_service),
    db: AsyncSession = Depends(get_db),
):
    """
    Accept an invitation using its raw token.
    The user must be logged in.
    """
    try:
        membership = await service.accept_invitation(token, user.id)

        # We need to explicitly commit because accept_invitation modifies multiple records
        # and doesn't call commit internally for the invitation status update yet (it relies on the session)
        await db.commit()

        return create_success_response(data=MembershipResponse.model_validate(membership))

    except InvitationAlreadyAcceptedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                code="INVITATION_ALREADY_ACCEPTED",
                message="This invitation has already been accepted."
            ).model_dump()
        )
    except InvitationExpiredError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                code="INVITATION_EXPIRED",
                message="This invitation has expired."
            ).model_dump()
        )
    except InvitationRevokedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                code="INVITATION_REVOKED",
                message="This invitation has been revoked."
            ).model_dump()
        )
    except InvitationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                code="INVITATION_INVALID",
                message=str(e)
            ).model_dump()
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred while accepting the invitation.",
            ).model_dump()
        )
