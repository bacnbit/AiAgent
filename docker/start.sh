#!/bin/bash
set -e

echo "Starting AI Agent application..."

# Start nginx
echo "Starting nginx..."
nginx

# Start FastAPI backend
echo "Starting FastAPI backend..."
cd /app
exec uvicorn main:app --host 0.0.0.0 --port 8000 --log-level ${LOG_LEVEL:-info}
