import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NotebookCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nome da Pasta")


class NotebookUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Novo nome da Pasta"
    )
    is_favorite: Optional[bool] = None


class NotebookResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_favorite: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
