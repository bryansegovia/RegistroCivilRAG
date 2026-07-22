from pathlib import Path

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import get_settings
from app.document_loader import load_source_documents, split_documents


def build_embeddings() -> GoogleGenerativeAIEmbeddings:
    settings = get_settings()
    return GoogleGenerativeAIEmbeddings(
        model=settings.gemini_embedding_model,
        google_api_key=settings.gemini_api_key or None,
        output_dimensionality=768,
    )


def build_vectorstore(reset: bool = False) -> Chroma:
    settings = get_settings()
    settings.vectorstore_dir.mkdir(parents=True, exist_ok=True)

    if reset:
        _clear_chroma_files(settings.vectorstore_dir)

    documents = load_source_documents(settings.source_dir)
    chunks = split_documents(documents)
    if not chunks:
        raise RuntimeError("No se generaron fragmentos para indexar.")

    return Chroma.from_documents(
        documents=chunks,
        embedding=build_embeddings(),
        persist_directory=str(settings.vectorstore_dir),
        collection_name="registro_civil_terminos",
    )


def vectorstore_exists(path: Path | None = None) -> bool:
    settings = get_settings()
    vectorstore_dir = path or settings.vectorstore_dir
    return (vectorstore_dir / "chroma.sqlite3").exists()


def load_vectorstore() -> Chroma:
    settings = get_settings()
    return Chroma(
        persist_directory=str(settings.vectorstore_dir),
        embedding_function=build_embeddings(),
        collection_name="registro_civil_terminos",
    )


def ensure_vectorstore() -> Chroma:
    if vectorstore_exists():
        return load_vectorstore()
    return build_vectorstore()


def _clear_chroma_files(vectorstore_dir: Path) -> None:
    for item in vectorstore_dir.iterdir():
        if item.is_dir():
            for child in item.rglob("*"):
                if child.is_file():
                    child.unlink()
            for child in sorted(item.rglob("*"), reverse=True):
                if child.is_dir():
                    child.rmdir()
            item.rmdir()
        else:
            item.unlink()


if __name__ == "__main__":
    build_vectorstore(reset=True)
    print("Indice vectorial generado en data/vectorstore.")
