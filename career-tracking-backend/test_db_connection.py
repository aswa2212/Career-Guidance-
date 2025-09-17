import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = "postgresql+asyncpg://postgres:Postgresql%400001@localhost:5433/career_db"

async def test_database():
    """Test database connection and show data"""
    try:
        print("Testing database connection...")
        
        # Create engine
        engine = create_async_engine(DATABASE_URL)
        
        async with engine.begin() as conn:
            # Test connection
            result = await conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print("Database connected successfully!")
            print(f"PostgreSQL Version: {version[0]}")
            
            # Check if tables exist
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            
            if tables:
                print(f"\nFound {len(tables)} tables:")
                for table in tables:
                    print(f"  - {table[0]}")
                
                # Show data counts
                print(f"\nData Summary:")
                for table_name in ['courses', 'careers', 'colleges', 'users']:
                    try:
                        result = await conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                        count = result.fetchone()[0]
                        print(f"  {table_name}: {count} records")
                        
                        # Show sample data
                        if count > 0:
                            if table_name == 'users':
                                result = await conn.execute(text(f"SELECT email FROM {table_name} LIMIT 3"))
                            else:
                                result = await conn.execute(text(f"SELECT * FROM {table_name} LIMIT 3"))
                            rows = result.fetchall()
                            for i, row in enumerate(rows, 1):
                                if table_name == 'users':
                                    print(f"    {i}. {row[0]}")
                                else:
                                    # Show title/name (usually second column)
                                    print(f"    {i}. {row[1] if len(row) > 1 else row[0]}")
                    except Exception as e:
                        print(f"  {table_name}: Error - {str(e)}")
                        
            else:
                print("No tables found in database")
                print("Run: python seed_data.py to create and populate tables")
                
    except Exception as e:
        print("Database connection failed!")
        print(f"Error: {e}")
        print("\nTo fix this:")
        print("1. Make sure PostgreSQL is running on port 5433")
        print("2. Database 'career_db' exists")
        print("3. Username 'postgres' with password 'Postgresql@0001'")
        print("4. Run: python seed_data.py to populate data")

if __name__ == "__main__":
    asyncio.run(test_database())
