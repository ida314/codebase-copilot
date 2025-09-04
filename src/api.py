# src/api.py
from fastapi import FastAPI
from .utils.logging import get_logger if False else None  # optional if you have it

app = FastAPI(title="Chunker API")

@app.get("/healthz")
def health():
    return {"status": "ok"}
