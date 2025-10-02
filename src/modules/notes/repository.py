import uuid

from sqlalchemy.orm import Session

from src.core.models import Note

from .schemas import NoteCreate, NoteUpdate


class NoteRepository:
    @staticmethod
    def create_note(db: Session, note_data: NoteCreate, notebook_id: uuid.UUID) -> Note:
        """Cria e adiciona uma nova Nota no Banco"""
        new_note = Note(title=note_data.title, notebook_id=notebook_id)

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        return new_note

    @staticmethod
    def get_note_by_id(
        db: Session, note_id: uuid.UUID, notebook_id: uuid.UUID
    ) -> Note | None:
        """Busca e retorna uma Nota a partir do ID dado"""
        return (
            db.query(Note)
            .filter(Note.id == note_id, Note.notebook_id == notebook_id)
            .first()
        )

    @staticmethod
    def get_all_notes_from_notebook_id(
        db: Session, notebook_id: uuid.UUID
    ) -> list[Note]:
        """Retorna todas as Notas de um Caderno a partir do ID"""
        return db.query(Note).filter(Note.notebook_id == notebook_id).all()

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
