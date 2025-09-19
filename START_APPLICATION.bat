@echo off
echo ========================================
echo   SIH 2025 Career Guidance Platform
echo ========================================
echo.
echo Starting your complete application...
echo.

echo 1. Starting Backend Server...
start "Backend Server" cmd /k "cd career-tracking-backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak > nul

echo 2. Starting Frontend Development Server...
start "Frontend Server" cmd /k "cd career-tracking-frontend && npm run dev"

echo.
echo ========================================
echo   Application Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.

pause
