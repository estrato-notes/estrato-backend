"""Schemas para o módulo tags"""

import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TagCreate(BaseModel):
    """Schema para a criação de uma nova tag"""

    name: str = Field(..., min_length=1, max_length=20, description="Nome da Tag")


class TagUpdate(BaseModel):
    """Schema para a atualização do nome de uma tag"""

    name: Optional[str] = Field(None, description="Novo nome da Tag")


class TagResponse(BaseModel):
    """Schema de retorno com os dados da tag"""

    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
