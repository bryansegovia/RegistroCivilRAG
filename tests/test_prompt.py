from app.prompts import SYSTEM_PROMPT


def test_prompt_requires_grounded_answers() -> None:
    assert "Usa unicamente el contexto recuperado" in SYSTEM_PROMPT
    assert "No inventes datos" in SYSTEM_PROMPT
    assert "Si la respuesta no esta en el contexto" in SYSTEM_PROMPT
