@echo off
REM Simple one-click launcher for Comment Analyzer
REM For Windows users who want the easiest possible experience

setlocal

echo ================================================================
echo                   COMMENT ANALYZER
echo                   One-Click Launcher
echo ================================================================
echo.
echo This will automatically set up and start the Comment Analyzer.
echo.
echo What this does:
echo  - Checks if Python is installed
echo  - Installs required software automatically  
echo  - Sets up your OpenAI API key (if needed)
echo  - Starts the application
echo.
echo The process may take a few minutes on first run.
echo.

pause

echo.
echo Starting setup process...

REM Try PowerShell first (most capable)
powershell -ExecutionPolicy Bypass -File ".\bootstrap.ps1" 2>nul

if %errorlevel% neq 0 (
    echo PowerShell method failed, trying Command Prompt method...
    call ".\bootstrap.bat"
)

if %errorlevel% neq 0 (
    echo.
    echo ================================================================
    echo SETUP FAILED
    echo ================================================================
    echo.
    echo Both automated setup methods failed.
    echo.
    echo Manual setup options:
    echo 1. Run bootstrap.ps1 in PowerShell
    echo 2. Run bootstrap.bat in Command Prompt
    echo 3. Follow the manual setup guide in README.md
    echo.
    pause
    exit /b 1
)

endlocal