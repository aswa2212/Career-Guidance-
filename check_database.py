import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings

async def check_database_connection():
    """Check if database is connected and show table data"""
    try:
        # Test connection
        engine = create_async_engine(settings.DATABASE_URL)
        
        async with engine.begin() as conn:
            # Check if tables exist
            result = await conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = result.fetchall()
            
            if tables:
                print("✅ Database connected successfully!")
                print("\n📋 Available tables:")
                for table in tables:
                    print(f"  - {table[0]}")
                
                # Show sample data
                for table_name in ['courses', 'careers', 'colleges']:
                    try:
                        result = await conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = result.fetchone()[0]
                        print(f"\n📊 {table_name}: {count} records")
                        
                        if count > 0:
                            result = await conn.execute(f"SELECT * FROM {table_name} LIMIT 3")
                            rows = result.fetchall()
                            for i, row in enumerate(rows, 1):
                                print(f"  {i}. {row[1] if len(row) > 1 else row[0]}")  # Show title/name
                    except Exception as e:
                        print(f"  ⚠️ {table_name}: Table exists but no data")
                        
            else:
                print("⚠️ Database connected but no tables found")
                print("Run: python setup_database.bat to create tables")
                
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {e}")
        print("\n🔧 To fix this:")
        print("1. Install PostgreSQL on port 5433")
        print("2. Create database 'career_db'")
        print("3. Use username 'postgres' and password 'Postgresql@0001'")

if __name__ == "__main__":
    asyncio.run(check_database_connection())
