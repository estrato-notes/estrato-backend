import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.models import Notebook

from .repository import NotebookRepository as notebook_repository
from .schemas import NotebookCreate, NotebookUpdate


class NotebookService:
    @staticmethod
    def create_notebook(db: Session, notebook_data: NotebookCreate) -> Notebook:
        """Cria um novo notebook e chama o repository para salvar no DB"""
        try:
            new_notebook = notebook_repository.create_notebook(db, notebook_data)
            return new_notebook
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Um caderno com esse nome já existe",
            )

    @staticmethod
    def get_all_notebooks(db: Session) -> list[Notebook]:
        """Retornar uma lista com todos os notebooks"""
        return notebook_repository.get_all_notebooks(db)

    @staticmethod
    def get_notebook_by_id(db: Session, notebook_id: uuid.UUID) -> Notebook:
        """Busca e retorna o notebook referente ao ID passado"""
        notebook = notebook_repository.get_notebook_by_id(db, notebook_id)
        if not notebook:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O caderno não foi encontrado",
            )
        return notebook

    @staticmethod
    def update_notebook_data_by_id(
        db: Session, notebook_id: uuid.UUID, notebook_update_data: NotebookUpdate
    ) -> Notebook:
        """Faz alterações nos dados de um notebook"""
        notebook_to_update = NotebookService.get_notebook_by_id(db, notebook_id)

        try:
            updated_notebook = notebook_repository.update_notebook(
                db, notebook_to_update, notebook_update_data
            )
            return updated_notebook
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Um caderno com esse nome já existe",
            )

    @staticmethod
    def delete_notebook_by_id(db: Session, notebook_id: uuid.UUID):
        """Deleta um notebook existente"""
        notebook_to_delete = NotebookService.get_notebook_by_id(db, notebook_id)
        notebook_repository.delete_notebook_by_id(db, notebook_to_delete)
