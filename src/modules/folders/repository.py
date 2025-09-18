from sqlalchemy.orm import Session

from src.core.models import Folder

from .schemas import FolderCreate


class FolderRepository:
    @staticmethod
    def create_folder(db: Session, folder_data: FolderCreate):
        new_folder = Folder(name=folder_data.name, is_favorite=folder_data.is_favorite)

        db.add(new_folder)
        db.commit()
        db.refresh(new_folder)

        return new_folder
