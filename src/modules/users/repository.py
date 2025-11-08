"""Repository para ações relacionadas ao usuário"""

import uuid

from sqlalchemy.orm import Session

from src.core.models import Notebook, Tag, Template


class UserRepository:
    """Agrupa os métodos de banco para limpar os dados de um usuário"""

    @staticmethod
    def clear_all_user_data(db: Session, user_id: uuid.UUID):
        """Exclui todos os dados associados a um user_id"""
        db.query(Notebook).filter(Notebook.user_id == user_id).delete(
            synchronize_session=False
        )
        db.query(Tag).filter(Tag.user_id == user_id).delete(synchronize_session=False)
        db.query(Template).filter(Template.user_id == user_id).delete(
            synchronize_session=False
        )

        db.commit()
