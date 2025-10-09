import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import NotebookCreate, NotebookResponse, NotebookUpdate
from .service import NotebookService as notebook_service

router = APIRouter(prefix="/notebooks", tags=["Notebooks"])


@router.post(
    "/",
    response_model=NotebookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo Caderno",
)
def create_notebook(
    notebook_data: NotebookCreate, db: Annotated[Session, Depends(get_db)]
):
    """Cria um novo notebook"""
    new_notebook = notebook_service.create_notebook(db, notebook_data)
    return new_notebook


@router.get(
    "/",
    response_model=list[NotebookResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista para todas os Cadernos",
)
def get_all_notebooks(db: Annotated[Session, Depends(get_db)]):
    """Retorna uma lista com todos os cadernos"""
    all_notebooks = notebook_service.get_all_notebooks(db)
    return all_notebooks


@router.get(
    "/{notebook_id}",
    response_model=NotebookResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca de Caderno por ID",
)
def get_notebook_by_id(notebook_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    """Busca e retorna um notebook de acordo com o ID passado"""
    notebook = notebook_service.get_notebook_by_id(db, notebook_id)
    return notebook


@router.patch(
    "/{notebook_id}",
    response_model=NotebookResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar informações de um caderno por ID",
)
def update_notebook_data_by_id(
    notebook_id: uuid.UUID,
    notebook_data: NotebookUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    """Edita as informações do notebook referente ao ID passado"""
    updated_notebook = notebook_service.update_notebook_data_by_id(
        db, notebook_id, notebook_data
    )
    return updated_notebook


@router.delete(
    "/{notebook_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar caderno por ID",
)
def delete_notebook_by_id(
    notebook_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
):
    """Remove do Banco o notebook referente ao ID passado"""
    notebook_service.delete_notebook_by_id(db, notebook_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
