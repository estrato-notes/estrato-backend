import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título da Nota")
    content: Optional[str] = Field(None, description="Conteúdo inicial da Nota")


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Novo título da Nota"
    )
    content: Optional[str] = Field(None, description="Novo conteúdo da Nota")
    notebook_id: Optional[str] = Field(
        None, description="ID do novo caderno para mover a nota"
    )
    is_favorite: Optional[bool] = None


class NoteTagResponse(BaseModel):
    note_title: str
    tag_name: str


class NoteFromTemplateCreate(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=200, description="Novo título para a Nota"
    )


class NoteResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str | None
    is_favorite: bool
    notebook_id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
