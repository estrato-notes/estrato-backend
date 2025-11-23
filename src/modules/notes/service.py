"""Service do Módulo Notes"""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.models import Note, Template
from src.modules.notebooks.service import NotebookService as notebook_service
from src.modules.tags.service import TagService as tag_service
from src.modules.templates.schemas import TemplateCreate, TemplateFromNoteCreate
from src.modules.templates.service import TemplateService as template_service

from .repository import NoteRepository as note_repository
from .schemas import NoteCreate, NoteFromTemplateCreate, NoteUpdate, QuickNoteCreate


class NoteService:
    """Classe do Service que conversa com o repository e retorna o resultado pro router"""

    @staticmethod
    def create_note(
        db: Session, note_data: NoteCreate, notebook_id: uuid.UUID, user_id: uuid.UUID
    ) -> Note:
        """Cria uma nova nota"""
        notebook_service.get_notebook_by_id(db, notebook_id, user_id)
        new_note = note_repository.create_note(db, note_data, notebook_id, user_id)
        return new_note

    @staticmethod
    def get_note_by_id(
        db: Session, note_id: uuid.UUID, notebook_id: uuid.UUID, user_id: uuid.UUID
    ) -> Note:
        """Busca e retorna a Nota referente ao ID passado"""
        note = note_repository.get_note_by_id(db, note_id, notebook_id, user_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A nota não foi encontrada",
            )
        return note

    @staticmethod
    def get_all_notes_from_notebook_id(
        db: Session, notebook_id: uuid.UUID, user_id: uuid.UUID
    ) -> list[Note]:
        """Retorna todas as notas de um caderno"""
        notebook_service.get_notebook_by_id(db, notebook_id, user_id)
        return note_repository.get_all_notes_from_notebook_id(db, notebook_id, user_id)

    @staticmethod
    def update_note_data_by_id(
        db: Session,
        note_id: uuid.UUID,
        notebook_id: uuid.UUID,
        note_update_data: NoteUpdate,
        user_id: uuid.UUID,
    ) -> Note:
        """Atualiza os dados de uma nota existente"""

        if note_update_data.notebook_id:
            notebook_service.get_notebook_by_id(
                db, note_update_data.notebook_id, user_id
            )

        note_to_update = NoteService.get_note_by_id(db, note_id, notebook_id, user_id)
        return note_repository.update_note(db, note_to_update, note_update_data)

    @staticmethod
    def delete_note_by_id(
        db: Session, note_id: uuid.UUID, notebook_id: uuid.UUID, user_id: uuid.UUID
    ):
        """Deleta uma nota existente"""
        note_to_delete = NoteService.get_note_by_id(db, note_id, notebook_id, user_id)
        note_repository.delete_note(db, note_to_delete)

    @staticmethod
    def add_tag_to_note(
        db: Session,
        note_id: uuid.UUID,
        tag_id: uuid.UUID,
        notebook_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        """Adiciona uma tag a uma nota"""
        note = NoteService.get_note_by_id(db, note_id, notebook_id, user_id)
        tag = tag_service.get_tag_by_id(db, tag_id, user_id)
        note_repository.add_tag_to_note(db, note, tag)
        return note, tag

    @staticmethod
    def delete_tag_from_note(
        db: Session,
        note_id: uuid.UUID,
        tag_id: uuid.UUID,
        notebook_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        """Remove uma tag associada a uma nota"""
        note = NoteService.get_note_by_id(db, note_id, notebook_id, user_id)
        tag = tag_service.get_tag_by_id(db, tag_id, user_id)
        note_repository.delete_tag_from_note(db, note, tag)

    @staticmethod
    def create_template_from_note(
        db: Session,
        note_id: uuid.UUID,
        notebook_id: uuid.UUID,
        template_data: TemplateFromNoteCreate,
        user_id: uuid.UUID,
    ) -> Template:
        """Cria um template com o conteúdo de uma nota existente"""
        note_to_template = NoteService.get_note_by_id(db, note_id, notebook_id, user_id)

        new_template = TemplateCreate(
            name=template_data.name, content=note_to_template.content
        )

        return template_service.create_template(db, new_template, user_id)

    @staticmethod
    def create_note_from_template(
        db: Session,
        template_id: uuid.UUID,
        notebook_id: uuid.UUID,
        note_data: NoteFromTemplateCreate,
        user_id: uuid.UUID,
    ) -> Note:
        """Cria uma nova nota a partir de um template"""
        template = template_service.get_template_by_id(db, template_id, user_id)

        new_note = NoteCreate(title=note_data.title, content=template.content)

        return NoteService.create_note(db, new_note, notebook_id, user_id)

    @staticmethod
    def create_quick_note(
        db: Session, quick_note_data: QuickNoteCreate, user_id: uuid.UUID
    ) -> Note:
        """Cria uma nota de captura rápida"""
        standard_notebook = notebook_service.get_or_create_quick_capture_notebook(
            db, user_id
        )

        content = quick_note_data.content
        title: str

        if len(content) > 30:
            title = content[:30] + "..."
        else:
            title = content

        return NoteService.create_note(
            db, NoteCreate(title=title, content=content), standard_notebook.id, user_id
        )

    @staticmethod
    def get_all_notes(db: Session, user_id: uuid.UUID) -> list[Note]:
        """Retorna todas as notas de um usuário"""
        return note_repository.get_all_notes(db, user_id)
