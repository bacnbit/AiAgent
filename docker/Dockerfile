# Multi-stage build for single container deployment
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# Stage 2: Final image with backend + frontend
FROM python:3.11-slim

WORKDIR /app

# Install nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Copy frontend build from previous stage
COPY --from=frontend-builder /frontend/dist /app/frontend/dist

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/sites-available/default

# Create data directory for SQLite
RUN mkdir -p /data && chmod 777 /data

# Expose port 80 for nginx
EXPOSE 80

# Copy startup script
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

CMD ["/start.sh"]
