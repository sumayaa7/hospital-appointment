from pathlib import Path
from typing import Any

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "vector_store"
SYSTEM_NAME = "Hospital Appointment System"
REJECTION = f"I can only answer questions about {SYSTEM_NAME}."


class RagAssistant:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = ChatOllama(model="gemma3:4b", temperature=0.1)
        self.store = Chroma(
            persist_directory=str(VECTOR_DIR),
            embedding_function=self.embeddings,
            collection_name="hospital_docs",
        )
        self.retriever = self.store.as_retriever(search_kwargs={"k": 4})

    def answer(self, question: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
        history = history or []
        docs = self.retriever.invoke(question)
        if not docs:
            return {"answer": REJECTION, "sources": []}

        top_text = " ".join(d.page_content[:300] for d in docs).strip()
        if len(top_text) < 80:
            return {"answer": REJECTION, "sources": []}

        context = "\n\n---\n\n".join(d.page_content for d in docs)
        history_text = "\n".join(
            f"{m.get('role', 'user')}: {m.get('content', '')}" for m in history[-6:]
        )

        prompt = f"""
You are a support assistant for users of this website.
Scope:
- Answer ONLY questions related to {SYSTEM_NAME}.
- Use ONLY the provided context.
- If question is unrelated or context is insufficient, reply exactly:
{REJECTION}
Behavior:
- Be clear, simple, and solution-oriented.
- If unsure, say: "I'm not sure about that. Please contact support."
- Do not include source names or file paths in the answer.
Conversation history:
{history_text}
Context:
{context}
User question:
{question}
"""
        response = self.llm.invoke(prompt)

        sources = []
        for d in docs:
            src = d.metadata.get("source", "unknown")
            if src not in sources:
                sources.append(src)

        return {"answer": response.content.strip(), "sources": sources[:3]}
