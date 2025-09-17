from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.modules.folders import folder_repository
from src.modules.folders.folder_schemas import FolderCreate, FolderResponse

router = APIRouter(prefix="/folders", tags=["Folders"])


@router.post(
    "/",
    response_model=FolderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova Pasta",
)
def create_folder(folder_data: FolderCreate, db: Session = Depends(get_db)):
    new_folder = folder_repository.FolderRepository.create_folder(db, folder_data)
    return new_folder
