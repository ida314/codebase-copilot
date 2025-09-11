"""Application configuration and settings"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    app_name: str = "Cold-Start-Copilot"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")

    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")

    # Vector Store
    qdrant_path: str = Field(default="./qdrant_data", env="QDRANT_PATH")
    collection_name: str = Field(default="code_chunks", env="COLLECTION_NAME")

    # Embeddings
    embedding_model: str = Field(default="BAAI/bge-m3", env="EMBEDDING_MODEL")
    embedding_cache_dir: str = Field(default="./model_cache", env="MODEL_CACHE_DIR")
    embedding_dimension: int = Field(default=768, env="EMBEDDING_DIM")

    # Chunking
    max_tokens: int = Field(default=200, env="MAX_TOKENS")
    chunk_overlap: int = Field(default=20, env="CHUNK_OVERLAP")

    # LLM
    llm_model: str = Field(default="llama3-8b", env="LLM_MODEL")
    llm_api_key: Optional[str] = Field(default=None, env="LLM_API_KEY")

    # Monitoring
    langfuse_public_key: Optional[str] = Field(default=None, env="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: Optional[str] = Field(default=None, env="LANGFUSE_SECRET_KEY")
    otlp_endpoint: Optional[str] = Field(default=None, env="OTLP_ENDPOINT")

    # Repository Processing
    ignore_patterns: set = Field(
        default={
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            "venv",
            "dist",
            "build",
            ".pytest_cache",
            ".mypy_cache",
            "*.pyc",
            "*.pyo",
            "*.egg-info",
            ".DS_Store",
            "Thumbs.db",
        }
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
