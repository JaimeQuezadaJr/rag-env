# backend/app.py

import os
import sys

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import shutil

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingest import run_ingest, get_pdf_list
from chat import chat

# Calculate project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_FOLDER = os.path.join(ROOT_DIR, "pdf_inputs")

# Ensure PDF folder exists
os.makedirs(PDF_FOLDER, exist_ok=True)

app = FastAPI(title="RAG Document Chat API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    model: str = "qwen3:1.7b"


class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]


class IngestResponse(BaseModel):
    success: bool
    message: str
    loaded: List[str] = []
    failed: List[str] = []
    chunks: int = 0


@app.get("/")
async def root():
    return {"status": "ok", "message": "RAG API is running"}


@app.get("/pdfs")
async def list_pdfs():
    """List all uploaded PDFs"""
    pdfs = get_pdf_list()
    return {"pdfs": pdfs, "count": len(pdfs)}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), auto_ingest: bool = False):
    """Upload a PDF file

    Args:
        auto_ingest: If True, automatically run ingestion after upload
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(PDF_FOLDER, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = {"success": True, "filename": file.filename}

        # Auto-ingest if requested
        if auto_ingest:
            ingest_result = run_ingest()
            result["ingestion"] = ingest_result

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/pdfs/{filename}")
async def delete_pdf(filename: str):
    """Delete a PDF file and automatically rebuild vectorstore"""
    file_path = os.path.join(PDF_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        os.remove(file_path)

        # Automatically rebuild vectorstore after deletion
        ingest_result = run_ingest()

        return {
            "success": True,
            "message": f"Deleted {filename}",
            "ingestion": ingest_result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", response_model=IngestResponse)
async def ingest_documents():
    """Run the ingestion process on all PDFs"""
    try:
        result = run_ingest()
        return result
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "loaded": [],
            "failed": [],
            "chunks": 0,
        }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat with the documents"""
    try:
        response = chat(request.message, model=request.model)
        return response
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "sources": []}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
