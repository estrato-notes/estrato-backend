"""Schemas para o módulo templates"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TemplateCreate(BaseModel):
    """Schema para a criação de um novo template"""

    name: str = Field(..., min_length=1, max_length=200, description="Nome do Template")
    content: Optional[str] = Field(None, description="Conteúdo do Template")


class TemplateUpdate(BaseModel):
    """Schema para a atualização dos dados de um template"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Novo Nome do Template"
    )
    content: Optional[str] = Field(None, description="Novo Conteúdo do Template")


class TemplateFromNoteCreate(BaseModel):
    """Schema para a criação de um novo template a partir de uma nota"""

    name: str = Field(
        ..., min_length=1, max_length=200, description="Nome para o novo template"
    )


class TemplateResponse(BaseModel):
    """Schema de resposta com os dados de um template"""

    id: uuid.UUID
    name: str
    content: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
