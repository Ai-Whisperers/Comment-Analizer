@echo off
REM Bootstrap script for Comment Analyzer on Windows
REM This script handles initialization and startup contracts

setlocal enabledelayedexpansion

echo ================================================
echo    Comment Analyzer - Windows Bootstrap v1.0
echo ================================================

REM Function to check critical requirements
:check_requirements
echo.
echo Checking requirements...

set "errors=0"

REM Check for OpenAI API Key
if "%OPENAI_API_KEY%"=="" (
    if exist ".env" (
        echo Loading environment from .env file...
        for /f "usebackq delims=" %%a in (".env") do (
            set "line=%%a"
            if "!line:~0,15!"=="OPENAI_API_KEY=" (
                set "OPENAI_API_KEY=!line:~15!"
            )
        )
    )
)

if "%OPENAI_API_KEY%"=="" (
    echo [X] CRITICAL: OPENAI_API_KEY not set
    echo     Please set via environment variable or .env file
    set /a errors+=1
) else (
    echo [Y] OpenAI API Key configured
)

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo [Y] %%i
) else (
    echo [X] Python not found
    set /a errors+=1
)

REM Check Streamlit installation
streamlit --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [Y] Streamlit installed
) else (
    echo [X] Streamlit not found
    set /a errors+=1
)

if %errors% neq 0 goto :bootstrap_failed
goto :init_directories

REM Function to initialize directories
:init_directories
echo.
echo Initializing directories...

set "directories=data\raw data\processed outputs\exports outputs\reports outputs\visualizations client_input logs"

for %%d in (%directories%) do (
    if not exist "%%d" (
        mkdir "%%d" 2>nul
        echo [Y] Created %%d
    ) else (
        echo     Directory exists: %%d
    )
)

goto :validate_environment

REM Function to validate environment
:validate_environment
echo.
echo Validating environment...

REM Check APP_ENV
if "%APP_ENV%"=="" (
    set "APP_ENV=production"
    echo     APP_ENV not set, defaulting to: production
) else (
    echo     APP_ENV: %APP_ENV%
)

REM Display configuration
echo.
echo Configuration:
if "%OPENAI_MODEL%"=="" (set "OPENAI_MODEL=gpt-4")
if "%OPENAI_MAX_TOKENS%"=="" (set "OPENAI_MAX_TOKENS=4000")
if "%MAX_FILE_SIZE_MB%"=="" (set "MAX_FILE_SIZE_MB=50")
if "%LOG_LEVEL%"=="" (set "LOG_LEVEL=INFO")
if "%STREAMLIT_PORT%"=="" (set "STREAMLIT_PORT=8501")

echo     OpenAI Model: %OPENAI_MODEL%
echo     Max Tokens: %OPENAI_MAX_TOKENS%
echo     Max File Size: %MAX_FILE_SIZE_MB% MB
echo     Log Level: %LOG_LEVEL%

goto :health_check

REM Function to run health checks
:health_check
echo.
echo Running health checks...

REM Check disk space (simplified for Windows)
for /f "tokens=3" %%a in ('dir /-c ^| find "bytes free"') do (
    set "free_space=%%a"
    set "free_space=!free_space:,=!"
    if !free_space! lss 104857600 (
        echo [!] Low disk space: !free_space! bytes available
    ) else (
        echo [Y] Disk space OK
    )
)

REM Check available memory (Windows equivalent)
for /f "skip=1" %%p in ('wmic os get freephysicalmemory ^| findstr /r /v "^$"') do (
    set "free_mem=%%p"
    if !free_mem! lss 524288 (
        echo [!] Low memory: !free_mem!KB available
    ) else (
        echo [Y] Memory OK
    )
)

goto :bootstrap_success

:bootstrap_failed
echo.
echo Bootstrap failed: Missing critical requirements
pause
exit /b 1

:bootstrap_success
echo.
echo ================================================
echo    Bootstrap completed successfully!
echo ================================================

REM Start the application
echo.
echo Starting Streamlit application...
echo Access the application at: http://localhost:%STREAMLIT_PORT%
echo ================================================

REM Execute streamlit with proper configuration
streamlit run src\main.py ^
    --server.port=%STREAMLIT_PORT% ^
    --server.address=0.0.0.0 ^
    --server.headless=true ^
    --browser.gatherUsageStats=false ^
    --theme.base=dark ^
    --theme.primaryColor=#4ea4ff ^
    --theme.backgroundColor=#0f1419 ^
    --theme.secondaryBackgroundColor=#18202a ^
    --theme.textColor=#e6edf3

endlocal