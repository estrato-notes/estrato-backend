from sqlalchemy import or_, select, union_all
from sqlalchemy.orm import Session
from sqlalchemy.sql import literal_column
from sqlalchemy.sql.selectable import Select

from src.core.models import Note, Notebook, Tag, Template


class SearchRepository:
    @staticmethod
    def notes_subquery(search_pattern: str) -> Select:
        """Cria a subconsulta para buscar em Notas (titulo e conteudo)"""
        return select(
            Note.id,
            Note.title.label("name"),
            literal_column("'note'").label("type"),
            Note.content.label("snippet"),
        ).where(
            or_(Note.title.ilike(search_pattern), Note.content.ilike(search_pattern))
        )

    @staticmethod
    def notebooks_subquery(search_pattern: str) -> Select:
        """Cria a subconsulta para buscar em Notebooks (nome)"""
        return select(
            Notebook.id,
            Notebook.name.label("name"),
            literal_column("'notebook'").label("type"),
            literal_column("NULL").label("snippet"),
        ).where(Notebook.name.ilike(search_pattern))

    @staticmethod
    def tag_subquery(search_pattern: str) -> Select:
        """Cria a subconsulta para buscar em Tags (nome)"""
        return select(
            Tag.id,
            Tag.name.label("name"),
            literal_column("'tag'").label("type"),
            literal_column("NULL").label("snippet"),
        ).where(Tag.name.ilike(search_pattern))

    @staticmethod
    def template_subquery(search_pattern: str) -> Select:
        """Cria a subconsulta para buscar em Templates (nome)"""
        return select(
            Template.id,
            Template.name.label("name"),
            literal_column("'template'").label("type"),
            literal_column("NULL").label("snippet"),
        ).where(Template.name.ilike(search_pattern))

    @staticmethod
    def search_query(db: Session, query_term: str) -> list:
        """Executa uma busca unificada com as subqueries em Nota, Notebook, Template e Tag"""
        if not query_term:
            return []

        search_pattern = f"%{query_term}%"

        notes = SearchRepository.notes_subquery(search_pattern)
        notebooks = SearchRepository.notebooks_subquery(search_pattern)
        tags = SearchRepository.tag_subquery(search_pattern)
        templates = SearchRepository.template_subquery(search_pattern)

        unified_query = union_all(notes, notebooks, tags, templates)

        return db.execute(unified_query).all()
