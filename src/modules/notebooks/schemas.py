import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NotebookCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nome da Pasta")


class NotebookUpdate(BaseModel):
    name: Optional[str] = Field(  # noqa: UP045
        None, min_length=3, max_length=100, description="Novo nome da Pasta"
    )  # noqa: UP045
    is_favorite: Optional[bool] = None  # noqa: UP045


class NotebookResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_favorite: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
