#!/usr/bin/env python3
"""
Database migration script to add scholarship_details column to colleges table
"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def add_scholarship_details_column():
    """Add scholarship_details column to colleges table"""
    
    # Get database URL
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and "postgresql+asyncpg" in DATABASE_URL:
        # Convert asyncpg URL to standard postgresql URL for asyncpg.connect
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    elif not DATABASE_URL:
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "Postgresql%400001")  # URL encoded
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "career_db")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    print("🔄 Connecting to database...")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Check if column already exists
        check_column = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'colleges' AND column_name = 'scholarship_details';
        """
        
        result = await conn.fetch(check_column)
        
        if result:
            print("✅ scholarship_details column already exists in colleges table")
        else:
            print("🔧 Adding scholarship_details column to colleges table...")
            
            # Add the column
            alter_query = """
            ALTER TABLE colleges 
            ADD COLUMN scholarship_details TEXT;
            """
            
            await conn.execute(alter_query)
            print("✅ Successfully added scholarship_details column")
            
            # Add some sample scholarship data
            print("📝 Adding sample scholarship data...")
            
            sample_scholarships = [
                "Merit-based scholarships up to 50% tuition fee waiver. Need-based financial aid available. Sports scholarships for exceptional athletes.",
                "Academic excellence scholarships for top 10% students. Research assistantships available for graduate programs. Industry-sponsored scholarships.",
                "Full tuition scholarships for economically disadvantaged students. Partial scholarships based on entrance exam scores. Alumni-funded scholarships.",
                "Government scholarships available through state quota. Private foundation scholarships for STEM programs. International student scholarships.",
                "Corporate-sponsored scholarships for engineering students. Women in technology scholarships. Rural area student special scholarships."
            ]
            
            # Update existing colleges with sample scholarship data
            update_query = """
            UPDATE colleges 
            SET scholarship_details = $1 
            WHERE id = $2;
            """
            
            # Get existing college IDs
            college_ids = await conn.fetch("SELECT id FROM colleges LIMIT 10;")
            
            for i, college in enumerate(college_ids):
                scholarship_text = sample_scholarships[i % len(sample_scholarships)]
                await conn.execute(update_query, scholarship_text, college['id'])
            
            print(f"✅ Updated {len(college_ids)} colleges with sample scholarship data")
        
        await conn.close()
        print("🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise

async def main():
    """Main function"""
    print("🚀 Starting scholarship_details migration...")
    await add_scholarship_details_column()

if __name__ == "__main__":
    asyncio.run(main())
