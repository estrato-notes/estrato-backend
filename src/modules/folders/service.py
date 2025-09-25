import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.models import Folder

from .repository import FolderRepository as repository
from .schemas import FolderCreate, FolderUpdate


class FolderService:
    @staticmethod
    def create_folder(db: Session, folder_data: FolderCreate):
        """Cria uma pasta nova e chama o repository para salvar no DB"""
        try:
            new_folder = repository.create_folder(db, folder_data)
            return new_folder
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uma pasta com esse nome já existe",
            )

    @staticmethod
    def get_all_folders(db: Session) -> list[Folder]:
        """Retornar uma lista com todas as Pastas"""
        return repository.get_all_folders(db)

    @staticmethod
    def get_folder_by_id(db: Session, folder_id: uuid.UUID) -> Folder:
        """Busca e retorna a pasta referente ao ID passado"""
        folder = repository.get_folder_by_id(db, folder_id)
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A pasta não foi encontrada",
            )
        return folder

    @staticmethod
    def update_folder_data_by_id(
        db: Session, folder_id: uuid.UUID, folder_update_data: FolderUpdate
    ) -> Folder:
        """Faz alterações nos dados de uma pasta"""
        folder_to_update = FolderService.get_folder_by_id(db, folder_id)
        try:
            updated_folder = repository.update_folder(
                db, folder_to_update, folder_update_data
            )
            return updated_folder
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uma pasta com esse nome já existe",
            )

    @staticmethod
    def delete_folder_by_id(db: Session, folder_id: uuid.UUID):
        """Deleta uma pasta existente"""
        folder_to_delete = FolderService.get_folder_by_id(db, folder_id)
        repository.delete_folder_by_id(db, folder_to_delete)
