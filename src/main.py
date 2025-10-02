from fastapi import FastAPI

app = FastAPI(title="Estrato API")

# Routers
from .modules.notebooks.router import router as notebook_router  # noqa: E402
from .modules.notes.router import router as note_router  # noqa: E402

app.include_router(notebook_router)
app.include_router(note_router)
