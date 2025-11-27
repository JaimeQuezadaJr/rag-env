# DocChat — AI Document Assistant

A RAG (Retrieval-Augmented Generation) application that lets you chat with your PDF documents using local LLMs.

## Features

- 📄 Upload PDF documents
- 🧠 Automatic embedding generation with Ollama
- 💬 Chat interface to ask questions about your documents
- 🔍 Source citations for answers
- ⚡ Fast vector search with FAISS

## Project Structure

```
rag-env/
├── backend/
│   ├── app.py          # FastAPI server
│   ├── ingest.py       # PDF processing & embedding
│   ├── query.py        # Vector search
│   ├── chat.py         # LLM chat integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx     # Main React component
│   │   ├── main.jsx    # Entry point
│   │   └── index.css   # Tailwind styles
│   └── package.json
├── pdf_inputs/         # Uploaded PDFs
└── vectorstore/        # FAISS index
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.ai) installed locally

### Install Ollama Models

```bash
# Embedding model (required)
ollama pull nomic-embed-text

# Chat model (choose one)
ollama pull gemma3:4b
# or
ollama pull llama3.2
```

## Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

The API will be available at `http://localhost:8000`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## Usage

1. **Upload PDFs**: Drag or click to upload your PDF documents
2. **Process Documents**: Click "Process Documents" to generate embeddings
3. **Start Chatting**: Ask questions about your documents

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pdfs` | List uploaded PDFs |
| POST | `/upload` | Upload a PDF file |
| DELETE | `/pdfs/{filename}` | Delete a PDF |
| POST | `/ingest` | Process all PDFs |
| POST | `/chat` | Chat with documents |

## Tech Stack

**Backend:**
- FastAPI
- LangChain
- FAISS
- Ollama

**Frontend:**
- React + Vite
- Tailwind CSS
- Lucide Icons
