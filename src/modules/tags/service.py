import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.models import Tag

from .repository import TagRepository as tag_repository
from .schemas import TagCreate, TagUpdate


class TagService:
    @staticmethod
    def create_tag(db: Session, tag_data: TagCreate) -> Tag:
        """Cria uma nova tag"""
        try:
            return tag_repository.create_tag(db, tag_data)
        except IntegrityError as err:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uma tag com esse nome já existe",
            ) from err

    @staticmethod
    def get_all_tags(db: Session) -> list[Tag]:
        """Retorna uma lista com todas as tags"""
        return tag_repository.get_all_tags(db)

    @staticmethod
    def get_tag_by_id(db: Session, tag_id: uuid.UUID) -> Tag:
        """Busca e retorna uma tag referente ao ID passado no parâmetro"""
        tag = tag_repository.get_tag_by_id(db, tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="A tag não foi encontrada"
            )
        return tag

    @staticmethod
    def update_tag(db: Session, tag_id: uuid.UUID, tag_update_data: TagUpdate) -> Tag:
        """Edita as informações de uma tag"""
        tag_to_update = TagService.get_tag_by_id(db, tag_id)

        try:
            return tag_repository.update_tag(db, tag_to_update, tag_update_data)
        except IntegrityError as err:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uma tag com esse nome já existe",
            ) from err

    @staticmethod
    def delete_tag(db: Session, tag_id: uuid.UUID):
        """Deleta uma tag do Banco"""
        tag_to_delete = TagService.get_tag_by_id(db, tag_id)
        tag_repository.delete_tag(db, tag_to_delete)
