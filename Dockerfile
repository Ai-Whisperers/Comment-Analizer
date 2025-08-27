# Multi-stage Docker build for Comment Analyzer
# Stage 1: Base image with Python 3.12
FROM python:3.12-slim as base

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Stage 2: Dependencies
FROM base as dependencies

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM base as runtime

# Copy Python dependencies from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data /app/outputs /app/logs /app/client_input && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy application code
COPY --chown=appuser:appuser ./src /app/src
COPY --chown=appuser:appuser ./tests /app/tests
COPY --chown=appuser:appuser ./requirements.txt /app/
COPY --chown=appuser:appuser ./pyproject.toml /app/
COPY --chown=appuser:appuser ./.env.template /app/.env.template

# Create necessary directories with proper permissions
RUN mkdir -p /app/data/raw /app/data/processed \
    /app/outputs/exports /app/outputs/reports /app/outputs/visualizations \
    /app/logs /app/client_input

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose Streamlit port
EXPOSE 8501

# Bootstrap script for startup
COPY --chown=appuser:appuser <<'EOF' /app/bootstrap.sh
#!/bin/bash
set -e

echo "================================"
echo "Comment Analyzer - Bootstrap"
echo "================================"

# Check for environment variables
if [ ! -f /app/.env ]; then
    if [ -f /app/.env.template ]; then
        echo "Warning: No .env file found. Please mount your .env file."
        echo "Example: docker run -v /path/to/.env:/app/.env ..."
    fi
fi

# Validate OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY not set. Application may not function properly."
    echo "Set it via: docker run -e OPENAI_API_KEY=your_key ..."
fi

# Create required directories if they don't exist
mkdir -p /app/data/raw /app/data/processed
mkdir -p /app/outputs/exports /app/outputs/reports /app/outputs/visualizations
mkdir -p /app/logs /app/client_input

echo "Starting Streamlit application..."
echo "================================"

# Start the Streamlit app
exec streamlit run /app/src/main.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --theme.base="dark"
EOF

RUN chmod +x /app/bootstrap.sh

# Set entrypoint to bootstrap script
ENTRYPOINT ["/app/bootstrap.sh"]