from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.config import BASE_DIR, get_settings
from app.ingest import ensure_vectorstore
from app.rag import RagService


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list)


class Source(BaseModel):
    source: str
    page: int | None = None
    preview: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


def warmup_vectorstore() -> None:
    settings = get_settings()
    if settings.gemini_api_key and settings.gemini_api_key != "pega_tu_api_key_aqui":
        ensure_vectorstore()


@asynccontextmanager
async def lifespan(app: FastAPI):
    warmup_vectorstore()
    yield


@lru_cache
def get_rag_service() -> RagService:
    settings = get_settings()
    placeholder = "pega_tu_api_key_aqui"
    if not settings.gemini_api_key or settings.gemini_api_key == placeholder:
        raise RuntimeError("Configura GEMINI_API_KEY en el archivo .env antes de conversar.")
    return RagService()


app = FastAPI(title="RAG Registro Civil", version="0.1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path(BASE_DIR / "static" / "index.html"))


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> dict[str, Any]:
    try:
        service = get_rag_service()
        return service.answer(
            payload.message.strip(),
            [message.model_dump() for message in payload.history],
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo generar la respuesta: {exc}") from exc
