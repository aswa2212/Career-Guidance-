#!/usr/bin/env python3
"""
Test database connection and insert sample data
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import AsyncSessionLocal, engine
from app.models.user import User
from app.models.college import College
from app.models.career import Career
from app.services.auth_service import get_password_hash

async def test_connection():
    """Test database connection and create sample data"""
    print("🔗 Testing database connection...")
    
    try:
        async with AsyncSessionLocal() as session:
            # Test basic connection
            from sqlalchemy import text
            result = await session.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Create sample user
            print("\n👤 Creating sample user...")
            sample_user = User(
                email="test@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="Test User",
                is_active=True,
                role="user"
            )
            
            # Check if user already exists
            existing_user = await session.execute(
                select(User).filter(User.email == "test@example.com")
            )
            if not existing_user.scalars().first():
                session.add(sample_user)
                await session.commit()
                print("✅ Sample user created!")
            else:
                print("ℹ️ Sample user already exists")
            
            # Create sample college
            print("\n🏫 Creating sample college...")
            sample_college = College(
                name="Indian Institute of Technology Delhi",
                address="Hauz Khas, New Delhi",
                city="New Delhi",
                state="Delhi",
                pincode="110016",
                website="https://www.iitd.ac.in",
                latitude=28.5449,
                longitude=77.1928
            )
            
            existing_college = await session.execute(
                select(College).filter(College.name == "Indian Institute of Technology Delhi")
            )
            if not existing_college.scalars().first():
                session.add(sample_college)
                await session.commit()
                print("✅ Sample college created!")
            else:
                print("ℹ️ Sample college already exists")
            
            # Create sample career
            print("\n💼 Creating sample career...")
            sample_career = Career(
                title="Data Scientist",
                description="Analyze complex data to help organizations make informed decisions",
                field="Technology",
                median_salary="₹15,00,000 per year",
                job_outlook="Growing rapidly",
                required_skills="Python, Statistics, Machine Learning, SQL, Data Visualization"
            )
            
            existing_career = await session.execute(
                select(Career).filter(Career.title == "Data Scientist")
            )
            if not existing_career.scalars().first():
                session.add(sample_career)
                await session.commit()
                print("✅ Sample career created!")
            else:
                print("ℹ️ Sample career already exists")
            
            # Display all data
            print("\n📊 Current database contents:")
            
            users = await session.execute(select(User))
            print(f"Users: {len(users.scalars().all())}")
            
            colleges = await session.execute(select(College))
            print(f"Colleges: {len(colleges.scalars().all())}")
            
            careers = await session.execute(select(Career))
            print(f"Careers: {len(careers.scalars().all())}")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("\n🔧 Check:")
        print("1. PostgreSQL is running")
        print("2. Database credentials in .env are correct")
        print("3. Database exists")

if __name__ == "__main__":
    asyncio.run(test_connection())
