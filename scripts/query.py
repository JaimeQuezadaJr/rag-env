# scripts/query.py
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

def load_index_and_meta(index_path="../faiss.index", meta_path="../meta.pkl"):
    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)
    return index, meta

def embed_query(query, model):
    emb = model.encode([query], convert_to_numpy=True)[0].astype(np.float32)
    emb = emb / (np.linalg.norm(emb) + 1e-10)
    return emb

def query_index(query, index, meta, top_k=4):
    model = SentenceTransformer(EMBED_MODEL_NAME)
    q_emb = embed_query(query, model)
    D, I = index.search(np.array([q_emb]), top_k)
    results = []
    for idx, score in zip(I[0], D[0]):
        item = meta[idx].copy()
        item["score"] = float(score)
        results.append(item)
    return results

if __name__ == "__main__":
    index, meta = load_index_and_meta()
    question = "How do I tune a standard guitar string?"
    results = query_index(question, index, meta, top_k=4)
    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} (score {r['score']:.3f}) ---")
        print("Source:", r["pdf"], "page:", r["page"])
        print(r["text"][:800])  # show first 800 chars
