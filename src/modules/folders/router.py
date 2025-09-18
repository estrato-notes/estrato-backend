import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import FolderCreate, FolderResponse, FolderUpdate
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


@router.get(
    "/",
    response_model=list[FolderResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista para todas as Pastas",
)
def get_all_folders(db: Session = Depends(get_db)):
    all_folders = service.get_all_folders(db)
    return all_folders


@router.get(
    "/{folder_id}",
    response_model=FolderResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca de Pasta por ID",
)
def get_folder_by_id(folder_id: uuid.UUID, db: Session = Depends(get_db)):
    folder = service.get_folder_by_id(db, folder_id)
    return folder


@router.patch(
    "/{folder_id}",
    response_model=FolderResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar informações de uma Pasta por ID",
)
def update_folder_data_by_id(
    folder_id: uuid.UUID, folder_data: FolderUpdate, db: Session = Depends(get_db)
):
    updated_folder = service.update_folder_data_by_id(db, folder_id, folder_data)
    return updated_folder


@router.delete(
    "/{folder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar Pasta por ID",
)
def delete_folder_by_id(folder_id: uuid.UUID, db: Session = Depends(get_db)):
    service.delete_folder_by_id(db, folder_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
