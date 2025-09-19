#!/usr/bin/env python3
"""
Create a test user for authentication testing
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'career-tracking-backend'))

from app.database import get_db, engine
from app.models.user import User
from app.services.auth_service import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_test_user():
    """Create a test user"""
    print("🔧 Creating test user...")
    
    async with engine.begin() as conn:
        # Create tables if they don't exist
        from app.models import Base
        await conn.run_sync(Base.metadata.create_all)
    
    async for db in get_db():
        try:
            # Check if user already exists
            result = await db.execute(select(User).filter(User.email == "test@example.com"))
            existing_user = result.scalars().first()
            
            if existing_user:
                print("✅ Test user already exists!")
                print(f"   Email: test@example.com")
                print(f"   Password: password123")
                return
            
            # Create new test user
            hashed_password = get_password_hash("password123")
            test_user = User(
                email="test@example.com",
                hashed_password=hashed_password,
                full_name="Test User",
                is_active=True,
                interests=["programming", "technology", "web development"]
            )
            
            db.add(test_user)
            await db.commit()
            await db.refresh(test_user)
            
            print("✅ Test user created successfully!")
            print(f"   Email: test@example.com")
            print(f"   Password: password123")
            print(f"   User ID: {test_user.id}")
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            await db.rollback()
        finally:
            await db.close()
            break

if __name__ == "__main__":
    asyncio.run(create_test_user())
