@echo off
echo ========================================
echo Career Tracking App - Complete Setup
echo ========================================
echo.

echo Step 1: Installing Python Dependencies...
cd career-tracking-backend
echo Installing backend requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed successfully!
echo.

echo Step 2: Creating ML Models...
python create_ml_model.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to create ML models
    pause
    exit /b 1
)
echo ✅ ML models created successfully!
echo.

echo Step 3: Installing Frontend Dependencies...
cd ..\Frontend
npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed successfully!
echo.

echo Step 4: Seeding Database with Sample Data...
cd ..\career-tracking-backend
python seed_data.py
if %errorlevel% neq 0 (
    echo WARNING: Database seeding failed - you may need to start PostgreSQL first
    echo You can run this step later after starting PostgreSQL
)
echo.

echo ========================================
echo Setup Complete! 🎉
echo ========================================
echo.
echo Your Career Tracking Application is ready!
echo.
echo IMPORTANT: Make sure PostgreSQL is running on port 5433
echo.
echo To start the application:
echo 1. Run start-all.bat
echo 2. Access Frontend: http://localhost:3000
echo 3. Access Backend API: http://localhost:8000
echo 4. API Documentation: http://localhost:8000/docs
echo.
echo If database seeding failed, start PostgreSQL and run:
echo cd career-tracking-backend
echo python seed_data.py
echo.
pause
