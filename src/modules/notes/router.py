import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.models import Note

from .schemas import NoteCreate, NoteResponse, NoteUpdate
from .service import NoteService as note_service

router = APIRouter(prefix="/notebooks/{notebook_id}/notes", tags=["Notes"])


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova nota em um caderno",
)
def create_note(
    notebook_id: uuid.UUID, note_data: NoteCreate, db: Session = Depends(get_db)
) -> Note:
    """Cria uma nova nota associada a um caderno específico"""
    return note_service.create_note(db, note_data, notebook_id)


@router.get(
    "/",
    response_model=list[NoteResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista todas as notas de um caderno",
)
def get_all_notes_from_notebook_id(
    notebook_id: uuid.UUID, db: Session = Depends(get_db)
) -> list[Note]:
    """Retorna uma lista com todas as notas associadas a um caderno"""
    return note_service.get_all_notes_from_notebook_id(db, notebook_id)


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca uma nota específica por ID",
)
def get_note_by_id(
    note_id: uuid.UUID, notebook_id: uuid.UUID, db: Session = Depends(get_db)
) -> Note:
    """Busca e retorna uma nota específica pelo ID"""
    return note_service.get_note_by_id(db, note_id, notebook_id)


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK,
    summary="Edita as informações de uma nota",
)
def update_note_data_by_id(
    note_id: uuid.UUID,
    notebook_id: uuid.UUID,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
) -> Note:
    """Edita as informações de uma nota existente"""
    return note_service.update_note_data_by_id(db, note_id, notebook_id, note_data)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma nota por ID",
)
def delete_note_by_id(
    note_id: uuid.UUID, notebook_id: uuid.UUID, db: Session = Depends(get_db)
):
    note_service.delete_note_by_id(db, note_id, notebook_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
