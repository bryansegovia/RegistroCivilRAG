from pathlib import Path

import pandas as pd
from reportlab.platypus import Paragraph, SimpleDocTemplate

from app.document_loader import load_document, split_documents


def test_load_csv_creates_document_per_row(tmp_path: Path) -> None:
    csv_path = tmp_path / "servicios.csv"
    pd.DataFrame(
        [
            {"servicio": "Certificado", "detalle": "Nacimiento"},
            {"servicio": "Duplicado", "detalle": "Cedula"},
        ]
    ).to_csv(csv_path, index=False)

    documents = load_document(csv_path)

    assert len(documents) == 2
    assert "servicio: Certificado" in documents[0].page_content
    assert documents[0].metadata["source"] == "servicios.csv"
    assert documents[0].metadata["row"] == 1


def test_load_pdf_and_split_documents(tmp_path: Path) -> None:
    pdf_path = tmp_path / "terminos.pdf"
    SimpleDocTemplate(str(pdf_path)).build(
        [Paragraph("Texto de prueba sobre terminos del Registro Civil.")]
    )

    documents = load_document(pdf_path)
    chunks = split_documents(documents)

    assert documents
    assert chunks
    assert chunks[0].metadata["source"] == "terminos.pdf"
    assert "Registro Civil" in chunks[0].page_content
