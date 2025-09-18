from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import FolderCreate, FolderResponse
from .service import FolderService as service

router = APIRouter(prefix="/folders", tags=["Folders"])


@router.post(
    "/",
    response_model=FolderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova Pasta",
)
def create_folder(folder_data: FolderCreate, db: Session = Depends(get_db)):
    new_folder = service.create_folder(db, folder_data)
    return new_folder
