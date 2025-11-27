# scripts/ingest.py

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import shutil
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
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
    failed_pdfs = []

    # Load PDFs
    for pdf in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf)
        try:
            print(f"📄 Loading {pdf_path}")
            # Try PyPDFLoader first (faster)
            try:
                loader = PyPDFLoader(pdf_path)
                docs = loader.load()
            except Exception as e1:
                # If PyPDFLoader fails, fall back to PyMuPDFLoader (more robust)
                print(f"   ⚠️  PyPDFLoader failed, trying PyMuPDFLoader...")
                loader = PyMuPDFLoader(pdf_path)
                docs = loader.load()

            all_documents.extend(docs)
            print(f"   ✅ Successfully loaded {len(docs)} pages")
        except Exception as e:
            print(f"   ❌ Failed to load {pdf} with both loaders: {str(e)}")
            failed_pdfs.append(pdf)
            continue

    if failed_pdfs:
        print(f"\n⚠️  Warning: {len(failed_pdfs)} PDF(s) could not be loaded:")
        for pdf in failed_pdfs:
            print(f"   - {pdf}")
        print("   Continuing with successfully loaded PDFs...\n")

    if not all_documents:
        print("❌ No documents were successfully loaded. Cannot create vectorstore.")
        return

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
