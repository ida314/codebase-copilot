from fastapi import FastAPI

# logging helper
try:
    from src.utils.logging import get_logger
except Exception:
    import logging
    def get_logger(name: str):
        return logging.getLogger(name)

log = get_logger(__name__)

app = FastAPI(title="Chunker API")

@app.get("/healthz")
def health():
    log.info("health check ok")
    return {"status": "ok"}
