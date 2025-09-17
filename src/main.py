from fastapi import FastAPI

app = FastAPI(title="Estrato API")

# Routers
from .modules.folders.folder_router import router as folder_router  # noqa: E402

app.include_router(folder_router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is working!"}
