@echo off
title Open Notebook Launcher
echo ===================================================
echo   🚀 Starting Open Notebook Services...
echo ===================================================

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8


echo.
echo [1/4] Starting SurrealDB database container...
docker compose up -d surrealdb
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to start SurrealDB container. Make sure Docker Desktop is running!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/4] Starting API Backend in a new window...
start "Open Notebook API" cmd /k "uv run run_api.py"

echo.
echo [3/4] Starting Background Worker in a new window...
start "Open Notebook Worker" cmd /k "uv run --env-file .env surreal-commands-worker --import-modules commands"

echo.
echo [4/4] Starting Next.js Frontend in a new window...
start "Open Notebook Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo   ✅ All services initialized!
echo.
echo   📱 Frontend: http://localhost:3000
echo   🔗 API: http://localhost:5055
echo   📚 API Docs: http://localhost:5055/docs
echo.
echo   To stop all services, you can close the opened
echo   windows or double-click "stop.bat"
echo ===================================================
echo.
pause
