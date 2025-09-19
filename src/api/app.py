from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# logging helper (your fallback pattern)
try:
    from src.utils.logging import get_logger
except Exception: # pragma: no cover
    import logging

def get_logger(name: str):
    return logging.getLogger(name)

log = get_logger(__name__)

# Optional settings (replace with your own Settings if present)
try:
    from src.config.settings import settings
    APP_NAME = settings.app_name
    APP_VERSION = settings.app_version
    CORS_ORIGINS = settings.cors_origins
except Exception:
    APP_NAME = "Cold-Start-Copilot"
    APP_VERSION = "0.1.0"
    CORS_ORIGINS = ["*"]

from src.api.middleware import add_correlation_id_middleware
from src.api.errors import install_error_handlers
from src.api.routes import health, metrics, collections, indexing, search, chat, feedback

def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Correlation/trace header
    add_correlation_id_middleware(app)

    # Error envelopes
    install_error_handlers(app)

    # Routers (versioned)
    app.include_router(health.router, prefix="/api/v1", tags=["health"]) # /health, /healthz
    app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"]) # /metrics/summary
    app.include_router(collections.router, prefix="/api/v1", tags=["collections"]) # /collections
    app.include_router(indexing.router, prefix="/api/v1", tags=["indexing"]) # /index-jobs
    app.include_router(search.router, prefix="/api/v1", tags=["search"]) # /search
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"]) # /chat, /chat/stream
    app.include_router(feedback.router, prefix="/api/v1", tags=["feedback"]) # /feedback

    log.info("App created: %s v%s", APP_NAME, APP_VERSION)
    return app


app = create_app()