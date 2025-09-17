#!/usr/bin/env python3
"""
Simple test script to check if backend dependencies are working
"""
import sys

def test_imports():
    try:
        import fastapi
        print("✅ FastAPI available")
    except ImportError:
        print("❌ FastAPI not installed")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn available")
    except ImportError:
        print("❌ Uvicorn not installed")
        return False
    
    try:
        import asyncpg
        print("✅ AsyncPG available")
    except ImportError:
        print("❌ AsyncPG not installed")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy available")
    except ImportError:
        print("❌ SQLAlchemy not installed")
        return False
    
    return True

def test_database_connection():
    try:
        import asyncpg
        import asyncio
        
        async def test_conn():
            try:
                conn = await asyncpg.connect(
                    "postgresql://postgres:Postgresql@0001@localhost:5433/career_db"
                )
                await conn.close()
                print("✅ Database connection successful")
                return True
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                return False
        
        return asyncio.run(test_conn())
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Backend Dependencies...")
    print("=" * 40)
    
    if test_imports():
        print("\n" + "=" * 40)
        print("Testing Database Connection...")
        test_database_connection()
    else:
        print("\n❌ Some dependencies are missing. Run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("Backend test complete!")
