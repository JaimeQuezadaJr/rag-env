# DocChat — AI Document Assistant

A RAG (Retrieval-Augmented Generation) application that allows you to upload PDF documents while using local LLMs for information retrieval. Built with FastAPI, React, LangChain, and FAISS for efficient document embedding and vector similarity search.

## Features

- 📄 Upload PDF documents
- 🧠 Automatic embedding generation with Ollama
- 💬 Chat interface to ask questions about your documents
- 🔍 Source citations for answers
- ⚡ Fast vector search with FAISS

## What I Learned

Key insights from building this RAG application:

- **RAG Architecture**: Combining vector search with LLM generation, understanding embedding vs. chat models, and optimizing chunk sizes for context preservation
- **Document Processing**: Robust PDF handling with fallback mechanisms (`PyPDFLoader` → `PyMuPDFLoader`) and automated ingestion using file system watchers
- **Vector Search**: Working with FAISS for efficient similarity search and managing vector store updates when documents change
- **Full-Stack Integration**: Building RESTful APIs with FastAPI, connecting React frontends, and implementing proper error handling and UX patterns
- **Docker & Containerization**: Orchestrating multi-container applications with Docker Compose, configuring Nginx for reverse proxying, and managing LLM memory requirements
- **Local LLMs**: Running models locally with Ollama, understanding model size/accuracy trade-offs, and crafting effective prompts for RAG responses

**Real-World Applications**: This RAG architecture can be extended to power enterprise knowledge bases, legal document analysis, academic research assistants, customer support chatbots with documentation, and internal company wikis. The ability to query large document collections with source citations makes it valuable for any scenario requiring accurate, traceable information retrieval.

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

> **Note for Docker users**: Allocate at least 6GB of memory to Docker Desktop (Settings → Resources → Advanced) for smooth operation.

### Install Ollama Models

```bash
# Embedding model (required)
ollama pull nomic-embed-text

# Chat model
ollama pull gemma3:4b
```

## Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

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

## Docker Setup

Run the entire application using Docker - includes Ollama and all dependencies.

### Quick Start:

1. **Navigate to project directory:**
   ```bash
   cd /path/to/rag-env
   ```

2. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### First Run:

On first startup, the system will automatically download and set up:
- Ollama server
- Required models (`nomic-embed-text` and `gemma3:4b`)

**First run takes 5-10 minutes** to download models (~3-4GB). Subsequent runs are fast.

### Docker Commands:

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Remove everything (including models)
docker-compose down -v
```

### Memory Configuration:

1. Open Docker Desktop
2. Go to **Settings** → **Resources** → **Advanced**
3. Set **Memory** to at least **6GB** (8GB+ recommended)
4. Click **Apply & Restart**

See [DOCKER.md](./DOCKER.md) for detailed Docker documentation.
