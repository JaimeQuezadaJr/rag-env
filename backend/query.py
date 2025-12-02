# backend/query.py

import os

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Get Ollama host from environment (for Docker) or use default
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Calculate project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_FOLDER = os.path.join(ROOT_DIR, "vectorstore")


def load_vectorstore():
    """Load the FAISS vectorstore"""
    if not os.path.exists(VECTORSTORE_FOLDER):
        return None

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_HOST if OLLAMA_HOST.startswith("http") else f"http://{OLLAMA_HOST}"
    )
    vectorstore = FAISS.load_local(
        VECTORSTORE_FOLDER, embeddings, allow_dangerous_deserialization=True
    )
    return vectorstore


def query_documents(query: str, top_k: int = 4):
    """Query the vectorstore and return results"""
    vectorstore = load_vectorstore()

    if vectorstore is None:
        return []

    results = vectorstore.similarity_search_with_score(query, k=top_k)

    formatted_results = []
    for doc, score in results:
        formatted_results.append(
            {
                "text": doc.page_content,
                "pdf": doc.metadata.get("source", "unknown").split("/")[-1],
                "page": doc.metadata.get("page", 0),
                "score": float(score),
            }
        )

    return formatted_results


if __name__ == "__main__":
    results = query_documents("Where did Jaime Quezada work in 2017?")
    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} (score {r['score']:.3f}) ---")
        print("Source:", r["pdf"], "| Page:", r["page"])
        print(r["text"][:800])
