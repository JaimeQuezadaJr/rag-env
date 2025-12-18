# DocChat — AI Document Assistant

A RAG (Retrieval-Augmented Generation) application that allows you to upload PDF documents while using local LLMs for information retrieval. Built with FastAPI, React, LangChain, and FAISS for efficient document embedding and vector similarity search.

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

## What I Learned

Building this RAG application provided valuable insights into several key areas:

### RAG Architecture
- **Retrieval-Augmented Generation**: Understanding how to combine vector search with LLM generation to provide accurate, context-aware responses
- **Embedding Models**: Learning the difference between embedding models (for semantic search) and chat models (for text generation)
- **Chunking Strategies**: Experimenting with chunk sizes and overlap to balance context preservation and retrieval accuracy

### Document Processing
- **PDF Handling**: Implementing robust PDF loading with fallback mechanisms (`PyPDFLoader` → `PyMuPDFLoader`) to handle various PDF formats
- **Text Extraction**: Dealing with malformed PDFs and understanding parser warnings vs. actual errors
- **File System Watching**: Building automatic ingestion pipelines using `watchdog` to monitor directory changes

### Vector Databases & Search
- **FAISS**: Working with Facebook's AI Similarity Search library for efficient vector storage and retrieval
- **Similarity Search**: Understanding cosine similarity and how to retrieve the most relevant document chunks
- **Vector Store Management**: Learning to rebuild and update vector stores when documents are added or removed

### Full-Stack Development
- **API Design**: Building RESTful APIs with FastAPI, including file uploads, CORS handling, and error responses
- **Frontend Integration**: Connecting React frontend to Python backend, handling async operations, and managing application state
- **User Experience**: Implementing loading states, notifications, and markdown rendering for better UX

### Docker & Containerization
- **Multi-Container Applications**: Orchestrating multiple services (backend, frontend, Ollama) with Docker Compose
- **Nginx Configuration**: Setting up reverse proxies, static file serving, and handling SPA routing
- **Resource Management**: Understanding memory requirements for LLMs and optimizing Docker resource allocation
- **Entrypoint Scripts**: Automating model downloads and service initialization in containers

### LLM Integration
- **Local LLMs**: Working with Ollama to run models locally without cloud dependencies
- **Model Selection**: Understanding trade-offs between model size, accuracy, and resource requirements
- **Prompt Engineering**: Crafting system prompts and context-aware prompts for better RAG responses
- **Timeout Handling**: Managing long-running LLM inference requests with appropriate timeout configurations

### Development Best Practices
- **Error Handling**: Implementing robust error handling with fallbacks and user-friendly error messages
- **Environment Management**: Using virtual environments, `.gitignore`, and environment variables effectively
- **Code Organization**: Structuring projects with clear separation between scripts, backend, and frontend
- **Documentation**: Writing comprehensive READMEs and setup guides for reproducibility

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
