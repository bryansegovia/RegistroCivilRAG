from fastapi.testclient import TestClient

from app.main import app


class FakeRagService:
    def answer(self, question: str, history: list[dict[str, str]] | None = None) -> dict:
        return {
            "answer": f"Respuesta basada en documento: {question}",
            "sources": [
                {
                    "source": "terminos_registro_civil.pdf",
                    "page": 0,
                    "preview": "Términos y Condiciones de Agencia Virtual",
                }
            ],
        }


def test_chat_endpoint_uses_rag_service(monkeypatch) -> None:
    from app import main

    main.get_rag_service.cache_clear()
    monkeypatch.setattr(main, "get_rag_service", lambda: FakeRagService())
    client = TestClient(app)

    response = client.post(
        "/api/chat",
        json={"message": "Que servicios estan disponibles?", "history": []},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "Respuesta basada en documento" in payload["answer"]
    assert payload["sources"][0]["source"] == "terminos_registro_civil.pdf"
