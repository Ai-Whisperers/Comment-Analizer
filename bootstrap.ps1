# Bootstrap script for Comment Analyzer on Windows (PowerShell)
# This script handles initialization and startup contracts

param(
    [switch]$SkipHealthCheck,
    [string]$Port = "8501"
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"

Write-Host "================================================" -ForegroundColor Green
Write-Host "   Comment Analyzer - PowerShell Bootstrap v1.0" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

function Test-Requirements {
    Write-Host "`nChecking requirements..." -ForegroundColor Yellow
    
    $errors = 0
    
    # Check for OpenAI API Key
    $apiKey = $env:OPENAI_API_KEY
    if (-not $apiKey) {
        if (Test-Path ".env") {
            Write-Host "Loading environment from .env file..." -ForegroundColor Yellow
            Get-Content ".env" | ForEach-Object {
                if ($_ -match "^OPENAI_API_KEY=(.+)$") {
                    $env:OPENAI_API_KEY = $matches[1]
                    $apiKey = $matches[1]
                }
            }
        }
    }
    
    if (-not $apiKey) {
        Write-Host "[X] CRITICAL: OPENAI_API_KEY not set" -ForegroundColor Red
        Write-Host "    Please set via environment variable or .env file" -ForegroundColor Red
        $errors++
    } else {
        Write-Host "[Y] OpenAI API Key configured" -ForegroundColor Green
    }
    
    # Check Python installation
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "[Y] $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "[X] Python not found" -ForegroundColor Red
        $errors++
    }
    
    # Check Streamlit installation
    try {
        $streamlitVersion = streamlit --version 2>&1 | Out-Null
        Write-Host "[Y] Streamlit installed" -ForegroundColor Green
    } catch {
        Write-Host "[X] Streamlit not found" -ForegroundColor Red
        $errors++
    }
    
    return $errors -eq 0
}

function Initialize-Directories {
    Write-Host "`nInitializing directories..." -ForegroundColor Yellow
    
    $directories = @(
        "data\raw",
        "data\processed", 
        "outputs\exports",
        "outputs\reports",
        "outputs\visualizations",
        "client_input",
        "logs"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "[Y] Created $dir" -ForegroundColor Green
        } else {
            Write-Host "    Directory exists: $dir" -ForegroundColor Gray
        }
    }
}

function Test-Environment {
    Write-Host "`nValidating environment..." -ForegroundColor Yellow
    
    # Check APP_ENV
    if (-not $env:APP_ENV) {
        $env:APP_ENV = "production"
        Write-Host "    APP_ENV not set, defaulting to: production" -ForegroundColor Gray
    } else {
        Write-Host "    APP_ENV: $env:APP_ENV" -ForegroundColor Gray
    }
    
    # Set defaults
    if (-not $env:OPENAI_MODEL) { $env:OPENAI_MODEL = "gpt-4" }
    if (-not $env:OPENAI_MAX_TOKENS) { $env:OPENAI_MAX_TOKENS = "4000" }
    if (-not $env:MAX_FILE_SIZE_MB) { $env:MAX_FILE_SIZE_MB = "50" }
    if (-not $env:LOG_LEVEL) { $env:LOG_LEVEL = "INFO" }
    if (-not $env:STREAMLIT_PORT) { $env:STREAMLIT_PORT = $Port }
    
    # Display configuration
    Write-Host "`nConfiguration:" -ForegroundColor Yellow
    Write-Host "    OpenAI Model: $env:OPENAI_MODEL" -ForegroundColor Gray
    Write-Host "    Max Tokens: $env:OPENAI_MAX_TOKENS" -ForegroundColor Gray
    Write-Host "    Max File Size: $env:MAX_FILE_SIZE_MB MB" -ForegroundColor Gray
    Write-Host "    Log Level: $env:LOG_LEVEL" -ForegroundColor Gray
}

function Test-SystemHealth {
    if ($SkipHealthCheck) {
        Write-Host "`nSkipping health checks..." -ForegroundColor Yellow
        return
    }
    
    Write-Host "`nRunning health checks..." -ForegroundColor Yellow
    
    # Check disk space
    try {
        $disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
        $freeSpaceGB = [math]::Round($disk.FreeSpace / 1GB, 2)
        if ($freeSpaceGB -lt 1) {
            Write-Host "[!] Low disk space: ${freeSpaceGB}GB available" -ForegroundColor Yellow
        } else {
            Write-Host "[Y] Disk space OK: ${freeSpaceGB}GB free" -ForegroundColor Green
        }
    } catch {
        Write-Host "[!] Could not check disk space" -ForegroundColor Yellow
    }
    
    # Check memory
    try {
        $memory = Get-WmiObject -Class Win32_ComputerSystem
        $totalMemoryGB = [math]::Round($memory.TotalPhysicalMemory / 1GB, 2)
        if ($totalMemoryGB -lt 2) {
            Write-Host "[!] Low memory: ${totalMemoryGB}GB total" -ForegroundColor Yellow
        } else {
            Write-Host "[Y] Memory OK: ${totalMemoryGB}GB total" -ForegroundColor Green
        }
    } catch {
        Write-Host "[!] Could not check memory" -ForegroundColor Yellow
    }
}

function Start-Application {
    Write-Host "`n================================================" -ForegroundColor Green
    Write-Host "   Bootstrap completed successfully!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    
    Write-Host "`nStarting Streamlit application..." -ForegroundColor Yellow
    Write-Host "Access the application at: http://localhost:$env:STREAMLIT_PORT" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Green
    
    # Start the application using run.py for better cross-platform support
    try {
        python run.py
    } catch {
        Write-Host "Error starting with run.py, trying direct streamlit..." -ForegroundColor Yellow
        streamlit run src\main.py --server.port=$env:STREAMLIT_PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false --theme.base=dark --theme.primaryColor=#4ea4ff --theme.backgroundColor=#0f1419 --theme.secondaryBackgroundColor=#18202a --theme.textColor=#e6edf3
    }
}

# Main execution
try {
    Write-Host "`nStarting bootstrap sequence..." -ForegroundColor Yellow
    
    # Check requirements
    if (-not (Test-Requirements)) {
        Write-Host "`nBootstrap failed: Missing critical requirements" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Initialize directories
    Initialize-Directories
    
    # Validate environment
    Test-Environment
    
    # Run health checks
    Test-SystemHealth
    
    # Start application
    Start-Application
    
} catch {
    Write-Host "`nBootstrap failed with error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}