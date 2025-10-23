import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=20, description="Nome da Tag")


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Novo nome da Tag")


class TagResponse(BaseModel):
    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
