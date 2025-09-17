from fastapi import FastAPI

app = FastAPI(title="Estrato API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is working!"}
