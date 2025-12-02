# Docker Setup Guide

This guide explains how to run the RAG application using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Docker Commands

### Start services
```bash
docker-compose up
```

### Start in background (detached mode)
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs
docker-compose logs -f
```

### Rebuild after code changes
```bash
docker-compose up --build
```

### Remove everything (including volumes)
```bash
docker-compose down -v
```

## Important Notes

### Ollama Service

**Ollama is included as a Docker service** - you don't need to install it on your host machine!

The setup includes:
- **Ollama container** - Automatically runs Ollama in Docker
- **Auto-download models** - Required models (`nomic-embed-text` and `gemma3:4b`) are automatically pulled on first startup
- **Persistent storage** - Models are stored in a Docker volume and persist between restarts

**First startup may take longer** as it downloads the models (several GB). Subsequent startups will be faster.

### Persistent Data

The following directories are mounted as volumes:
- `./pdf_inputs` - Uploaded PDF files
- `./vectorstore` - FAISS vectorstore index

These persist between container restarts.

## Development vs Production

### Development (Current Setup)
- Frontend: Vite dev server (port 5173)
- Backend: FastAPI with auto-reload
- Direct file access

### Production (Docker)
- Frontend: Nginx serving built React app (port 3000)
- Backend: FastAPI in container (port 8000)
- Volumes for persistence

## Troubleshooting

### Port already in use
```bash
# Find process using port
lsof -ti:8000
lsof -ti:3000

# Kill process
kill $(lsof -ti:8000)
```

### Rebuild specific service
```bash
docker-compose build backend
docker-compose up -d backend
```

### Check container status
```bash
docker-compose ps
```

### Execute commands in container
```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh
```

