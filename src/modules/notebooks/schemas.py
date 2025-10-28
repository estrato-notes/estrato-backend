"""Schemas para o módulo de notebooks"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NotebookCreate(BaseModel):
    """Schema para a criação de um novo notebook"""

    name: str = Field(..., min_length=3, max_length=100, description="Nome da Pasta")


class NotebookUpdate(BaseModel):
    """Schema para atualizar os dados de um notebook"""

    name: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Novo nome da Pasta"
    )
    is_favorite: Optional[bool] = None


class NotebookResponse(BaseModel):
    """Schema de retorno com os dados de um notebook"""

    id: uuid.UUID
    name: str
    is_favorite: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
