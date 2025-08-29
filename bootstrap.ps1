# Bootstrap script for Comment Analyzer on Windows (PowerShell)
# Complete automated setup for non-technical users v2.0

param(
    [switch]$SkipHealthCheck,
    [switch]$SkipDependencyInstall,
    [string]$Port = "8501"
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"

Write-Host "================================================" -ForegroundColor Green
Write-Host "   Comment Analyzer - PowerShell Bootstrap v2.0" -ForegroundColor Green
Write-Host "   Automated Setup for Windows Users" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

function Test-PythonInstallation {
    Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
    
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $majorVersion = [int]$matches[1]
            $minorVersion = [int]$matches[2]
            
            if ($majorVersion -eq 3 -and $minorVersion -ge 8) {
                Write-Host "[✓] Python $($matches[0]) found" -ForegroundColor Green
                return $true
            } else {
                Write-Host "[!] Python version too old: $($matches[0]). Need Python 3.8+" -ForegroundColor Yellow
                return $false
            }
        }
    } catch {
        Write-Host "[✗] Python not found or not working" -ForegroundColor Red
        return $false
    }
    return $false
}

function Install-Python {
    Write-Host "`nPython installation required..." -ForegroundColor Yellow
    Write-Host "================================================" -ForegroundColor Yellow
    Write-Host "PYTHON INSTALLATION NEEDED" -ForegroundColor Yellow
    Write-Host "================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This application requires Python 3.8 or later." -ForegroundColor White
    Write-Host "We'll guide you through the installation process." -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor White
    Write-Host "1. Automatic installation (Recommended)" -ForegroundColor Green
    Write-Host "2. Manual installation (Advanced users)" -ForegroundColor Yellow
    Write-Host "3. Exit and install later" -ForegroundColor Red
    Write-Host ""
    
    do {
        $choice = Read-Host "Select option (1-3)"
        switch ($choice) {
            "1" { 
                return Install-PythonAutomatic 
            }
            "2" { 
                Write-Host ""
                Write-Host "Manual Installation:" -ForegroundColor Yellow
                Write-Host "1. Visit: https://www.python.org/downloads/"
                Write-Host "2. Download Python 3.8+ for Windows"
                Write-Host "3. During installation, check 'Add Python to PATH'"
                Write-Host "4. Restart this script after installation"
                Read-Host "Press Enter to exit"
                exit 0
            }
            "3" { 
                Write-Host "Installation cancelled by user" -ForegroundColor Red
                exit 0 
            }
            default { 
                Write-Host "Invalid option. Please select 1, 2, or 3." -ForegroundColor Red 
            }
        }
    } while ($true)
}

function Install-PythonAutomatic {
    Write-Host "`nStarting automatic Python installation..." -ForegroundColor Green
    
    try {
        # Check if winget is available (Windows 10 1709+ and Windows 11)
        $wingetAvailable = Get-Command winget -ErrorAction SilentlyContinue
        
        if ($wingetAvailable) {
            Write-Host "Using Windows Package Manager (winget)..." -ForegroundColor Yellow
            Write-Host "Installing Python 3.11..." -ForegroundColor Yellow
            
            $installProcess = Start-Process -FilePath "winget" -ArgumentList "install", "Python.Python.3.11", "--accept-source-agreements", "--accept-package-agreements" -Wait -PassThru
            
            if ($installProcess.ExitCode -eq 0) {
                Write-Host "[✓] Python installed successfully!" -ForegroundColor Green
                Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
                $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
                return $true
            } else {
                Write-Host "[!] Winget installation failed" -ForegroundColor Yellow
                return Install-PythonFallback
            }
        } else {
            return Install-PythonFallback
        }
    } catch {
        Write-Host "[!] Automatic installation failed: $_" -ForegroundColor Yellow
        return Install-PythonFallback
    }
}

function Install-PythonFallback {
    Write-Host "Fallback: Manual download method..." -ForegroundColor Yellow
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    
    try {
        Write-Host "Downloading Python installer..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
        
        Write-Host "Running Python installer..." -ForegroundColor Yellow
        Write-Host "Please check 'Add Python to PATH' during installation!" -ForegroundColor Red
        
        Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_test=0" -Wait
        
        # Clean up
        Remove-Item $installerPath -ErrorAction SilentlyContinue
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        Write-Host "[✓] Python installation completed!" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[✗] Failed to download/install Python: $_" -ForegroundColor Red
        Write-Host "Please install Python manually from https://www.python.org/downloads/" -ForegroundColor Yellow
        return $false
    }
}

function Install-Dependencies {
    if ($SkipDependencyInstall) {
        Write-Host "`nSkipping dependency installation..." -ForegroundColor Yellow
        return $true
    }
    
    Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
    
    # Check if requirements.txt exists
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "[✗] requirements.txt not found" -ForegroundColor Red
        return $false
    }
    
    try {
        Write-Host "Upgrading pip..." -ForegroundColor Yellow
        python -m pip install --upgrade pip --quiet
        
        Write-Host "Installing application dependencies..." -ForegroundColor Yellow
        Write-Host "(This may take a few minutes)" -ForegroundColor Gray
        
        $installProcess = Start-Process -FilePath "python" -ArgumentList "-m", "pip", "install", "-r", "requirements.txt", "--quiet" -Wait -PassThru -NoNewWindow
        
        if ($installProcess.ExitCode -eq 0) {
            Write-Host "[✓] Dependencies installed successfully!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[✗] Failed to install dependencies" -ForegroundColor Red
            Write-Host "Trying with verbose output..." -ForegroundColor Yellow
            python -m pip install -r requirements.txt
            return $false
        }
    } catch {
        Write-Host "[✗] Error during dependency installation: $_" -ForegroundColor Red
        return $false
    }
}

function Setup-ApiKey {
    Write-Host "`nChecking OpenAI API configuration..." -ForegroundColor Yellow
    
    # Check environment variable first
    $apiKey = $env:OPENAI_API_KEY
    
    # Check .env file
    if (-not $apiKey -and (Test-Path ".env")) {
        Write-Host "Loading environment from .env file..." -ForegroundColor Gray
        Get-Content ".env" | ForEach-Object {
            if ($_ -match "^OPENAI_API_KEY=(.+)$") {
                $env:OPENAI_API_KEY = $matches[1].Trim('"')
                $apiKey = $matches[1].Trim('"')
            }
        }
    }
    
    if (-not $apiKey) {
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Yellow
        Write-Host "OPENAI API KEY SETUP REQUIRED" -ForegroundColor Yellow
        Write-Host "================================================" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "This application requires an OpenAI API key to analyze comments." -ForegroundColor White
        Write-Host ""
        Write-Host "How to get an API key:" -ForegroundColor Green
        Write-Host "1. Visit: https://platform.openai.com/api-keys" -ForegroundColor White
        Write-Host "2. Sign up or log in to your OpenAI account" -ForegroundColor White
        Write-Host "3. Click 'Create new secret key'" -ForegroundColor White
        Write-Host "4. Copy the key (it starts with 'sk-')" -ForegroundColor White
        Write-Host ""
        
        $setupChoice = Read-Host "Do you have an API key ready? (y/n)"
        
        if ($setupChoice -eq "y" -or $setupChoice -eq "Y") {
            do {
                Write-Host ""
                $userApiKey = Read-Host "Please enter your OpenAI API key" -MaskInput
                
                if ($userApiKey -and $userApiKey.StartsWith("sk-") -and $userApiKey.Length -gt 20) {
                    # Create .env file
                    try {
                        "OPENAI_API_KEY=$userApiKey" | Out-File -FilePath ".env" -Encoding UTF8
                        $env:OPENAI_API_KEY = $userApiKey
                        Write-Host "[✓] API key saved to .env file" -ForegroundColor Green
                        return $true
                    } catch {
                        Write-Host "[✗] Failed to save API key: $_" -ForegroundColor Red
                        return $false
                    }
                } else {
                    Write-Host "[✗] Invalid API key format. Keys should start with 'sk-'" -ForegroundColor Red
                    $retry = Read-Host "Try again? (y/n)"
                    if ($retry -ne "y" -and $retry -ne "Y") {
                        return $false
                    }
                }
            } while ($true)
        } else {
            Write-Host ""
            Write-Host "Please get an API key from OpenAI and run this script again." -ForegroundColor Yellow
            Write-Host "The application cannot work without an API key." -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 0
        }
    } else {
        Write-Host "[✓] OpenAI API Key configured" -ForegroundColor Green
        return $true
    }
}

function Test-Requirements {
    Write-Host "`nValidating final installation..." -ForegroundColor Yellow
    
    $errors = 0
    
    # Final Python check
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "[✓] $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "[✗] Python still not available" -ForegroundColor Red
        $errors++
    }
    
    # Final Streamlit check
    try {
        python -c "import streamlit" 2>&1 | Out-Null
        Write-Host "[✓] Streamlit available" -ForegroundColor Green
    } catch {
        Write-Host "[✗] Streamlit still not available" -ForegroundColor Red
        $errors++
    }
    
    # Final API key check
    if ($env:OPENAI_API_KEY) {
        Write-Host "[✓] OpenAI API Key configured" -ForegroundColor Green
    } else {
        Write-Host "[✗] OpenAI API Key not set" -ForegroundColor Red
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
    Write-Host "   🚀 SETUP COMPLETED SUCCESSFULLY! 🚀" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting Comment Analyzer application..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📱 Access the application at: http://localhost:$env:STREAMLIT_PORT" -ForegroundColor Cyan
    Write-Host "🌐 Or: http://127.0.0.1:$env:STREAMLIT_PORT" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✋ To stop the application, press Ctrl+C" -ForegroundColor Gray
    Write-Host "================================================" -ForegroundColor Green
    
    # Set the port environment variable for run.py
    $env:STREAMLIT_PORT = $Port
    
    # Start the application using run.py for cross-platform compatibility
    try {
        if (Test-Path "run.py") {
            Write-Host "Starting via run.py..." -ForegroundColor Gray
            python run.py
        } else {
            Write-Host "run.py not found, using direct streamlit..." -ForegroundColor Yellow
            streamlit run src\main.py --server.port=$env:STREAMLIT_PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false --theme.base=dark --theme.primaryColor=#4ea4ff --theme.backgroundColor=#0f1419 --theme.secondaryBackgroundColor=#18202a --theme.textColor=#e6edf3
        }
    } catch {
        Write-Host ""
        Write-Host "[✗] Error starting application: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Troubleshooting:" -ForegroundColor Yellow
        Write-Host "1. Try running: python run.py" -ForegroundColor White
        Write-Host "2. Or: streamlit run src\main.py" -ForegroundColor White
        Write-Host "3. Check that all dependencies are installed" -ForegroundColor White
        Read-Host "Press Enter to exit"
    }
}

# Main execution
try {
    Write-Host "`nStarting automated setup sequence..." -ForegroundColor Yellow
    
    # Step 1: Check and install Python if needed
    if (-not (Test-PythonInstallation)) {
        if (-not (Install-Python)) {
            Write-Host "`nSetup failed: Python installation unsuccessful" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
        
        # Verify Python installation worked
        if (-not (Test-PythonInstallation)) {
            Write-Host "`nSetup failed: Python still not available after installation" -ForegroundColor Red
            Write-Host "Please restart your computer and try again, or install Python manually" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    # Step 2: Install dependencies
    if (-not (Install-Dependencies)) {
        Write-Host "`nSetup failed: Dependency installation unsuccessful" -ForegroundColor Red
        Write-Host "You can try running manually: pip install -r requirements.txt" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Step 3: Setup API key
    if (-not (Setup-ApiKey)) {
        Write-Host "`nSetup failed: API key configuration unsuccessful" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Step 4: Final validation
    if (-not (Test-Requirements)) {
        Write-Host "`nSetup failed: Final validation unsuccessful" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Step 5: Initialize directories
    Initialize-Directories
    
    # Step 6: Validate environment
    Test-Environment
    
    # Step 7: Run health checks
    Test-SystemHealth
    
    # Step 8: Start application
    Start-Application
    
} catch {
    Write-Host "`nBootstrap failed with error: $_" -ForegroundColor Red
    Write-Host "Please check the error message above and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}