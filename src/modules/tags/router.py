import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import TagCreate, TagResponse, TagUpdate
from .service import TagService as tag_service

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova Tag",
)
def create_tag(tag_data: TagCreate, db: Annotated[Session, Depends(get_db)]):
    """Cria uma nova tag"""
    return tag_service.create_tag(db, tag_data)


@router.get(
    "/",
    response_model=list[TagResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista para todas as Tags",
)
def get_all_tags(db: Annotated[Session, Depends(get_db)]):
    """Retorna uma lista com todas as tags"""
    return tag_service.get_all_tags(db)


@router.get(
    "/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca Tag por ID",
)
def get_tag_by_id(tag_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    """Busca e retorna uma tag referente ao ID passado"""
    return tag_service.get_tag_by_id(db, tag_id)


@router.patch(
    "/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar as informações de uma Tag",
)
def update_tag(
    tag_id: uuid.UUID,
    tag_update_data: TagUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    """Atualiza as informações de uma tag"""
    return tag_service.update_tag(db, tag_id, tag_update_data)


@router.delete(
    "/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletar tag por ID"
)
def delete_tag(tag_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    """Deleta uma tag do Banco"""
    tag_service.delete_tag(db, tag_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
