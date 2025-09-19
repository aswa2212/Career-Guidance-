#!/usr/bin/env python3
"""
Populate database with sample data for testing
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'career-tracking-backend'))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine
from app.models.college import College
from app.models.course import Course
from app.models.career import Career

async def populate_colleges():
    """Add sample colleges to database"""
    print("🏫 Adding sample colleges...")
    
    sample_colleges = [
        {
            "name": "SNS College of Technology",
            "address": "Sathy Road, Coimbatore",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "pincode": "641035",
            "website": "https://snsct.org",
            "latitude": 11.0168,
            "longitude": 76.9558
        },
        {
            "name": "Indian Institute of Technology Madras",
            "address": "IIT Madras, Chennai",
            "city": "Chennai", 
            "state": "Tamil Nadu",
            "pincode": "600036",
            "website": "https://iitm.ac.in",
            "latitude": 12.9916,
            "longitude": 80.2336
        },
        {
            "name": "Anna University",
            "address": "Sardar Patel Road, Guindy",
            "city": "Chennai",
            "state": "Tamil Nadu", 
            "pincode": "600025",
            "website": "https://annauniv.edu",
            "latitude": 13.0067,
            "longitude": 80.2206
        },
        {
            "name": "PSG College of Technology",
            "address": "Avinashi Road, Peelamedu",
            "city": "Coimbatore",
            "state": "Tamil Nadu",
            "pincode": "641004", 
            "website": "https://psgtech.edu",
            "latitude": 11.0194,
            "longitude": 76.9319
        },
        {
            "name": "VIT University",
            "address": "Katpadi, Vellore",
            "city": "Vellore",
            "state": "Tamil Nadu",
            "pincode": "632014",
            "website": "https://vit.ac.in",
            "latitude": 12.9692,
            "longitude": 79.1559
        }
    ]
    
    async for db in get_db():
        try:
            for college_data in sample_colleges:
                # Check if college already exists
                from sqlalchemy import select
                result = await db.execute(select(College).filter(College.name == college_data["name"]))
                existing = result.scalar_one_or_none()
                
                if not existing:
                    college = College(**college_data)
                    db.add(college)
                    print(f"✅ Added: {college_data['name']}")
                else:
                    print(f"ℹ️ Already exists: {college_data['name']}")
            
            await db.commit()
            print(f"✅ Successfully added colleges to database!")
            
        except Exception as e:
            print(f"❌ Error adding colleges: {e}")
            await db.rollback()
        finally:
            await db.close()
            break

async def populate_courses():
    """Add sample courses to database"""
    print("\n📚 Adding sample courses...")
    
    sample_courses = [
        {
            "title": "Computer Science Engineering",
            "description": "Comprehensive program covering programming, algorithms, data structures, and software engineering",
            "category": "Engineering",
            "duration": "4 years",
            "level": "Undergraduate",
            "skills_required": ["Programming", "Mathematics", "Problem Solving"],
            "career_opportunities": ["Software Developer", "Data Scientist", "System Architect"]
        },
        {
            "title": "Data Science",
            "description": "Master data analysis, machine learning, statistics, and big data technologies",
            "category": "Technology",
            "duration": "2 years", 
            "level": "Postgraduate",
            "skills_required": ["Python", "Statistics", "Machine Learning"],
            "career_opportunities": ["Data Scientist", "ML Engineer", "Business Analyst"]
        },
        {
            "title": "Artificial Intelligence",
            "description": "Advanced AI concepts including neural networks, deep learning, and cognitive computing",
            "category": "Technology",
            "duration": "2 years",
            "level": "Postgraduate", 
            "skills_required": ["Python", "Mathematics", "Neural Networks"],
            "career_opportunities": ["AI Engineer", "ML Researcher", "Robotics Engineer"]
        },
        {
            "title": "Web Development",
            "description": "Full-stack web development with modern frameworks and technologies",
            "category": "Technology",
            "duration": "6 months",
            "level": "Certificate",
            "skills_required": ["HTML", "CSS", "JavaScript", "React"],
            "career_opportunities": ["Frontend Developer", "Backend Developer", "Full Stack Developer"]
        },
        {
            "title": "Mechanical Engineering",
            "description": "Design, development, and manufacturing of mechanical systems and machines",
            "category": "Engineering",
            "duration": "4 years",
            "level": "Undergraduate",
            "skills_required": ["Mathematics", "Physics", "CAD Design"],
            "career_opportunities": ["Mechanical Engineer", "Design Engineer", "Manufacturing Engineer"]
        }
    ]
    
    async for db in get_db():
        try:
            for course_data in sample_courses:
                # Check if course already exists
                from sqlalchemy import select
                result = await db.execute(select(Course).filter(Course.title == course_data["title"]))
                existing = result.scalar_one_or_none()
                
                if not existing:
                    course = Course(**course_data)
                    db.add(course)
                    print(f"✅ Added: {course_data['title']}")
                else:
                    print(f"ℹ️ Already exists: {course_data['title']}")
            
            await db.commit()
            print(f"✅ Successfully added courses to database!")
            
        except Exception as e:
            print(f"❌ Error adding courses: {e}")
            await db.rollback()
        finally:
            await db.close()
            break

async def populate_careers():
    """Add sample careers to database"""
    print("\n💼 Adding sample careers...")
    
    sample_careers = [
        {
            "title": "Software Developer",
            "description": "Design, develop, and maintain software applications and systems",
            "field": "Technology",
            "average_salary": 800000,
            "growth_rate": 15.5,
            "required_skills": ["Programming", "Problem Solving", "Software Design"],
            "education_requirements": ["Bachelor's in Computer Science", "Programming Bootcamp"]
        },
        {
            "title": "Data Scientist", 
            "description": "Analyze complex data to help companies make better business decisions",
            "field": "Technology",
            "average_salary": 1200000,
            "growth_rate": 22.0,
            "required_skills": ["Python", "Statistics", "Machine Learning", "Data Analysis"],
            "education_requirements": ["Master's in Data Science", "Statistics Background"]
        },
        {
            "title": "Mechanical Engineer",
            "description": "Design and develop mechanical systems, machines, and tools",
            "field": "Engineering", 
            "average_salary": 600000,
            "growth_rate": 8.5,
            "required_skills": ["CAD Design", "Mathematics", "Physics", "Problem Solving"],
            "education_requirements": ["Bachelor's in Mechanical Engineering"]
        },
        {
            "title": "AI Engineer",
            "description": "Develop artificial intelligence systems and machine learning models",
            "field": "Technology",
            "average_salary": 1500000,
            "growth_rate": 25.0,
            "required_skills": ["Python", "Machine Learning", "Neural Networks", "Deep Learning"],
            "education_requirements": ["Master's in AI/ML", "Computer Science Background"]
        },
        {
            "title": "Web Developer",
            "description": "Create and maintain websites and web applications",
            "field": "Technology",
            "average_salary": 500000,
            "growth_rate": 18.0,
            "required_skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
            "education_requirements": ["Web Development Bootcamp", "Computer Science Degree"]
        }
    ]
    
    async for db in get_db():
        try:
            for career_data in sample_careers:
                # Check if career already exists
                from sqlalchemy import select
                result = await db.execute(select(Career).filter(Career.title == career_data["title"]))
                existing = result.scalar_one_or_none()
                
                if not existing:
                    career = Career(**career_data)
                    db.add(career)
                    print(f"✅ Added: {career_data['title']}")
                else:
                    print(f"ℹ️ Already exists: {career_data['title']}")
            
            await db.commit()
            print(f"✅ Successfully added careers to database!")
            
        except Exception as e:
            print(f"❌ Error adding careers: {e}")
            await db.rollback()
        finally:
            await db.close()
            break

async def main():
    """Populate all database tables"""
    print("🗄️ Populating Database with Sample Data")
    print("=" * 50)
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        from app.models import Base
        await conn.run_sync(Base.metadata.create_all)
    
    # Populate data
    await populate_colleges()
    await populate_courses() 
    await populate_careers()
    
    print("\n" + "=" * 50)
    print("🎉 Database population completed!")
    print("=" * 50)
    print("✅ Your database now contains:")
    print("   • Sample colleges (including SNS College)")
    print("   • Sample courses (Engineering, Technology, etc.)")
    print("   • Sample careers (Software Developer, Data Scientist, etc.)")
    print()
    print("🔄 The frontend will now show real database data!")
    print("📊 Recommendations should work with this data!")

if __name__ == "__main__":
    asyncio.run(main())
