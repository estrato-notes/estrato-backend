from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.models import Note, Notebook, Tag, note_tags


class DashboardRepository:
    @staticmethod
    def get_recent_notes(db: Session, limit: int = 5) -> list[Note]:
        """Busca as 5 notas mais recentemente atualizadas no banco de dados."""
        return db.query(Note).order_by(Note.updated_at.desc()).limit(limit).all()

    @staticmethod
    def get_favorite_notes(db: Session, limit: int = 5) -> list[Note]:
        """Busca 5 notas marcadas como favorita ordenadas pela data de atualização"""
        return (
            db.query(Note)
            .filter(Note.is_favorite)
            .order_by(Note.updated_at.desc().nulls_last())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_favorite_notebooks(db: Session, limit: int = 5) -> list[Notebook]:
        """Busca 5 notebooks marcados como favorito ordenados pela data de atualização"""
        return (
            db.query(Notebook)
            .filter(Notebook.is_favorite)
            .order_by(Notebook.updated_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_popular_tags(db: Session, limit: int = 5) -> list[tuple[Tag, int]]:
        """Busca as 5 tags mais utilizadas e a contagem de notas relacionadas a cada uma delas"""
        return (
            db.query(Tag, func.count(note_tags.c.note_id))
            .join(note_tags, Tag.id == note_tags.c.tag_id)
            .group_by(Tag.id)
            .order_by(func.count(note_tags.c.note_id).desc())
            .limit(limit)
            .all()
        )
