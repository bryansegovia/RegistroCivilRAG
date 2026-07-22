from pathlib import Path

import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.config import get_settings


SUPPORTED_EXTENSIONS = {".pdf", ".csv"}


def load_document(path: Path) -> list[Document]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _load_pdf(path)
    if suffix == ".csv":
        return _load_csv(path)
    raise ValueError(f"Formato no soportado: {suffix}. Usa PDF o CSV.")


def load_source_documents(source_dir: Path | None = None) -> list[Document]:
    settings = get_settings()
    base_dir = source_dir or settings.source_dir
    documents: list[Document] = []

    for path in sorted(base_dir.iterdir()):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.extend(load_document(path))

    if not documents:
        raise FileNotFoundError(f"No se encontraron documentos PDF o CSV en {base_dir}.")
    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def _load_pdf(path: Path) -> list[Document]:
    reader = PdfReader(str(path))
    documents: list[Document] = []
    for page_number, page in enumerate(reader.pages):
        documents.append(
            Document(
                page_content=page.extract_text() or "",
                metadata={"source": path.name, "page": page_number},
            )
        )
    return documents


def _load_csv(path: Path) -> list[Document]:
    frame = pd.read_csv(path)
    documents: list[Document] = []
    for index, row in frame.fillna("").iterrows():
        content = "\n".join(f"{column}: {value}" for column, value in row.items())
        documents.append(
            Document(
                page_content=content,
                metadata={"source": path.name, "row": int(index) + 1},
            )
        )
    return documents
