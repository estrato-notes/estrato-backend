from fastapi import FastAPI

app = FastAPI(title="Estrato API")

# Routers
from .modules.notebooks.router import router as notebook_router  # noqa: E402

app.include_router(notebook_router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is working!"}
