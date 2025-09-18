from sqlalchemy.orm import Session

from .repository import FolderRepository as repository
from .schemas import FolderCreate


class FolderService:
    @staticmethod
    def create_folder(db: Session, folder_data: FolderCreate):
        new_folder = repository.create_folder(db, folder_data)
        return new_folder
