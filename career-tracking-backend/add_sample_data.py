#!/usr/bin/env python3
"""
Simple script to add sample college data directly to fix server errors
No scrapers, no complex connections - just sample data
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def add_sample_data():
    """Add sample data using the same connection as the server"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        from app.models.course import Course
        from app.models.college import College
        from app.models.career import Career
        
        # Use the same database URL as the server
        DATABASE_URL = "postgresql+asyncpg://postgres:Postgresql%400001@localhost/career_db"
        
        # Create engine and session
        engine = create_async_engine(DATABASE_URL, echo=False)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            print("🔍 Checking existing data...")
            
            # Check colleges
            result = await session.execute(select(College))
            existing_colleges = result.scalars().all()
            print(f"Found {len(existing_colleges)} existing colleges")
            
            if len(existing_colleges) == 0:
                print("📚 Adding sample colleges...")
                sample_colleges = [
                    College(
                        name="Indian Institute of Technology Delhi",
                        address="Hauz Khas, New Delhi",
                        city="New Delhi",
                        state="Delhi",
                        pincode="110016",
                        website="https://home.iitd.ac.in/",
                        latitude=28.5449,
                        longitude=77.1928,
                        scholarship_details="Merit-based scholarships available"
                    ),
                    College(
                        name="Indian Institute of Technology Bombay",
                        address="Powai, Mumbai",
                        city="Mumbai",
                        state="Maharashtra",
                        pincode="400076",
                        website="https://www.iitb.ac.in/",
                        latitude=19.1334,
                        longitude=72.9133,
                        scholarship_details="Need-based and merit scholarships"
                    ),
                    College(
                        name="Delhi University",
                        address="University Enclave, Delhi",
                        city="New Delhi",
                        state="Delhi",
                        pincode="110007",
                        website="https://www.du.ac.in/",
                        latitude=28.6862,
                        longitude=77.2090,
                        scholarship_details="Various government scholarships available"
                    ),
                    College(
                        name="Jawaharlal Nehru University",
                        address="New Mehrauli Road, New Delhi",
                        city="New Delhi",
                        state="Delhi",
                        pincode="110067",
                        website="https://www.jnu.ac.in/",
                        latitude=28.5383,
                        longitude=77.1641,
                        scholarship_details="UGC scholarships and fellowships"
                    ),
                    College(
                        name="Anna University",
                        address="Sardar Patel Road, Guindy",
                        city="Chennai",
                        state="Tamil Nadu",
                        pincode="600025",
                        website="https://www.annauniv.edu/",
                        latitude=13.0067,
                        longitude=80.2206,
                        scholarship_details="State government scholarships available"
                    )
                ]
                
                for college in sample_colleges:
                    session.add(college)
                print(f"✅ Added {len(sample_colleges)} colleges")
            
            # Check courses
            result = await session.execute(select(Course))
            existing_courses = result.scalars().all()
            print(f"Found {len(existing_courses)} existing courses")
            
            if len(existing_courses) == 0:
                print("📖 Adding sample courses...")
                sample_courses = [
                    Course(
                        title="Computer Science Engineering",
                        description="Comprehensive program covering programming, algorithms, and software engineering",
                        duration="4 years",
                        provider="Various Universities",
                        category="Engineering",
                        difficulty_level="Intermediate"
                    ),
                    Course(
                        title="Data Science",
                        description="Master data analysis, machine learning, and statistics",
                        duration="2 years",
                        provider="Tech Institutes",
                        category="Technology",
                        difficulty_level="Advanced"
                    ),
                    Course(
                        title="Web Development",
                        description="Full-stack web development with modern frameworks",
                        duration="6 months",
                        provider="Online Platforms",
                        category="Programming",
                        difficulty_level="Beginner"
                    )
                ]
                
                for course in sample_courses:
                    session.add(course)
                print(f"✅ Added {len(sample_courses)} courses")
            
            # Check careers
            result = await session.execute(select(Career))
            existing_careers = result.scalars().all()
            print(f"Found {len(existing_careers)} existing careers")
            
            if len(existing_careers) == 0:
                print("💼 Adding sample careers...")
                sample_careers = [
                    Career(
                        title="Software Developer",
                        description="Design, develop, and maintain software applications",
                        field="Technology",
                        median_salary="₹8,50,000",
                        job_outlook="Excellent",
                        required_skills="Programming, Problem Solving, Software Design"
                    ),
                    Career(
                        title="Data Scientist",
                        description="Analyze complex data to help organizations make decisions",
                        field="Technology",
                        median_salary="₹12,00,000",
                        job_outlook="Very Good",
                        required_skills="Python, Statistics, Machine Learning"
                    )
                ]
                
                for career in sample_careers:
                    session.add(career)
                print(f"✅ Added {len(sample_careers)} careers")
            
            # Commit all changes
            await session.commit()
            print("🎉 Sample data added successfully!")
            
            # Final verification
            result = await session.execute(select(College))
            total_colleges = len(result.scalars().all())
            result = await session.execute(select(Course))
            total_courses = len(result.scalars().all())
            result = await session.execute(select(Career))
            total_careers = len(result.scalars().all())
            
            print(f"📊 Final counts:")
            print(f"   Colleges: {total_colleges}")
            print(f"   Courses: {total_courses}")
            print(f"   Careers: {total_careers}")
            print("✅ Database is ready for the API!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Adding sample data to fix college endpoint errors...")
    asyncio.run(add_sample_data())
