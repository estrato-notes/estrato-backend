import uuid

from sqlalchemy.orm import Session

from src.core.models import Folder

from .schemas import FolderCreate, FolderUpdate


class FolderRepository:
    @staticmethod
    def create_folder(db: Session, folder_data: FolderCreate):
        """Cria e adiciona uma pasta no DB"""
        new_folder = Folder(name=folder_data.name)

        db.add(new_folder)
        db.commit()
        db.refresh(new_folder)

        return new_folder

    @staticmethod
    def get_all_folders(db: Session) -> list[Folder]:
        """Retorna uma lista com todas as pastas"""
        return db.query(Folder).all()

    @staticmethod
    def get_folder_by_id(db: Session, folder_id: uuid.UUID) -> Folder | None:
        """Busca e retorna uma pasta referente ao ID passado"""
        return db.query(Folder).filter(Folder.id == folder_id).first()

    @staticmethod
    def update_folder(
        db: Session, folder: Folder, folder_update_data: FolderUpdate
    ) -> Folder:
        """Edita as informações da pasta"""
        updated_dictionary = folder_update_data.model_dump(exclude_unset=True)
        for key, value in updated_dictionary.items():
            setattr(folder, key, value)

        db.commit()
        db.refresh(folder)
        return folder

    @staticmethod
    def delete_folder_by_id(db: Session, folder: Folder):
        """Deleta a pasta do DB"""
        db.delete(folder)
        db.commit()
