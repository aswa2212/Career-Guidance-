@echo off
echo ========================================
echo Quick Setup for Career Tracking System
echo ========================================
echo.

echo Step 1: Checking PostgreSQL service...
sc query postgresql-x64-16 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL 16 service found and running
) else (
    net start postgresql-x64-16 >nul 2>&1
    if %errorlevel% neq 0 (
        net start postgresql-x64-15 >nul 2>&1
        if %errorlevel% neq 0 (
            net start postgresql-x64-14 >nul 2>&1
            if %errorlevel% neq 0 (
                net start postgresql-x64-13 >nul 2>&1
                if %errorlevel% neq 0 (
                    echo ❌ Could not start PostgreSQL. Please start it manually.
                    echo Try: Services.msc -> Find PostgreSQL -> Start
                    pause
                    exit /b 1
                )
            )
        )
    )
    echo ✅ PostgreSQL service is running
)

echo.
echo Step 2: Adding interests column to database...
cd career-tracking-backend
python add_interests_column.py
if %errorlevel% neq 0 (
    echo ❌ Database migration failed
    echo Make sure PostgreSQL is running and credentials are correct
    pause
    exit /b 1
)

echo.
echo Step 3: Starting backend server...
echo Starting backend in background...
start /B python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 4: Testing setup...
cd ..
python test_new_features.py

echo.
echo ========================================
echo Setup completed!
echo ========================================
echo.
echo Backend is running at: http://localhost:8000
echo To start frontend, run: .\start-frontend.bat
echo.
pause
