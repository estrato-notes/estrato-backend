"""Service para ações relacionadas ao usuário"""

import uuid

from sqlalchemy.orm import Session

from .repository import UserRepository as user_repository


class UserService:
    """Coordena as ações do repositório de usuário"""

    @staticmethod
    def clear_all_user_data(db: Session, user_id: uuid.UUID):
        """Chama o repositório para limpar os dados do usuário"""
        user_repository.clear_all_user_data(db, user_id)
