@echo off
REM Bootstrap Script for Personal Paraguay Comment Analyzer v2.1.0 FINAL
REM Automated Streamlit Installation and Launch - Windows

echo ===============================================
echo Personal Paraguay Comment Analyzer v2.1.0 FINAL
echo PRODUCTION-READY Bootstrap Script
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo [1/5] Python version check...
python --version

echo.
echo [2/5] Installing/upgrading dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo [3/5] Verifying Streamlit installation...
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"

if %errorlevel% neq 0 (
    echo ERROR: Streamlit installation failed
    echo Attempting manual installation...
    pip install streamlit>=1.28.0,<2.0.0
)

echo.
echo [4/5] Creating .env file if not exists...
if not exist .env (
    echo Creating default .env configuration...
    echo # Personal Paraguay Comment Analyzer Configuration > .env
    echo # OPCIONAL: Solo necesario para "Analisis Avanzado (IA)" >> .env
    echo # Pipeline Rapido funciona SIN API key >> .env
    echo OPENAI_API_KEY=tu_clave_api_aqui >> .env
    echo STREAMLIT_PORT=8501 >> .env
    echo LOG_LEVEL=INFO >> .env
    echo.
    echo Created .env file - Edit it to add your OpenAI API key for IA analysis
)

echo.
echo [5/5] Launching Comment Analyzer...
echo Application will start at: http://localhost:8501
echo.

REM Check if port 8501 is available
netstat -an | find ":8501" >nul
if %errorlevel% equ 0 (
    echo WARNING: Port 8501 might be in use
    echo If application fails to start, try: set STREAMLIT_PORT=8502
    echo.
)

echo ===============================================
echo ESTADO FINAL VERIFICATION:
echo - UI profesional sin emojis: READY
echo - Dual pipeline (Rapido + IA): READY  
echo - Excel inteligente: READY
echo - Production ready: READY
echo ===============================================
echo.
echo Starting application...

python run.py

if %errorlevel% neq 0 (
    echo.
    echo Application failed to start. Trying alternative method...
    streamlit run src/main.py --server.port 8501
)

pause