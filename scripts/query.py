# scripts/query.py
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Calculate project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_FOLDER = os.path.join(ROOT_DIR, "vectorstore")


def load_index_and_meta():
    """Load the FAISS vectorstore"""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.load_local(
        VECTORSTORE_FOLDER, embeddings, allow_dangerous_deserialization=True
    )
    return vectorstore, None  # Return None for meta to keep compatible


def query_index(query, vectorstore, meta=None, top_k=4):
    """Query the vectorstore and return results"""
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
    vectorstore, _ = load_index_and_meta()
    question = "Where did Rajiv Battula work in 2015?"
    results = query_index(question, vectorstore, top_k=4)
    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} (score {r['score']:.3f}) ---")
        print("Source:", r["pdf"], "| Page:", r["page"])
        print(r["text"][:800])  # show first 800 chars
