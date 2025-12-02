#!/bin/bash
set -e

echo "Waiting for Ollama to be ready..."
until curl -f http://ollama:11434/api/tags > /dev/null 2>&1; do
  echo "Ollama is not ready yet. Waiting..."
  sleep 2
done

echo "Ollama is ready!"

# Check if models exist, if not pull them
echo "Checking for required models..."

if ! curl -s http://ollama:11434/api/tags | grep -q "nomic-embed-text"; then
  echo "Pulling nomic-embed-text model..."
  curl -X POST http://ollama:11434/api/pull -d '{"name": "nomic-embed-text"}'
fi

if ! curl -s http://ollama:11434/api/tags | grep -q "gemma3:4b"; then
  echo "Pulling gemma3:4b model..."
  curl -X POST http://ollama:11434/api/pull -d '{"name": "gemma3:4b"}'
fi

echo "All models ready. Starting backend..."
exec uvicorn app:app --host 0.0.0.0 --port 8000

