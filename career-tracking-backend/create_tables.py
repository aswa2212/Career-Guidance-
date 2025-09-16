#!/usr/bin/env python3
"""
Database initialization script for Career Tracking System
Run this script to create all tables in your PostgreSQL database
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
from app.models import Base  # This imports all models

async def create_tables():
    """Create all database tables"""
    print("🔗 Connecting to database...")
    print(f"Database URL: {settings.DATABASE_URL.replace('password', '***')}")
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            print("📋 Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("✅ All tables created successfully!")
            
        # List created tables
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            )
            tables = result.fetchall()
            print("\n📊 Created tables:")
            for table in tables:
                print(f"  - {table[0]}")
                
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your database credentials in .env file")
        print("2. Ensure PostgreSQL is running")
        print("3. Verify database exists")
        
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())
