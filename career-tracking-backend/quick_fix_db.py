#!/usr/bin/env python3
"""
Quick Database Fix Script
Populates database with essential data to fix server errors
"""

import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models.college import College
from app.models.course import Course
from app.models.career import Career

# Database URL
DATABASE_URL = "postgresql+asyncpg://postgres:Postgresql%40001@localhost:5432/career_db"

async def populate_basic_data():
    """Populate database with basic data"""
    
    # Create async engine
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine)
    
    async with async_session() as session:
        try:
            # Add basic colleges
            colleges_data = [
                {
                    'name': 'University of Kashmir',
                    'address': 'Hazratbal, Srinagar, Jammu and Kashmir',
                    'city': 'Srinagar',
                    'state': 'Jammu and Kashmir',
                    'pincode': '190006',
                    'website': 'https://www.kashmiruniversity.net',
                    'latitude': 34.1269,
                    'longitude': 74.8370,
                    'scholarship_details': 'Merit scholarships available'
                },
                {
                    'name': 'University of Jammu',
                    'address': 'Baba Saheb Ambedkar Road, Jammu',
                    'city': 'Jammu',
                    'state': 'Jammu and Kashmir',
                    'pincode': '180006',
                    'website': 'https://www.jammuuniversity.ac.in',
                    'latitude': 32.7266,
                    'longitude': 74.8570,
                    'scholarship_details': 'Government scholarships available'
                },
                {
                    'name': 'NIT Srinagar',
                    'address': 'Hazratbal, Srinagar, Jammu and Kashmir',
                    'city': 'Srinagar',
                    'state': 'Jammu and Kashmir',
                    'pincode': '190006',
                    'website': 'https://www.nitsri.ac.in',
                    'latitude': 34.1269,
                    'longitude': 74.8370,
                    'scholarship_details': 'Technical education scholarships'
                }
            ]
            
            for college_data in colleges_data:
                college = College(**college_data)
                session.add(college)
            
            # Add basic courses
            courses_data = [
                {
                    'title': 'Computer Science Engineering',
                    'description': 'Comprehensive program in computer science and engineering',
                    'duration': '4 years',
                    'provider': 'University',
                    'category': 'Engineering',
                    'difficulty_level': 'Intermediate'
                },
                {
                    'title': 'Data Science',
                    'description': 'Master data analysis and machine learning',
                    'duration': '2 years',
                    'provider': 'University',
                    'category': 'Technology',
                    'difficulty_level': 'Advanced'
                },
                {
                    'title': 'Web Development',
                    'description': 'Full-stack web development course',
                    'duration': '6 months',
                    'provider': 'Online',
                    'category': 'Programming',
                    'difficulty_level': 'Beginner'
                }
            ]
            
            for course_data in courses_data:
                course = Course(**course_data)
                session.add(course)
            
            # Add basic careers
            careers_data = [
                {
                    'title': 'Software Developer',
                    'description': 'Develop software applications and systems',
                    'field': 'Technology',
                    'median_salary': '₹8,00,000 - ₹15,00,000',
                    'job_outlook': 'Excellent',
                    'required_skills': 'Programming, Problem Solving, Software Design'
                },
                {
                    'title': 'Data Scientist',
                    'description': 'Analyze data to extract business insights',
                    'field': 'Data Science',
                    'median_salary': '₹10,00,000 - ₹20,00,000',
                    'job_outlook': 'Very Good',
                    'required_skills': 'Python, Statistics, Machine Learning, SQL'
                },
                {
                    'title': 'Web Developer',
                    'description': 'Create and maintain websites and web applications',
                    'field': 'Technology',
                    'median_salary': '₹5,00,000 - ₹12,00,000',
                    'job_outlook': 'Good',
                    'required_skills': 'HTML, CSS, JavaScript, React, Node.js'
                }
            ]
            
            for career_data in careers_data:
                career = Career(**career_data)
                session.add(career)
            
            await session.commit()
            print("✅ Database populated successfully!")
            print(f"Added {len(colleges_data)} colleges")
            print(f"Added {len(courses_data)} courses") 
            print(f"Added {len(careers_data)} careers")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error populating database: {e}")
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(populate_basic_data())
