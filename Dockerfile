# division-service - Standalone Cloud Run Service
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=True
ENV PYTHONDONTWRITEBYTECODE=True
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared utilities (included in this repo)
COPY shared_utils /app/shared_utils

# Copy application source code
COPY src /app/src

# Create temp directories with appropriate permissions
RUN mkdir -p /tmp/shipments_processing && \
    chown -R app:app /app /tmp/shipments_processing

# Switch to non-root user
USER app

# Set working directory to src
WORKDIR /app/src

# Run application
CMD exec python main.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Labels for metadata
LABEL service="division-service" \
      version="2.0.0" \
      description="division-service microservice - Shipments Processing Platform" \
      maintainer="shipments-platform-team"
