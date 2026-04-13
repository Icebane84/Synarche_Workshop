<#
==============================================================================
ARTIFACT ID: CODE-DEV-START-001
OFFICIAL NAME: dev_start.ps1
VERSION: v13.1 [OMEGA]
DOMAIN: CODE
EVOLUTION: Omega Ascension
STATUS: [ACTIVE]
RELATIONS: GOVERNED_BY: CORE-CODEX-001
==============================================================================
Block D: Standardized Synergy Block (The Loom Signature)
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law.
#>

Write-Host "🚀 Starting Open Notebook Local Environment (Windows/Python 3.14)..." -ForegroundColor Cyan

# Define project root
# We look for run_api.py to anchor the root
if (Test-Path (Join-Path $PSScriptRoot "run_api.py")) {
    $root = $PSScriptRoot
} elseif (Test-Path (Join-Path $PSScriptRoot "open_notebook\run_api.py")) {
    $root = Join-Path $PSScriptRoot "open_notebook"
} else {
    Write-Error "Could not locate project root (run_api.py not found). Please run this script from the project root or its parent."
    exit 1
}

# Check for venv python
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Warning "Virtual environment not found at $venvPython. Using system 'python'."
    $venvPython = "python"
} else {
    Write-Host "Using Virtual Environment: $venvPython" -ForegroundColor Cyan
}

# Dependency Check
Write-Host "Checking dependencies..." -ForegroundColor Gray
& $venvPython -c "import streamlit; import surreal_commands; import uvicorn; import fastapi; print('Dependencies OK')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Dependencies appear missing!"
    Write-Host "Installing dependencies now (this may take a minute)..." -ForegroundColor Yellow
    & $venvPython -m pip install -e ".[dev]"
}

# Helper to find executable or module
function Get-Runner {
    param($exeName, $moduleName)
    $exePath = Join-Path $PSScriptRoot ".venv\Scripts\$exeName"
    if (Test-Path $exePath) {
        return "& '$exePath'"
    }
    return "& '$venvPython' -m $moduleName"
}

$streamlitCmd = Get-Runner "streamlit.exe" "streamlit"
# 'surreal-commands-worker' might verify as module 'surreal_commands.worker' if script missing
# We assume CLI script name first
$workerStartCmd = "$venvPython -m surreal_commands.cli.worker" 
if (Test-Path ".venv\Scripts\surreal-commands-worker.exe") {
    $workerStartCmd = "& '.venv\Scripts\surreal-commands-worker.exe'"
}

# Define script paths
$apiScript = Join-Path $root "run_api.py"
$appScript = Join-Path $root "app_home.py"

# 1. Start SurrealDB (Local)
Write-Host "Started Terminal 1: SurrealDB" -ForegroundColor Green
# Check for SurrealDB in PATH or User AppData
if (Get-Command "surreal" -ErrorAction SilentlyContinue) {
    $surrealCmd = "surreal"
} elseif (Test-Path "$env:LOCALAPPDATA\SurrealDB\surreal.exe") {
    $surrealCmd = "& '$env:LOCALAPPDATA\SurrealDB\surreal.exe'"
} else {
    Write-Warning "SurrealDB not found! Please install it."
    $surrealCmd = "surreal" # Fallback to hope it works or fails visibly
}
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 1: SurrealDB'; cd '$root'; $surrealCmd start --user root --pass root file://surreal.db"

# 2. Start API Server (Backend)
# API_RELOAD="false" is critical for Python 3.14 compat
Write-Host "Started Terminal 2: API Server" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 2: API Server'; cd '$root'; `$env:API_RELOAD='false'; & '$venvPython' '$apiScript'"

# 3. Start Background Worker
Write-Host "Started Terminal 3: Background Worker" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 3: Background Worker'; cd '$root'; $workerStartCmd --import-modules commands"

# 4. Start Application (Web UI)
Write-Host "Started Terminal 4: Streamlit App" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 4: Streamlit App'; cd '$root'; $streamlitCmd run '$appScript'"

# 5. Start Frontend (Next.js)
Write-Host "Started Terminal 5: Next.js Frontend" -ForegroundColor Green
$frontendPath = Join-Path $root "frontend"
if (-not (Test-Path $frontendPath)) {
    Write-Warning "Frontend directory not found at $frontendPath. Frontend will not start."
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 5: Next.js Frontend'; cd '$frontendPath'; npm run dev"
}

Write-Host "✅ All services launched in separate windows." -ForegroundColor Cyan
Write-Host "   - Database: ws://localhost:8000/rpc"
Write-Host "   - API:      http://localhost:5055/docs"
Write-Host "   - Streamlit: http://localhost:8501"
Write-Host "   - Frontend:  http://localhost:3000"
