# setup_prs_db.ps1
# Created: 2026-02-23 03:29:00 EST
#
# This script automates the setup of a Python virtual environment,
# installs necessary packages, and orchestrates a PostgreSQL
# container via Docker Compose (Windows Native).

$VENV_DIR = ".venv_prs"
$COMPOSE_FILE = "docker-compose.yml"

Write-Host "--- Starting Dockerized PostgreSQL Setup for PRS ---" -ForegroundColor Cyan

# --- What: Create Python Virtual Environment ---
if (-not (Test-Path $VENV_DIR)) {
    Write-Host "Creating Python virtual environment in '$VENV_DIR'..."
    python -m venv $VENV_DIR
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error: Failed to create virtual environment."
        exit 1
    }
} else {
    Write-Host "Virtual environment '$VENV_DIR' already exists."
}

# --- What: Install Python Dependencies ---
Write-Host "Installing Python dependencies (psycopg2-binary)..."
$ActivateScript = Join-Path $VENV_DIR "Scripts" "Activate.ps1"

if (Test-Path $ActivateScript) {
    & $ActivateScript
    python -m pip install --upgrade pip
    pip install psycopg2-binary
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error: Failed to install Python packages."
        exit 1
    }
} else {
    Write-Error "Error: Activation script not found at $ActivateScript"
    exit 1
}

# --- What: Start Docker Container ---
Write-Host "Orchestrating PostgreSQL container..."
if (Test-Path $COMPOSE_FILE) {
    docker compose up -d
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error: Failed to start Docker container."
        exit 1
    }
    Write-Host "PostgreSQL container is running." -ForegroundColor Green
} else {
    Write-Error "Error: docker-compose.yml not found."
    exit 1
}

# --- What: Verify Connectivity ---
Write-Host "Verifying database connectivity..."
$TestScript = @"
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv("POSTGRES_DB", "prs_db"),
        user=os.getenv("POSTGRES_USER", "prs_user"),
        password=os.getenv("POSTGRES_PASSWORD", "prs_password")
    )
    print("Success: Connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"Error: Could not connect to database: {e}")
    exit(1)
"@

# Note: We need python-dotenv for the verification script
pip install python-dotenv
$TestScript | Out-File -FilePath "test_db.py" -Encoding utf8
python test_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "--- Setup Verified & Complete ---" -ForegroundColor Cyan
} else {
    Write-Error "Verification failed. Check if Docker container is fully initialized."
}
