import uuid

from sqlalchemy.orm import Session

from src.core.models import Notebook

from .schemas import NotebookCreate, NotebookUpdate


class NotebookRepository:
    @staticmethod
    def create_notebook(db: Session, notebook_data: NotebookCreate) -> Notebook:
        """Cria e adiciona um notebook no DB"""
        new_notebook = Notebook(name=notebook_data.name)

        db.add(new_notebook)
        db.commit()
        db.refresh(new_notebook)

        return new_notebook

    @staticmethod
    def get_all_notebooks(db: Session) -> list[Notebook]:
        """Retorna uma lista com todos os notebooks"""
        return db.query(Notebook).all()

    @staticmethod
    def get_notebook_by_id(db: Session, notebook_id: uuid.UUID) -> Notebook | None:
        """Busca e retorna uma pasta referente ao ID passado"""
        return db.query(Notebook).filter(Notebook.id == notebook_id).first()

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
