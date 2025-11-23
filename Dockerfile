# Multi-stage build for Student Compass
FROM python:3.11-slim as backend

# Set working directory for backend
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY Generative/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY Generative/ .

# Frontend build stage
FROM node:18-alpine as frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY Generative/frontend/package*.json ./
RUN npm ci

# Copy frontend source and build
COPY Generative/frontend/ ./
RUN npm run build

# Final production stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy backend from backend stage
COPY --from=backend /app/backend .

# Copy frontend build from frontend stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]