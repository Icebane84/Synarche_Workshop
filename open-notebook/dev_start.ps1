<#
==============================================================================
ARTIFACT ID: CODE-DEV-START-001
OFFICIAL NAME: dev_start.ps1
VERSION: v13.2 [OMEGA]
DOMAIN: CODE
EVOLUTION: Omega Ascension
STATUS: [ACTIVE]
RELATIONS: GOVERNED_BY: CORE-CODEX-001
==============================================================================
#>

# Force UTF-8 for the entire session
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

Write-Host "🚀 Starting Open Notebook Local Environment (Synarche Stable)..." -ForegroundColor Cyan

# 1. Project Root Detection
if (Test-Path (Join-Path $PSScriptRoot "run_api.py")) {
    $root = $PSScriptRoot
} elseif (Test-Path (Join-Path $PSScriptRoot "open_notebook\run_api.py")) {
    $root = Join-Path $PSScriptRoot "open_notebook"
} else {
    Write-Error "Could not locate project root (run_api.py not found). Please run this script from the project root."
    exit 1
}

# 2. Virtual Environment Configuration
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Warning "Virtual environment not found at .venv. Please ensure dependencies are installed."
    $venvPython = "python"
} else {
    Write-Host "Using Virtual Environment: $venvPython" -ForegroundColor Gray
}

# 3. Port Conflict Detection
function Test-Port {
    param($port)
    return (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue)
}

Write-Host "Checking for existing services..." -ForegroundColor Gray
if (Test-Port 8000) { Write-Warning "Port 8000 is busy (SurrealDB?). Skipping startup for Terminal 1." }
if (Test-Port 5055) { Write-Warning "Port 5055 is busy (API?). Skipping startup for Terminal 2." }
if (Test-Port 8501) { Write-Warning "Port 8501 is busy (Streamlit?). Skipping startup for Terminal 4." }

# 4. Service Launchers
$apiScript = Join-Path $root "run_api.py"
$appScript = Join-Path $root "app_home.py"
$workerCmd = "$venvPython -m surreal_commands.cli.worker --import-modules commands"

# Terminal 1: SurrealDB
if (-not (Test-Port 8000)) {
    Write-Host "Starting Terminal 1: SurrealDB" -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 1: SurrealDB'; cd '$root'; surreal start --user root --pass root file:surreal.db --bind 127.0.0.1:8000"
}

# Terminal 2: API Server
if (-not (Test-Port 5055)) {
    Write-Host "Starting Terminal 2: API Server" -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 2: API Server'; cd '$root'; `$env:API_RELOAD='false'; `$env:PYTHONIOENCODING='utf-8'; & '$venvPython' '$apiScript'"
}

# Terminal 3: Background Worker
Write-Host "Starting Terminal 3: Background Worker" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 3: Background Worker'; cd '$root'; `$env:PYTHONIOENCODING='utf-8'; $workerCmd"

# Terminal 4: Streamlit App
if (-not (Test-Port 8501)) {
    Write-Host "Starting Terminal 4: Streamlit App" -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 4: Streamlit App'; cd '$root'; & '$venvPython' -m streamlit run '$appScript'"
}

# Terminal 5: Next.js Frontend
$frontendPath = Join-Path $root "frontend"
if (Test-Path $frontendPath) {
    if (-not (Test-Port 3000)) {
        Write-Host "Starting Terminal 5: Next.js Frontend" -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'Terminal 5: Next.js Frontend'; cd '$frontendPath'; npm run dev"
    }
}

Write-Host "`n✅ All services initiated." -ForegroundColor Cyan
Write-Host "   - Database:  ws://localhost:8000/rpc"
Write-Host "   - API:       http://localhost:5055/docs"
Write-Host "   - Streamlit: http://localhost:8501"
Write-Host "   - Frontend:  http://localhost:3000"
Write-Host "`nKeep this window open to monitor launch progress."
Read-Host "Press Enter to exit this launcher script..."
