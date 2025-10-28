"""Schemas para o módulo search"""

import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict


class SearchResultType(str, Enum):
    """Enum com os tipos de resultados possíveis para uma busca"""

    NOTE = "note"
    NOTEBOOK = "notebook"
    TAG = "tag"
    TEMPLATE = "template"


class SearchResultItem(BaseModel):
    """Schema com os dados para cada item encontrado na busca"""

    id: uuid.UUID
    name: str
    type: SearchResultType
    snippet: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SearchResponse(BaseModel):
    """Schema de retorno geral com todos os itens encontrados na busca"""

    results: list[SearchResultItem]
