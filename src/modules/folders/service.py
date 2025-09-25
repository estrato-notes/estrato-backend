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
        return repository.get_all_folders(db)

    @staticmethod
    def get_folder_by_id(db: Session, folder_id: uuid.UUID) -> Folder:
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
        folder_to_delete = FolderService.get_folder_by_id(db, folder_id)
        repository.delete_folder_by_id(db, folder_to_delete)
