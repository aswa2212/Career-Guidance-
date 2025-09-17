@echo off
echo Starting Career Tracking Application...
echo.
echo Installing/Updating Backend Dependencies...
cd career-tracking-backend
pip install -r requirements.txt
echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
cd ..\Frontend
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ================================
echo Career Tracking App is starting!
echo ================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Both servers will open in separate windows.
echo Close this window when done.
pause
