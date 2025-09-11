# 🌩️ Streamlit Cloud Emulator Dockerfile
# Replica exacta del entorno de Streamlit Cloud para desarrollo local
FROM python:3.12-slim

# Set environment variables (matching Streamlit Cloud)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_BROWSER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_CLOUD_EMULATOR=true

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY ../requirements.txt .
COPY ../runtime.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from parent directory
COPY ../ .

# Create directories that Streamlit might need
RUN mkdir -p .streamlit

# Set memory limits to simulate Streamlit Cloud (1GB)
ENV PYTHONMALLOC=malloc
ENV MALLOC_ARENA_MAX=2
ENV MALLOC_MMAP_THRESHOLD_=131072
ENV MALLOC_TRIM_THRESHOLD_=131072
ENV MALLOC_TOP_PAD_=131072
ENV MALLOC_MMAP_MAX_=65536

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]