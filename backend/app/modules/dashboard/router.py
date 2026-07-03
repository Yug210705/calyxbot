import uuid
from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.dashboard.schemas import DashboardResponse
from app.modules.dashboard.services import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    x_organization_id: uuid.UUID = Header(..., alias="X-Organization-Id"),
    session: AsyncSession = Depends(get_db),
):
    service = DashboardService(session)
    return await service.get_dashboard(x_organization_id)
