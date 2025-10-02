import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.models import Note
from src.modules.notebooks.service import NotebookService as notebook_service

from .repository import NoteRepository as note_repository
from .schemas import NoteCreate, NoteUpdate


class NoteService:
    @staticmethod
    def create_note(db: Session, note_data: NoteCreate, notebook_id: uuid.UUID) -> Note:
        """Cria uma nova nota"""
        notebook_service.get_notebook_by_id(db, notebook_id)
        new_note = note_repository.create_note(db, note_data, notebook_id)
        return new_note

    @staticmethod
    def get_note_by_id(db: Session, note_id: uuid.UUID, notebook_id: uuid.UUID) -> Note:
        """Busca e retorna a Nota referente ao ID passado"""
        note = note_repository.get_note_by_id(db, note_id, notebook_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A nota não foi encontrada",
            )
        return note

    @staticmethod
    def get_all_notes_from_notebook_id(
        db: Session, notebook_id: uuid.UUID
    ) -> list[Note]:
        """Retorna todas as notas de um caderno"""
        notebook_service.get_notebook_by_id(db, notebook_id)
        return note_repository.get_all_notes_from_notebook_id(db, notebook_id)

    @staticmethod
    def update_note_data_by_id(
        db: Session,
        note_id: uuid.UUID,
        notebook_id: uuid.UUID,
        note_update_data: NoteUpdate,
    ) -> Note:
        """Atualiza os dados de uma nota existente"""
        note_to_update = NoteService.get_note_by_id(db, note_id, notebook_id)
        return note_repository.update_note(db, note_to_update, note_update_data)

    @staticmethod
    def delete_note_by_id(db: Session, note_id: uuid.UUID, notebook_id: uuid.UUID):
        """Deleta uma nota existente"""
        note_to_delete = NoteService.get_note_by_id(db, note_id, notebook_id)
        note_repository.delete_note(db, note_to_delete)
