from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import get_settings
from app.rag import RagService


def load_secrets_into_environment() -> None:
    try:
        secrets = st.secrets
        available_keys = set(secrets.keys())
    except Exception:
        secrets = {}
        available_keys = set()

    for key in ("GEMINI_API_KEY", "GEMINI_CHAT_MODEL", "GEMINI_EMBEDDING_MODEL"):
        if key in available_keys and not os.getenv(key):
            os.environ[key] = str(secrets[key])

    get_settings.cache_clear()


@st.cache_resource(show_spinner=False)
def get_rag_service() -> RagService:
    load_secrets_into_environment()
    settings = get_settings()

    if not settings.gemini_api_key or settings.gemini_api_key == "pega_tu_api_key_aqui":
        raise RuntimeError("Configura GEMINI_API_KEY en los Secrets de Streamlit.")

    return RagService()


def render_sources(sources: list[dict]) -> None:
    if not sources:
        return

    with st.expander("Fuentes usadas"):
        for index, source in enumerate(sources, start=1):
            page = source.get("page")
            page_text = f", pagina {page + 1}" if isinstance(page, int) else ""
            st.markdown(f"**{index}. {source.get('source', 'documento')}{page_text}**")
            st.caption(source.get("preview", ""))


def submit_suggestion(question: str) -> None:
    st.session_state.pending_question = question
    st.session_state.show_suggestions = False


st.set_page_config(page_title="RAG Registro Civil", page_icon="RC", layout="centered")
st.title("RAG Registro Civil")
st.caption("Consulta los terminos y condiciones de la Agencia Virtual del Registro Civil de Ecuador.")

load_secrets_into_environment()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hola. Puedo responder preguntas sobre los terminos y condiciones de la Agencia Virtual del Registro Civil de Ecuador.",
            "sources": [],
        }
    ]

if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            render_sources(message.get("sources", []))

if st.session_state.show_suggestions:
    st.button(
        "¿Quiénes pueden solicitar el duplicado de cédula de identidad?",
        on_click=submit_suggestion,
        args=("¿Quiénes pueden solicitar el duplicado de cédula de identidad?",),
    )
    st.button(
        "Formas de pago disponibles",
        on_click=submit_suggestion,
        args=("Formas de pago disponibles",),
    )
    st.button(
        "Indícame los servicios disponibles",
        on_click=submit_suggestion,
        args=("Indícame los servicios disponibles",),
    )

prompt = st.chat_input("Pregunta sobre el documento...")
if st.session_state.pending_question:
    prompt = st.session_state.pending_question
    st.session_state.pending_question = None

if prompt:
    st.session_state.show_suggestions = False
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Escribiendo..."):
            try:
                service = get_rag_service()
                history = [
                    {"role": message["role"], "content": message["content"]}
                    for message in st.session_state.messages[:-1]
                    if message["role"] in {"user", "assistant"}
                ]
                result = service.answer(prompt, history)
                st.markdown(result["answer"])
                render_sources(result.get("sources", []))
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result.get("sources", []),
                    }
                )
            except Exception as exc:
                error_message = f"No se pudo generar la respuesta: {exc}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message, "sources": []}
                )
