# backend/ingest.py

import os

import shutil
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Get Ollama host from environment (for Docker) or use default
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Calculate project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_FOLDER = os.path.join(ROOT_DIR, "pdf_inputs")
VECTORSTORE_FOLDER = os.path.join(ROOT_DIR, "vectorstore")


def run_ingest():
    """Run the ingestion process and return status"""
    print("\n🔄 Running ingestion...")

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if not pdf_files:
        return {"success": False, "message": "No PDFs found in pdf_inputs/"}

    all_documents = []
    failed_pdfs = []
    loaded_pdfs = []

    # Load PDFs
    for pdf in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf)
        try:
            print(f"📄 Loading {pdf_path}")
            try:
                loader = PyPDFLoader(pdf_path)
                docs = loader.load()
            except Exception:
                print(f"   ⚠️  PyPDFLoader failed, trying PyMuPDFLoader...")
                loader = PyMuPDFLoader(pdf_path)
                docs = loader.load()

            all_documents.extend(docs)
            loaded_pdfs.append(pdf)
            print(f"   ✅ Successfully loaded {len(docs)} pages")
        except Exception as e:
            print(f"   ❌ Failed to load {pdf}: {str(e)}")
            failed_pdfs.append(pdf)
            continue

    if not all_documents:
        return {"success": False, "message": "No documents were successfully loaded"}

    # Split into chunks
    print("✂️ Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(all_documents)

    # Generate embeddings
    print("🧠 Generating embeddings...")
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_HOST if OLLAMA_HOST.startswith("http") else f"http://{OLLAMA_HOST}"
    )

    # Remove old vectorstore
    if os.path.exists(VECTORSTORE_FOLDER):
        shutil.rmtree(VECTORSTORE_FOLDER)

    # Build FAISS vectorstore
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_FOLDER)

    print("✅ Ingestion complete!\n")

    return {
        "success": True,
        "message": "Ingestion complete",
        "loaded": loaded_pdfs,
        "failed": failed_pdfs,
        "chunks": len(chunks),
    }


def get_pdf_list():
    """Get list of PDFs in the input folder"""
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
        return []
    return [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]


if __name__ == "__main__":
    run_ingest()
