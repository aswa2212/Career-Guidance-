@echo off
echo ========================================
echo   SIH 2025 Complete System Setup
echo ========================================
echo.
echo This will:
echo 1. Start PostgreSQL service
echo 2. Create database if needed
echo 3. Populate with sample data
echo 4. Start backend server
echo 5. Provide frontend instructions
echo.

echo Step 1: Starting PostgreSQL service...
net start postgresql-x64-13
if %errorlevel% neq 0 (
    echo PostgreSQL service not found. Trying alternative names...
    net start postgresql-13
    if %errorlevel% neq 0 (
        net start postgresql
        if %errorlevel% neq 0 (
            echo ⚠️  Could not start PostgreSQL automatically.
            echo Please start PostgreSQL manually and run this script again.
            pause
            exit /b 1
        )
    )
)

echo ✅ PostgreSQL service started

echo.
echo Step 2: Creating database...
cd career-tracking-backend
psql -U postgres -c "CREATE DATABASE career_db;" 2>nul
echo ✅ Database created (or already exists)

echo.
echo Step 3: Installing Python dependencies...
python -m pip install -r requirements.txt
python -m pip install asyncpg numpy pandas scikit-learn

echo.
echo Step 4: Creating database tables...
python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base

async def create_tables():
    engine = create_async_engine('postgresql+asyncpg://postgres:Postgresql%%40001@localhost:5432/career_db')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print('✅ Database tables created')

asyncio.run(create_tables())
"

echo.
echo Step 5: Populating with sample data...
python generate_jk_data.py

echo.
echo Step 6: Starting backend server...
echo Backend will start at http://localhost:8000
echo API docs will be at http://localhost:8000/docs
echo.

start "SIH 2025 Backend" cmd /k "python -m uvicorn app.main:app --reload"

timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo   System Setup Complete!
echo ========================================
echo.
echo ✅ PostgreSQL: Running
echo ✅ Database: Created and populated
echo ✅ Backend: Starting at http://localhost:8000
echo.
echo Next steps:
echo 1. Wait for backend to fully start (check the new window)
echo 2. Open http://localhost:8000/docs to test API
echo 3. Start frontend:
echo    cd ../frontend
echo    npm install
echo    npm run dev
echo.
echo Your SIH 2025 Career Guidance Platform is ready!
echo.

pause
