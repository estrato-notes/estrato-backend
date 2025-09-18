from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .repository import FolderRepository as repository
from .schemas import FolderCreate


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
