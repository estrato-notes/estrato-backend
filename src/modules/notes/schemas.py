import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título da Nota")


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Novo título da Nota"
    )
    content: Optional[str] = Field(None, description="Novo conteúdo da Nota")
    is_favorite: Optional[bool] = None


class NoteResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str | None
    is_favorite: bool
    notebook_id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
