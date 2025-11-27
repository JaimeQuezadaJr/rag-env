# scripts/ingest.py

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings  # <- UPDATED IMPORT

# Calculate project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_FOLDER = os.path.join(ROOT_DIR, "pdf_inputs")
VECTORSTORE_FOLDER = os.path.join(ROOT_DIR, "vectorstore")


def run_ingest():
    print("\n🔄 Running ingestion...")

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if not pdf_files:
        print("⚠️ No PDFs found in pdf_inputs/. Skipping.")
        return

    all_documents = []

    # Load PDFs
    for pdf in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf)
        print(f"📄 Loading {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        all_documents.extend(docs)

    # Split into chunks
    print("✂️ Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(all_documents)

    # Generate embeddings
    print("🧠 Generating embeddings...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Remove old vectorstore
    if os.path.exists(VECTORSTORE_FOLDER):
        shutil.rmtree(VECTORSTORE_FOLDER)

    # Build FAISS vectorstore
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_FOLDER)

    print("✅ Ingestion complete! Vector store updated.\n")


if __name__ == "__main__":
    run_ingest()
