"""Schemas para o módulo dashboard"""

from pydantic import BaseModel, ConfigDict

from src.modules.notebooks.schemas import NotebookResponse
from src.modules.notes.schemas import NoteResponse
from src.modules.tags.schemas import TagResponse
from src.modules.templates.schemas import TemplateResponse


class TagPopularResponse(TagResponse):
    """Schemas com a contagem de notas baseada em uma tag"""

    note_count: int

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    """Schema de retorno padrão com os dados do dashboard"""

    recent_notes: list[NoteResponse]
    popular_tags: list[TagPopularResponse]
    favorite_notes: list[NoteResponse]
    recent_templates: list[TemplateResponse]
    favorite_notebooks: list[NotebookResponse]

    model_config = ConfigDict(from_attributes=True)
