#!/usr/bin/env python3
"""
Database migration script to add interests column to users table
Run this script to update the database schema
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def add_interests_column():
    """Add interests column to users table"""
    
    # Database connection parameters
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and "postgresql+asyncpg" in DATABASE_URL:
        # Convert asyncpg URL to standard postgresql URL for asyncpg.connect
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    elif not DATABASE_URL:
        # Construct from individual components
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "Postgresql%400001")  # URL encoded
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "career_db")
        
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        # Connect to database
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected to database successfully")
        
        # Check if interests column already exists
        check_column_query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'interests';
        """
        
        result = await conn.fetch(check_column_query)
        
        if result:
            print("Interests column already exists in users table")
        else:
            # Add interests column
            add_column_query = """
            ALTER TABLE users 
            ADD COLUMN interests JSONB DEFAULT '[]'::jsonb;
            """
            
            await conn.execute(add_column_query)
            print("Successfully added interests column to users table")
            
            # Create an index on the interests column for better performance
            create_index_query = """
            CREATE INDEX IF NOT EXISTS idx_users_interests 
            ON users USING GIN (interests);
            """
            
            await conn.execute(create_index_query)
            print("Created GIN index on interests column")
        
        # Close connection
        await conn.close()
        print("Database connection closed")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Adding interests column to users table...")
    success = asyncio.run(add_interests_column())
    
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
        exit(1)
