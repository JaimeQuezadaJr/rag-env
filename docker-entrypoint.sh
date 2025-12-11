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

if ! curl -s http://ollama:11434/api/tags | grep -q "mxbai-embed-large"; then
  echo "Pulling mxbai-embed-large embedding model..."
  curl -X POST http://ollama:11434/api/pull -d '{"name": "mxbai-embed-large"}'
fi

if ! curl -s http://ollama:11434/api/tags | grep -q "qwen3:4b"; then
  echo "Pulling qwen3:4b model..."
  curl -X POST http://ollama:11434/api/pull -d '{"name": "qwen3:4b"}'
fi

echo "All models ready. Starting backend..."
exec uvicorn app:app --host 0.0.0.0 --port 8000

