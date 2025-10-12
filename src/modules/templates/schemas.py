import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Nome do Template")
    content: Optional[str] = Field(None, description="Conteúdo do Template")


class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Novo Nome do Template"
    )
    content: Optional[str] = Field(None, description="Novo Conteúdo do Template")


class TemplateResponse(BaseModel):
    id: uuid.UUID
    name: str
    content: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
