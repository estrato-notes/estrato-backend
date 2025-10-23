import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user_id

from .schemas import DashboardResponse
from .service import DashboardService as dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/",
    response_model=DashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Lista as estatísticas do Dashboard",
)
def get_dashboard_data(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
) -> DashboardResponse:
    """Retorna as listas com as estatísticas que o dashboard trata"""
    return dashboard_service.get_dashboard_data(db, user_id)
