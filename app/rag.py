from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import get_settings
from app.ingest import ensure_vectorstore
from app.prompts import SYSTEM_PROMPT


def format_documents(documents: list[Any]) -> str:
    formatted = []
    for index, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "documento")
        page = document.metadata.get("page")
        location = f"{source}, pagina {page + 1}" if isinstance(page, int) else source
        formatted.append(f"[Fuente {index}: {location}]\n{document.page_content}")
    return "\n\n".join(formatted)


def normalize_history(history: list[dict[str, str]] | None) -> list[Any]:
    messages: list[Any] = []
    for item in history or []:
        role = item.get("role")
        content = item.get("content", "").strip()
        if not content:
            continue
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
    return messages[-8:]


class RagService:
    def __init__(self) -> None:
        settings = get_settings()
        vectorstore = ensure_vectorstore()
        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": settings.retrieval_k},
        )
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_chat_model,
            google_api_key=settings.gemini_api_key or None,
            temperature=0.1,
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

    def answer(self, question: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
        documents = self.retriever.invoke(question)
        context = format_documents(documents)
        messages = self.prompt.invoke(
            {
                "context": context,
                "chat_history": normalize_history(history),
                "question": question,
            }
        )
        response = self.llm.invoke(messages)

        return {
            "answer": response.content,
            "sources": [
                {
                    "source": document.metadata.get("source", "documento"),
                    "page": document.metadata.get("page"),
                    "preview": document.page_content[:220],
                }
                for document in documents
            ],
        }
