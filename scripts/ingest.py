# scripts/ingest.py
import os
import fitz                      # PyMuPDF
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast, good baseline

def load_pdf_paths(folder_path):
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text("text")
        pages.append((i+1, text))
    return pages

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if len(chunk) > 40:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def embed_texts(texts, model):
    embs = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return [np.array(e, dtype=np.float32) for e in embs]

def build_faiss_index(embeddings):
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatIP(dim)  # inner product with normalized vectors = cosine
    embs = np.stack(embeddings)
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    embs = embs / (norms + 1e-10)
    index.add(embs)
    return index

def ingest_all_pdfs(pdf_folder, index_path="faiss.index", meta_path="meta.pkl"):
    pdf_paths = load_pdf_paths(pdf_folder)
    docs = []  # list of dicts: {pdf, page, text}
    for p in pdf_paths:
        print("Processing:", p)
        pages = extract_text_from_pdf(p)
        for page_num, page_text in pages:
            chunks = chunk_text(page_text)
            for chunk in chunks:
                docs.append({"pdf": os.path.basename(p), "page": page_num, "text": chunk})

    print(f"Total chunks: {len(docs)}")
    texts = [d["text"] for d in docs]

    # embed
    print("Loading embedding model:", EMBED_MODEL_NAME)
    model = SentenceTransformer(EMBED_MODEL_NAME)
    embeddings = embed_texts(texts, model)
    print("Embeddings computed.")

    # build FAISS
    index = build_faiss_index(embeddings)
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(docs, f)
    print("Index and metadata saved:", index_path, meta_path)

if __name__ == "__main__":
    ingest_all_pdfs("../pdf_inputs", index_path="../faiss.index", meta_path="../meta.pkl")
