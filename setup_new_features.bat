@echo off
echo ========================================
echo Setting up new Career Tracking features
echo ========================================
echo.

echo 1. Adding interests column to database...
cd career-tracking-backend
python add_interests_column.py
if %errorlevel% neq 0 (
    echo Failed to add interests column
    pause
    exit /b 1
)

echo.
echo 2. Testing new features...
cd ..
python test_new_features.py
if %errorlevel% neq 0 (
    echo Some tests failed. Please check the output above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo New features added:
echo - Header integration in Dashboard
echo - User interests profile section
echo - AI-powered course recommendations
echo - Enhanced UI/UX with animations
echo.
echo To start the application:
echo 1. Run: start-backend.bat
echo 2. Run: start-frontend.bat
echo 3. Visit: http://localhost:3000
echo.
pause
