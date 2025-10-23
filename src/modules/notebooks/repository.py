import uuid

from sqlalchemy.orm import Session

from src.core.models import Notebook

from .schemas import NotebookCreate, NotebookUpdate


class NotebookRepository:
    @staticmethod
    def create_notebook(
        db: Session, notebook_data: NotebookCreate, user_id: uuid.UUID
    ) -> Notebook:
        """Cria e adiciona um notebook no DB"""
        new_notebook = Notebook(name=notebook_data.name, user_id=user_id)

        db.add(new_notebook)
        db.commit()
        db.refresh(new_notebook)

        return new_notebook

    @staticmethod
    def get_all_notebooks(db: Session, user_id: uuid.UUID) -> list[Notebook]:
        """Retorna uma lista com todos os notebooks"""
        return db.query(Notebook).filter(Notebook.user_id == user_id).all()

    @staticmethod
    def get_notebook_by_id(
        db: Session, notebook_id: uuid.UUID, user_id: uuid.UUID
    ) -> Notebook | None:
        """Busca e retorna um notebook referente ao ID passado"""
        return (
            db.query(Notebook)
            .filter(Notebook.id == notebook_id, Notebook.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_notebook_by_name(
        db: Session, notebook_name: str, user_id: uuid.UUID
    ) -> Notebook | None:
        """Busca e retorna um notebook com o nome passado pelo parâmetro da função"""
        return (
            db.query(Notebook)
            .filter(Notebook.name == notebook_name, Notebook.user_id == user_id)
            .first()
        )

    @staticmethod
    def update_notebook(
        db: Session, notebook: Notebook, notebook_update_data: NotebookUpdate
    ) -> Notebook:
        """Edita as informações do notebook"""
        updated_dictionary = notebook_update_data.model_dump(exclude_unset=True)
        for key, value in updated_dictionary.items():
            setattr(notebook, key, value)

        db.commit()
        db.refresh(notebook)
        return notebook

    @staticmethod
    def delete_notebook(db: Session, notebook: Notebook):
        """Deleta o notebook do DB"""
        db.delete(notebook)
        db.commit()
