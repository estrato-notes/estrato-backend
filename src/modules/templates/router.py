import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.models import Template

from .schemas import TemplateCreate, TemplateResponse, TemplateUpdate
from .service import TemplateService as template_service

router = APIRouter(prefix="/templates", tags=["Templates"])


@router.post(
    "/",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo Template",
)
def create_template(
    template_data: TemplateCreate, db: Annotated[Session, Depends(get_db)]
) -> Template:
    """Cria um novo template"""
    return template_service.create_template(db, template_data)


@router.get(
    "/",
    response_model=list[TemplateResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista para todos os Templates",
)
def get_all_templates(db: Annotated[Session, Depends(get_db)]) -> list[Template]:
    """Retorna uma lista com todos os templates"""
    return template_service.get_all_templates(db)


@router.get(
    "/{template_id}",
    response_model=TemplateResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca de Template por ID",
)
def get_template_by_id(
    template_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
) -> Template:
    """Busca e retorna um template de acordo com o ID passado"""
    return template_service.get_template_by_id(db, template_id)


@router.patch(
    "/{template_id}",
    response_model=TemplateResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar informações de um template",
)
def update_template(
    template_id: uuid.UUID,
    template_data: TemplateUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Template:
    """Edita as informações do template referente ao ID passado"""
    return template_service.update_template(db, template_id, template_data)


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar template por ID",
)
def delete_template(template_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    """Remove do Banco o template referente ao ID passado"""
    template_service.delete_template_by_id(db, template_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
