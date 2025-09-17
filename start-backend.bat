@echo off
echo Starting Career Tracking Backend...
cd "career-tracking-backend"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
