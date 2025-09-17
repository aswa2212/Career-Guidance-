@echo off
echo ========================================
echo Setting up PostgreSQL Database
echo ========================================
echo.

echo Step 1: Creating database and tables...
cd career-tracking-backend
.venv\Scripts\activate.ps1; python -c "
import asyncio
from app.database import engine
from app.models import Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Database tables created!')

asyncio.run(create_tables())
"

echo.
echo Step 2: Adding sample data...
.venv\Scripts\activate.ps1; python seed_data.py

echo.
echo ========================================
echo Database setup complete! 🎉
echo ========================================
echo.
echo You can now view your data at:
echo - pgAdmin: http://localhost/pgadmin (if installed)
echo - Or use any PostgreSQL client
echo.
echo Database connection details:
echo Host: localhost
echo Port: 5433
echo Database: career_db
echo Username: postgres
echo Password: Postgresql@0001
echo.
pause
