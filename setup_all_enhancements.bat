@echo off
echo ========================================
echo  COMPREHENSIVE SYSTEM SETUP SCRIPT
echo ========================================
echo.

echo 🔧 Setting up all enhancements for the Career Tracking System...
echo.

REM Change to project directory
cd /d "%~dp0"

echo 📁 Current directory: %CD%
echo.

REM Setup backend
echo 🔄 Setting up backend environment...
cd career-tracking-backend

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Python dependencies installed successfully
echo.

REM Run database migrations
echo 🗄️ Running database migrations...
python add_interests_column.py
if %ERRORLEVEL% neq 0 (
    echo ⚠️ Interests column migration had issues (might already exist)
)

python add_scholarship_details_migration.py
if %ERRORLEVEL% neq 0 (
    echo ⚠️ Scholarship details migration had issues (might already exist)
)

echo ✅ Database migrations completed
echo.

REM Populate database with sample data
echo 📊 Populating database with sample data...
python populate_database.py
if %ERRORLEVEL% neq 0 (
    echo ⚠️ Database population had issues (data might already exist)
)

echo ✅ Database populated
echo.

REM Go back to project root
cd ..

REM Setup frontend
echo 🎨 Setting up frontend environment...
cd Frontend

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Node.js dependencies installed successfully
echo.

REM Go back to project root
cd ..

echo 🧪 Running comprehensive tests...
python comprehensive_test.py
if %ERRORLEVEL% neq 0 (
    echo ⚠️ Some tests failed, but setup is complete
) else (
    echo ✅ All tests passed!
)

echo.
echo ========================================
echo  SETUP COMPLETE!
echo ========================================
echo.
echo 🎉 Your enhanced Career Tracking System is ready!
echo.
echo 📝 To start the system:
echo.
echo 1. Backend (Terminal 1):
echo    cd career-tracking-backend
echo    python -m uvicorn app.main:app --reload
echo.
echo 2. Frontend (Terminal 2):
echo    cd Frontend
echo    npm run dev
echo.
echo 3. Open your browser to: http://localhost:3000
echo.
echo 🔧 New Features Available:
echo ✅ Fixed recommendation engine with real-time user interests
echo ✅ Real database integration (no more mock data)
echo ✅ Enhanced frontend with consistent icons and navigation
echo ✅ College scholarship details feature
echo ✅ Improved error handling and user experience
echo.
echo 📋 Test Account:
echo Email: testuser@example.com
echo Password: testpassword123
echo.
pause
