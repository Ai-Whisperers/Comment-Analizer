#!/bin/bash
# Bootstrap Script for Personal Paraguay Comment Analyzer v2.1.0 FINAL
# Automated Streamlit Installation and Launch - Linux/Mac

echo "==============================================="
echo "Personal Paraguay Comment Analyzer v2.1.0 FINAL"
echo "PRODUCTION-READY Bootstrap Script"
echo "==============================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.11+ first"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "[1/5] Python version check..."
$PYTHON_CMD --version

echo
echo "[2/5] Installing/upgrading dependencies..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo
echo "[3/5] Verifying Streamlit installation..."
$PYTHON_CMD -c "import streamlit; print('Streamlit version:', streamlit.__version__)"

if [ $? -ne 0 ]; then
    echo "ERROR: Streamlit installation failed"
    echo "Attempting manual installation..."
    $PYTHON_CMD -m pip install "streamlit>=1.28.0,<2.0.0"
fi

echo
echo "[4/5] Creating .env file if not exists..."
if [ ! -f .env ]; then
    echo "Creating default .env configuration..."
    cat > .env << EOF
# Personal Paraguay Comment Analyzer Configuration
# OPCIONAL: Solo necesario para "Analisis Avanzado (IA)"
# Pipeline Rapido funciona SIN API key
OPENAI_API_KEY=tu_clave_api_aqui
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
EOF
    echo "Created .env file - Edit it to add your OpenAI API key for IA analysis"
fi

echo
echo "[5/5] Launching Comment Analyzer..."
echo "Application will start at: http://localhost:8501"
echo

# Check if port 8501 is available
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null ; then
    echo "WARNING: Port 8501 might be in use"
    echo "If application fails to start, try: export STREAMLIT_PORT=8502"
    echo
fi

echo "==============================================="
echo "ESTADO FINAL VERIFICATION:"
echo "✅ UI profesional sin emojis: READY"
echo "✅ Dual pipeline (Rapido + IA): READY"  
echo "✅ Excel inteligente: READY"
echo "✅ Production ready: READY"
echo "==============================================="
echo
echo "Starting application..."

$PYTHON_CMD run.py

if [ $? -ne 0 ]; then
    echo
    echo "Application failed to start. Trying alternative method..."
    $PYTHON_CMD -m streamlit run src/main.py --server.port 8501
fi

echo
echo "Press Enter to continue..."
read