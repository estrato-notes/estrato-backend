import uuid

from sqlalchemy.orm import Session

from src.core.models import Tag
from src.modules.tags.schemas import TagCreate, TagUpdate


class TagRepository:
    @staticmethod
    def create_tag(db: Session, tag_data: TagCreate, user_id: uuid.UUID) -> Tag:
        """Cria uma nova tag no Banco"""
        new_tag = Tag(name=tag_data.name, user_id=user_id)

        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)

        return new_tag

    @staticmethod
    def get_all_tags(db: Session, user_id: uuid.UUID) -> list[Tag]:
        """Retorna uma lista com todas as tags"""
        return db.query(Tag).filter(Tag.user_id == user_id).all()

    @staticmethod
    def get_tag_by_id(db: Session, tag_id: uuid.UUID, user_id: uuid.UUID) -> Tag | None:
        """Busca e retorna uma tag com o id igual ao passado"""
        return db.query(Tag).filter(Tag.id == tag_id, Tag.user_id == user_id).first()

    @staticmethod
    def update_tag(db: Session, tag: Tag, tag_update_data: TagUpdate) -> Tag:
        """Atualiza os dados de uma tag"""
        updated_data = tag_update_data.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(tag, key, value)

        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def delete_tag(db: Session, tag: Tag):
        """Deleta uma tag do Banco"""
        db.delete(tag)
        db.commit()
