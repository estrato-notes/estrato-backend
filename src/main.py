from fastapi import FastAPI

app = FastAPI(title="Estrato API")

# Routers
from .modules.notebooks.router import router as notebook_router  # noqa: E402
from .modules.notes.router import router as note_router  # noqa: E402
from .modules.tags.router import router as tag_router  # noqa: E402
from .modules.templates.router import router as template_router  # noqa: E402

app.include_router(notebook_router)
app.include_router(note_router)
app.include_router(tag_router)
app.include_router(template_router)
