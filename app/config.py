from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_chat_model: str = Field(default="gemini-3.5-flash", alias="GEMINI_CHAT_MODEL")
    gemini_embedding_model: str = Field(
        default="gemini-embedding-2",
        alias="GEMINI_EMBEDDING_MODEL",
    )
    source_dir: Path = BASE_DIR / "data" / "source"
    vectorstore_dir: Path = BASE_DIR / "data" / "vectorstore"
    default_pdf_path: Path = BASE_DIR / "data" / "source" / "terminos_registro_civil.pdf"
    chunk_size: int = 900
    chunk_overlap: int = 160
    retrieval_k: int = 4

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    load_dotenv(BASE_DIR / ".env")
    return Settings()
