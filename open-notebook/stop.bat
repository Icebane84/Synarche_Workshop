@echo off
title Stop Open Notebook
echo ===================================================
echo   🛑 Stopping Open Notebook Services...
echo ===================================================
echo.

echo [1/3] Stopping Docker SurrealDB container...
docker compose down

echo.
echo [2/3] Terminating API and Worker processes...
taskkill /F /FI "WINDOWTITLE eq Open Notebook API" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Open Notebook Worker" >nul 2>&1

echo.
echo [3/3] Terminating Frontend processes...
taskkill /F /FI "WINDOWTITLE eq Open Notebook Frontend" >nul 2>&1

echo.
echo ===================================================
echo   ✅ All services stopped!
echo ===================================================
echo.
pause
