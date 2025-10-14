import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.models import Note, Template
from src.modules.templates.schemas import TemplateFromNoteCreate, TemplateResponse

from .schemas import (
    NoteCreate,
    NoteFromTemplateCreate,
    NoteResponse,
    NoteTagResponse,
    NoteUpdate,
)
from .service import NoteService as note_service

router = APIRouter(prefix="/notebooks/{notebook_id}/notes", tags=["Notes"])


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova nota em um caderno",
)
def create_note(
    notebook_id: uuid.UUID,
    note_data: NoteCreate,
    db: Annotated[Session, Depends(get_db)],
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
    notebook_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
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
    note_id: uuid.UUID, notebook_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
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
    db: Annotated[Session, Depends(get_db)],
) -> Note:
    """Edita as informações de uma nota existente"""
    return note_service.update_note_data_by_id(db, note_id, notebook_id, note_data)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma nota por ID",
)
def delete_note_by_id(
    note_id: uuid.UUID, notebook_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
):
    """Deleta uma nota referente ao ID passado"""
    note_service.delete_note_by_id(db, note_id, notebook_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{note_id}/tags/{tag_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteTagResponse,
    summary="Atribui uma tag a uma nota",
)
def add_tag_to_note(
    note_id: uuid.UUID,
    tag_id: uuid.UUID,
    notebook_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    """Associa uma tag a lista de tags da nota"""
    note, tag = note_service.add_tag_to_note(db, note_id, tag_id, notebook_id)
    return {"note_title": note.title, "tag_name": tag.name}


@router.delete(
    "/{note_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma tag de uma nota",
)
def delete_tag_from_note(
    note_id: uuid.UUID,
    tag_id: uuid.UUID,
    notebook_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    """Remove uma tag da lista de tags da nota"""
    note_service.delete_tag_from_note(db, note_id, tag_id, notebook_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{note_id}/templates",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um template a partir de uma nota",
)
def create_template_from_note(
    note_id: uuid.UUID,
    notebook_id: uuid.UUID,
    template_data: TemplateFromNoteCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Template:
    """Cria um template a partir de uma nota existente"""
    return note_service.create_template_from_note(
        db, note_id, notebook_id, template_data
    )


@router.post(
    "/from-template/{template_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova nota a partir de um template",
)
def create_note_from_template(
    template_id: uuid.UUID,
    notebook_id: uuid.UUID,
    note_data: NoteFromTemplateCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Note:
    """Cria uma nova nota a partir de um template"""
    return note_service.create_note_from_template(
        db, template_id, notebook_id, note_data
    )
