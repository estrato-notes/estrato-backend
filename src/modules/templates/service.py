import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.models import Template

from .repository import TemplateRepository as template_repository
from .schemas import TemplateCreate, TemplateUpdate


class TemplateService:
    @staticmethod
    def create_template(db: Session, template_data: TemplateCreate) -> Template:
        """Cria um novo template e chama o repository para salvar no DB"""
        try:
            return template_repository.create_template(db, template_data)
        except IntegrityError as err:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Um template com esse nome já existe",
            ) from err

    @staticmethod
    def get_all_templates(db: Session) -> list[Template]:
        """Retornar uma lista com todos os templates"""
        return template_repository.get_all_templates(db)

    @staticmethod
    def get_template_by_id(db: Session, template_id: uuid.UUID) -> Template:
        """Busca e retorna o template referente ao ID passado"""
        template = template_repository.get_template_by_id(db, template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O template não foi encontrado",
            )
        return template

    @staticmethod
    def update_template(
        db: Session, template_id: uuid.UUID, template_update_data: TemplateUpdate
    ) -> Template:
        """Faz alterações nos dados de um template"""
        template_to_update = TemplateService.get_template_by_id(db, template_id)

        try:
            return template_repository.update_template(
                db, template_to_update, template_update_data
            )
        except IntegrityError as err:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Um template com esse nome já existe",
            ) from err

    @staticmethod
    def delete_template_by_id(db: Session, template_id: uuid.UUID):
        """Deleta um template existente"""
        template_to_delete = TemplateService.get_template_by_id(db, template_id)
        template_repository.delete_template(db, template_to_delete)
