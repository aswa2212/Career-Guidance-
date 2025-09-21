#!/usr/bin/env python3
"""
Quick script to populate basic data (courses, colleges, careers) to fix server errors
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.course import Course
from app.models.college import College
from app.models.career import Career

# Database URL
DATABASE_URL = "postgresql+asyncpg://postgres:Postgresql%400001@localhost/career_db"

# Sample data
SAMPLE_COURSES = [
    {
        "title": "Computer Science Engineering",
        "description": "Comprehensive program covering programming, algorithms, data structures, and software engineering",
        "duration": "4 years",
        "provider": "Various Universities",
        "category": "Engineering",
        "difficulty_level": "Intermediate"
    },
    {
        "title": "Data Science",
        "description": "Master data analysis, machine learning, statistics, and big data technologies",
        "duration": "2 years",
        "provider": "Tech Institutes",
        "category": "Technology",
        "difficulty_level": "Advanced"
    },
    {
        "title": "Web Development",
        "description": "Full-stack web development with modern frameworks and technologies",
        "duration": "6 months",
        "provider": "Online Platforms",
        "category": "Programming",
        "difficulty_level": "Beginner"
    },
    {
        "title": "Digital Marketing",
        "description": "Learn modern digital marketing strategies and tools",
        "duration": "3 months",
        "provider": "Marketing Institutes",
        "category": "Marketing",
        "difficulty_level": "Beginner"
    },
    {
        "title": "Artificial Intelligence",
        "description": "Advanced AI concepts including neural networks, deep learning, and cognitive computing",
        "duration": "2 years",
        "provider": "AI Research Centers",
        "category": "Technology",
        "difficulty_level": "Advanced"
    }
]

SAMPLE_COLLEGES = [
    {
        "name": "Indian Institute of Technology Delhi",
        "address": "Hauz Khas, New Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110016",
        "website": "https://home.iitd.ac.in/",
        "latitude": 28.5449,
        "longitude": 77.1928,
        "scholarship_details": "Merit-based scholarships available"
    },
    {
        "name": "Indian Institute of Technology Bombay",
        "address": "Powai, Mumbai",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400076",
        "website": "https://www.iitb.ac.in/",
        "latitude": 19.1334,
        "longitude": 72.9133,
        "scholarship_details": "Need-based and merit scholarships"
    },
    {
        "name": "Delhi University",
        "address": "University Enclave, Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110007",
        "website": "https://www.du.ac.in/",
        "latitude": 28.6862,
        "longitude": 77.2090,
        "scholarship_details": "Various government scholarships available"
    }
]

SAMPLE_CAREERS = [
    {
        "title": "Software Developer",
        "description": "Design, develop, and maintain software applications and systems",
        "field": "Technology",
        "median_salary": "₹8,50,000",
        "job_outlook": "Excellent",
        "required_skills": "Programming, Problem Solving, Software Design, Testing"
    },
    {
        "title": "Data Scientist",
        "description": "Analyze complex data to help organizations make informed decisions",
        "field": "Technology",
        "median_salary": "₹12,00,000",
        "job_outlook": "Very Good",
        "required_skills": "Python, Statistics, Machine Learning, Data Visualization"
    },
    {
        "title": "Digital Marketing Specialist",
        "description": "Create and manage online marketing campaigns and strategies",
        "field": "Marketing",
        "median_salary": "₹6,00,000",
        "job_outlook": "Good",
        "required_skills": "SEO, Social Media, Content Marketing, Analytics"
    }
]

async def populate_data():
    """Populate basic data to fix server errors"""
    try:
        # Create async engine
        engine = create_async_engine(DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            # Check and add courses
            from sqlalchemy import select
            result = await session.execute(select(Course))
            existing_courses = result.scalars().all()
            
            if not existing_courses:
                print("Adding sample courses...")
                for course_data in SAMPLE_COURSES:
                    course = Course(**course_data)
                    session.add(course)
                print(f"Added {len(SAMPLE_COURSES)} courses")
            else:
                print(f"Found {len(existing_courses)} existing courses")
            
            # Check and add colleges
            result = await session.execute(select(College))
            existing_colleges = result.scalars().all()
            
            if not existing_colleges:
                print("Adding sample colleges...")
                for college_data in SAMPLE_COLLEGES:
                    college = College(**college_data)
                    session.add(college)
                print(f"Added {len(SAMPLE_COLLEGES)} colleges")
            else:
                print(f"Found {len(existing_colleges)} existing colleges")
            
            # Check and add careers
            result = await session.execute(select(Career))
            existing_careers = result.scalars().all()
            
            if not existing_careers:
                print("Adding sample careers...")
                for career_data in SAMPLE_CAREERS:
                    career = Career(**career_data)
                    session.add(career)
                print(f"Added {len(SAMPLE_CAREERS)} careers")
            else:
                print(f"Found {len(existing_careers)} existing careers")
            
            await session.commit()
            print("✅ Data population completed successfully!")
            
    except Exception as e:
        print(f"❌ Error populating data: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(populate_data())
