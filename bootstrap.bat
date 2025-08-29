@echo off
REM Bootstrap script for Comment Analyzer on Windows
REM Complete automated setup for non-technical users v2.0

setlocal enabledelayedexpansion

echo ================================================
echo    Comment Analyzer - Windows Bootstrap v2.0
echo    Automated Setup for Windows Users
echo ================================================

REM Function to install dependencies
:install_dependencies
echo.
echo Installing Python dependencies...
echo (This may take a few minutes)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [X] requirements.txt not found
    goto :bootstrap_failed
)

echo Upgrading pip...
python -m pip install --upgrade pip --quiet

echo Installing application dependencies...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [X] Failed to install dependencies
    echo Trying with verbose output...
    python -m pip install -r requirements.txt
    goto :bootstrap_failed
)

echo [Y] Dependencies installed successfully!
goto :setup_api_key

REM Function to setup API key
:setup_api_key
echo.
echo Checking OpenAI API configuration...

REM Check .env file first
if exist ".env" (
    echo Loading environment from .env file...
    for /f "usebackq delims=" %%a in (".env") do (
        set "line=%%a"
        if "!line:~0,15!"=="OPENAI_API_KEY=" (
            set "OPENAI_API_KEY=!line:~15!"
        )
    )
)

if "%OPENAI_API_KEY%"=="" (
    echo.
    echo ================================================
    echo OPENAI API KEY SETUP REQUIRED
    echo ================================================
    echo.
    echo This application requires an OpenAI API key to analyze comments.
    echo.
    echo How to get an API key:
    echo 1. Visit: https://platform.openai.com/api-keys
    echo 2. Sign up or log in to your OpenAI account
    echo 3. Click 'Create new secret key'
    echo 4. Copy the key ^(it starts with 'sk-'^)
    echo.
    set /p setup_choice="Do you have an API key ready? (y/n): "
    
    if /i "%setup_choice%"=="y" (
        :api_key_input
        echo.
        set /p user_api_key="Please enter your OpenAI API key: "
        
        REM Basic validation - check if starts with sk- and has reasonable length
        if "!user_api_key:~0,3!"=="sk-" if "!user_api_key:~20,1!" neq "" (
            echo OPENAI_API_KEY=!user_api_key!> .env
            set "OPENAI_API_KEY=!user_api_key!"
            echo [Y] API key saved to .env file
            goto :check_final_requirements
        ) else (
            echo [X] Invalid API key format. Keys should start with 'sk-'
            set /p retry="Try again? (y/n): "
            if /i "!retry!"=="y" goto :api_key_input
            goto :bootstrap_failed
        )
    ) else (
        echo.
        echo Please get an API key from OpenAI and run this script again.
        echo The application cannot work without an API key.
        pause
        exit /b 1
    )
) else (
    echo [Y] OpenAI API Key configured
)
goto :check_final_requirements

REM Function to check Python installation
:check_python_installation
echo.
echo Checking Python installation...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo [Y] %%i
    goto :install_dependencies
) else (
    echo [X] Python not found
    echo.
    echo ================================================
    echo PYTHON INSTALLATION REQUIRED
    echo ================================================
    echo.
    echo This application requires Python 3.8 or later.
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    echo After installation, restart this script.
    pause
    exit /b 1
)

REM Function for final validation
:check_final_requirements
echo.
echo Validating final installation...

set "errors=0"

REM Final Python check
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo [Y] %%i
) else (
    echo [X] Python still not available
    set /a errors+=1
)

REM Final Streamlit check
python -c "import streamlit" >nul 2>&1
if %errorlevel% equ 0 (
    echo [Y] Streamlit available
) else (
    echo [X] Streamlit still not available
    set /a errors+=1
)

REM Final API key check
if "%OPENAI_API_KEY%"=="" (
    echo [X] OpenAI API Key not set
    set /a errors+=1
) else (
    echo [Y] OpenAI API Key configured
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
echo    Setup completed successfully!
echo ================================================
echo.
echo Starting Comment Analyzer application...
echo.
echo Access the application at: http://localhost:%STREAMLIT_PORT%
echo Or: http://127.0.0.1:%STREAMLIT_PORT%
echo.
echo To stop the application, press Ctrl+C
echo ================================================

REM Start the application using run.py for cross-platform compatibility
if exist "run.py" (
    echo Starting via run.py...
    python run.py
) else (
    echo run.py not found, using direct streamlit...
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
)

if %errorlevel% neq 0 (
    echo.
    echo [X] Error starting application
    echo.
    echo Troubleshooting:
    echo 1. Try running: python run.py
    echo 2. Or: streamlit run src\main.py
    echo 3. Check that all dependencies are installed
    pause
)

goto :end

REM ================================================
REM MAIN EXECUTION STARTS HERE
REM ================================================
echo.
echo Starting automated setup sequence...

REM Step 1: Check Python installation
goto :check_python_installation

:end
endlocal