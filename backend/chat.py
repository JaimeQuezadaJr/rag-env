# backend/chat.py

import subprocess
from query import query_documents

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


def generate_response(prompt: str, model: str = "gemma3:4b") -> str:
    """Generate response using Ollama"""
    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = process.communicate(prompt)
    return out.strip()


def chat(question: str, model: str = "gemma3:4b", top_k: int = 4) -> dict:
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
