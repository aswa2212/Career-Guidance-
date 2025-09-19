#!/usr/bin/env python3
"""
Simple database migration to ensure interests column exists and works properly
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'career-tracking-backend'))

from sqlalchemy import text
from app.database import engine
from app.models.user import User
from app.services.auth_service import get_password_hash

async def fix_interests_migration():
    """Ensure interests column exists and create test user"""
    print("🔧 Fixing interests migration...")
    
    try:
        async with engine.begin() as conn:
            # Check if interests column exists
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'interests'
            """))
            
            interests_column_exists = result.fetchone() is not None
            
            if not interests_column_exists:
                print("📝 Adding interests column...")
                await conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN interests JSON DEFAULT '[]'::json
                """))
                print("✅ Interests column added successfully!")
            else:
                print("✅ Interests column already exists!")
            
            # Create or update test user
            print("👤 Creating/updating test user...")
            
            # Check if test user exists
            result = await conn.execute(text("""
                SELECT id, email, interests FROM users WHERE email = 'test@example.com'
            """))
            
            existing_user = result.fetchone()
            
            if existing_user:
                print(f"✅ Test user exists with ID: {existing_user[0]}")
                print(f"   Current interests: {existing_user[2]}")
                
                # Update interests if empty
                if not existing_user[2] or existing_user[2] == []:
                    await conn.execute(text("""
                        UPDATE users 
                        SET interests = '["programming", "technology", "web development"]'::json
                        WHERE email = 'test@example.com'
                    """))
                    print("✅ Updated test user interests!")
            else:
                # Create new test user
                hashed_password = get_password_hash("password123")
                await conn.execute(text("""
                    INSERT INTO users (email, hashed_password, full_name, is_active, interests)
                    VALUES (:email, :password, :name, :active, :interests)
                """), {
                    "email": "test@example.com",
                    "password": hashed_password,
                    "name": "Test User",
                    "active": True,
                    "interests": '["programming", "technology", "web development"]'
                })
                print("✅ Test user created successfully!")
            
            # Verify the setup
            result = await conn.execute(text("""
                SELECT id, email, full_name, interests FROM users WHERE email = 'test@example.com'
            """))
            
            user_data = result.fetchone()
            if user_data:
                print(f"\n🎯 Test User Details:")
                print(f"   ID: {user_data[0]}")
                print(f"   Email: {user_data[1]}")
                print(f"   Name: {user_data[2]}")
                print(f"   Interests: {user_data[3]}")
                print(f"\n🔑 Login Credentials:")
                print(f"   Email: test@example.com")
                print(f"   Password: password123")
            
        print("\n✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(fix_interests_migration())
    if success:
        print("\n🚀 You can now test the interests functionality!")
        print("   1. Login with test@example.com / password123")
        print("   2. Go to Settings page to manage interests")
        print("   3. Check Dashboard for personalized recommendations")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
