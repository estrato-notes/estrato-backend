"""Router para ações relacionadas ao usuário"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user_id

from .service import UserService as user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.delete(
    "/me/data",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui todos os dados do usuário logado",
)
def delete_all_user_data(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
):
    """
    Exclui todos os cadernos, notas, tags e templates
    associados ao usuário autenticado.
    """
    user_service.clear_all_user_data(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
