"""Arquivo Main da aplicação Estrato"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings

# Routers
from .modules.dashboard.router import router as dashboard_router
from .modules.notebooks.router import router as notebook_router
from .modules.notes.router import base_router as base_notes_router
from .modules.notes.router import router as note_router
from .modules.search.router import router as search_router
from .modules.tags.router import router as tag_router
from .modules.templates.router import router as template_router
from .modules.users.router import router as user_router

app = FastAPI(title="Estrato API")

origins = [settings.CLIENT_ORIGIN_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notebook_router)
app.include_router(note_router)
app.include_router(base_notes_router)
app.include_router(tag_router)
app.include_router(template_router)
app.include_router(dashboard_router)
app.include_router(search_router)
app.include_router(user_router)
