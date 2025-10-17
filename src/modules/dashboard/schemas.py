from pydantic import BaseModel, ConfigDict

from src.modules.notebooks.schemas import NotebookResponse
from src.modules.notes.schemas import NoteResponse
from src.modules.tags.schemas import TagResponse


class TagPopularResponse(TagResponse):
    note_count: int

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    recent_notes: list[NoteResponse]
    popular_tags: list[TagPopularResponse]
    favorite_notes: list[NoteResponse]
    favorite_notebooks: list[NotebookResponse]
