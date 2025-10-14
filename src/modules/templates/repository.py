import uuid

from sqlalchemy.orm import Session

from src.core.models import Template

from .schemas import TemplateCreate, TemplateUpdate


class TemplateRepository:
    @staticmethod
    def create_template(db: Session, template_data: TemplateCreate) -> Template:
        """Cria e adiciona um novo template no Banco"""
        new_template = Template(**template_data.model_dump())

        db.add(new_template)
        db.commit()
        db.refresh(new_template)

        return new_template

    @staticmethod
    def get_all_templates(db: Session) -> list[Template]:
        """Retorna uma lista com todos os templates"""
        return db.query(Template).all()

    @staticmethod
    def get_template_by_id(db: Session, template_id: uuid.UUID) -> Template | None:
        """Busca e retorna um template referente ao ID passado"""
        return db.query(Template).filter(Template.id == template_id).first()

    @staticmethod
    def update_template(
        db: Session, template: Template, template_update_data: TemplateUpdate
    ) -> Template:
        """Edita as informações de um template"""
        update_data = template_update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(template, key, value)

        db.commit()
        db.refresh(template)
        return template

    @staticmethod
    def delete_template(db: Session, template: Template):
        """Deleta um template do banco pelo ID"""
        db.delete(template)
        db.commit()
