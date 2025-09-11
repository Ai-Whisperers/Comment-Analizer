@echo off
REM 🌩️ Quick Start para Streamlit Cloud Emulator (Windows)
echo.
echo 🌩️ STREAMLIT CLOUD EMULATOR - QUICK START
echo ==========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está corriendo
    echo 💡 Inicia Docker Desktop y vuelve a intentar
    pause
    exit /b 1
)

echo ✅ Docker detectado
echo 🚀 Iniciando emulador de Streamlit Cloud...
echo.

REM Start the emulator
python emulator.py --start

echo.
echo 📋 COMANDOS ÚTILES:
echo   python emulator.py --status    Ver estado
echo   python emulator.py --monitor   Monitor de recursos
echo   python emulator.py --logs      Ver logs
echo   python emulator.py --restart   Reiniciar
echo   python emulator.py --stop      Detener
echo.
pause