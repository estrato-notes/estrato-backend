import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict


class SearchResultType(str, Enum):
    NOTE = "note"
    NOTEBOOK = "notebook"
    TAG = "tag"
    TEMPLATE = "template"


class SearchResultItem(BaseModel):
    id: uuid.UUID
    name: str
    type: SearchResultType
    snippet: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SearchResponse(BaseModel):
    results: list[SearchResultItem]
