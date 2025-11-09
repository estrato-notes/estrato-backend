"""Repository do Módulo de Notes"""

import uuid

from sqlalchemy.orm import Session

from src.core.models import Note, Tag

from .schemas import NoteCreate, NoteUpdate


class NoteRepository:
    """Classe do Repository de Notes com os métodos que conversam com o banco"""

    @staticmethod
    def create_note(
        db: Session, note_data: NoteCreate, notebook_id: uuid.UUID, user_id: uuid.UUID
    ) -> Note:
        """Cria e adiciona uma nova Nota no Banco"""
        new_note = Note(
            **note_data.model_dump(), notebook_id=notebook_id, user_id=user_id
        )

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        return new_note

    @staticmethod
    def get_note_by_id(
        db: Session, note_id: uuid.UUID, notebook_id: uuid.UUID, user_id: uuid.UUID
    ) -> Note | None:
        """Busca e retorna uma Nota a partir do ID dado"""
        return (
            db.query(Note)
            .filter(
                Note.id == note_id,
                Note.notebook_id == notebook_id,
                Note.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_all_notes_from_notebook_id(
        db: Session, notebook_id: uuid.UUID, user_id: uuid.UUID
    ) -> list[Note]:
        """Retorna todas as Notas de um Caderno a partir do ID"""
        return (
            db.query(Note)
            .filter(Note.notebook_id == notebook_id, Note.user_id == user_id)
            .all()
        )

    @staticmethod
    def update_note(db: Session, note: Note, note_updated_data: NoteUpdate) -> Note:
        """Atualiza os atributos de uma Nota"""
        updated_data = note_updated_data.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(note, key, value)

        db.commit()
        db.refresh(note)

        return note

    @staticmethod
    def delete_note(db: Session, note: Note):
        """Deleta uma Nota do Banco"""
        db.delete(note)
        db.commit()

    @staticmethod
    def add_tag_to_note(db: Session, note: Note, tag: Tag):
        """Adiciona uma tag à lista de tags de uma nota"""
        if tag not in note.tags:
            note.tags.append(tag)
            db.commit()

    @staticmethod
    def delete_tag_from_note(db: Session, note: Note, tag: Tag):
        """Remove uma tag da lista de tags de uma nota"""
        if tag in note.tags:
            note.tags.remove(tag)
            db.commit()
    
    @staticmethod
    def get_all_notes(db: Session, user_id: uuid.UUID) -> list[Note]:
        """Retorna todas as Notas de um usuário"""
        return (
            db.query(Note)
            .filter(Note.user_id == user_id)
            .order_by(Note.updated_at.desc().nulls_last())
            .all()
        )
