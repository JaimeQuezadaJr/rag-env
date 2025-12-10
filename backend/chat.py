# backend/chat.py

import os
import requests
from query import query_documents

# Get Ollama host from environment (for Docker) or use default
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
if not OLLAMA_HOST.startswith("http"):
    OLLAMA_HOST = f"http://{OLLAMA_HOST}"

SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided document context.

Your responses should be:
- Accurate and based on the provided context
- Clear and well-structured
- Concise but complete

If the answer is not found in the context, say: "I couldn't find that information in the uploaded documents."
"""


def build_prompt(question: str, context_chunks: list) -> str:
    """Build the prompt with context and question"""
    context = ""
    for chunk in context_chunks:
        context += (
            f"\n[Source: {chunk['pdf']} | Page {chunk['page']}]\n{chunk['text']}\n"
        )

    return f"""CONTEXT FROM DOCUMENTS:
{context}

USER QUESTION:
{question}

Please answer the question based on the context above."""


def generate_response(prompt: str, model: str = "qwen3:4b") -> str:
    """Generate response using Ollama API"""
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"


def chat(question: str, model: str = "qwen3:4b", top_k: int = 4) -> dict:
    """Main chat function - retrieves context and generates response"""
    # Retrieve relevant chunks
    chunks = query_documents(question, top_k=top_k)

    if not chunks:
        return {
            "answer": "No documents have been uploaded yet. Please upload some PDFs first.",
            "sources": [],
        }

    # Build prompt and generate response
    prompt = build_prompt(question, chunks)
    answer = generate_response(prompt, model)

    # Format sources - deduplicate by (pdf, page) combination
    seen = set()
    sources = []
    for c in chunks:
        source_key = (c["pdf"], c["page"])
        if source_key not in seen:
            seen.add(source_key)
            sources.append({"pdf": c["pdf"], "page": c["page"]})

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    response = chat("Where did Rajiv Battula work in 2015?")
    print(response["answer"])
    print("\nSources:", response["sources"])
