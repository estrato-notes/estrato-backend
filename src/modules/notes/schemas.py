"""Schemas para o módulo Notes"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    """Schema para a criação de uma nota"""

    title: str = Field(..., min_length=1, max_length=200, description="Título da Nota")
    content: Optional[str] = Field(None, description="Conteúdo inicial da Nota")


class NoteUpdate(BaseModel):
    """Schema para a atualização dos dados de uma nota"""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Novo título da Nota"
    )
    content: Optional[str] = Field(None, description="Novo conteúdo da Nota")
    notebook_id: Optional[str] = Field(
        None, description="ID do novo caderno para mover a nota"
    )
    is_favorite: Optional[bool] = None


class NoteTagResponse(BaseModel):
    """Schema de retorno com os dados da nota associada a uma tag"""

    note_title: str
    tag_name: str

    model_config = ConfigDict(from_attributes=True)


class NoteFromTemplateCreate(BaseModel):
    """Schema para a criação de uma nota a partir de um template"""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Novo título para a Nota"
    )


class QuickNoteCreate(BaseModel):
    """Schema para a criação de uma nota rápida"""

    content: str = Field(..., description="Conteúdo da nota rápida")


class NoteResponse(BaseModel):
    """Schema de retorno com os dados de uma nota"""

    id: uuid.UUID
    title: str
    content: str | None
    is_favorite: bool
    notebook_id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
