#!/usr/bin/env python3
"""
Simple script to populate real data using scrapers with proper error handling
"""

import asyncio
import sys
import os
import logging

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def populate_with_scrapers():
    """Populate database with real scraped data"""
    try:
        # Import after path setup
        from scrapers.course_scraper import CourseScraper
        from scrapers.career_scraper import CareerScraper
        from scrapers.college_scraper import CollegeScraper
        
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from app.models.course import Course
        from app.models.career import Career
        from app.models.college import College
        
        # Database URL
        DATABASE_URL = "postgresql+asyncpg://postgres:Postgresql%400001@localhost/career_db"
        
        # Create async engine
        engine = create_async_engine(DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            # Check existing data
            from sqlalchemy import select
            
            # Check courses
            result = await session.execute(select(Course))
            existing_courses = result.scalars().all()
            logger.info(f"Found {len(existing_courses)} existing courses")
            
            if len(existing_courses) < 10:  # If we have less than 10 courses, scrape more
                logger.info("Scraping courses...")
                try:
                    course_scraper = CourseScraper()
                    courses_data = course_scraper.scrape()
                    
                    for course_data in courses_data[:20]:  # Limit to 20 courses
                        # Check if course already exists
                        existing = await session.execute(
                            select(Course).filter(Course.title == course_data['title'])
                        )
                        if not existing.scalars().first():
                            course = Course(
                                title=course_data.get('title', 'Unknown Course'),
                                description=course_data.get('description', ''),
                                duration=course_data.get('duration', 'Not specified'),
                                provider=course_data.get('provider', 'Unknown'),
                                category=course_data.get('category', 'General'),
                                difficulty_level=course_data.get('difficulty', 'Intermediate')
                            )
                            session.add(course)
                    
                    logger.info(f"Added new courses from scraper")
                except Exception as e:
                    logger.error(f"Error scraping courses: {e}")
            
            # Check colleges
            result = await session.execute(select(College))
            existing_colleges = result.scalars().all()
            logger.info(f"Found {len(existing_colleges)} existing colleges")
            
            if len(existing_colleges) < 5:  # If we have less than 5 colleges, scrape more
                logger.info("Scraping colleges...")
                try:
                    college_scraper = CollegeScraper()
                    colleges_data = college_scraper.scrape()
                    
                    for college_data in colleges_data[:15]:  # Limit to 15 colleges
                        # Check if college already exists
                        existing = await session.execute(
                            select(College).filter(College.name == college_data['name'])
                        )
                        if not existing.scalars().first():
                            college = College(
                                name=college_data.get('name', 'Unknown College'),
                                address=college_data.get('address', ''),
                                city=college_data.get('city', ''),
                                state=college_data.get('state', ''),
                                pincode=college_data.get('pincode', ''),
                                website=college_data.get('website', ''),
                                latitude=college_data.get('latitude'),
                                longitude=college_data.get('longitude'),
                                scholarship_details=college_data.get('scholarship_details', '')
                            )
                            session.add(college)
                    
                    logger.info(f"Added new colleges from scraper")
                except Exception as e:
                    logger.error(f"Error scraping colleges: {e}")
            
            # Check careers
            result = await session.execute(select(Career))
            existing_careers = result.scalars().all()
            logger.info(f"Found {len(existing_careers)} existing careers")
            
            if len(existing_careers) < 5:  # If we have less than 5 careers, scrape more
                logger.info("Scraping careers...")
                try:
                    career_scraper = CareerScraper()
                    careers_data = career_scraper.scrape()
                    
                    for career_data in careers_data[:15]:  # Limit to 15 careers
                        # Check if career already exists
                        existing = await session.execute(
                            select(Career).filter(Career.title == career_data['title'])
                        )
                        if not existing.scalars().first():
                            career = Career(
                                title=career_data.get('title', 'Unknown Career'),
                                description=career_data.get('description', ''),
                                field=career_data.get('field', 'General'),
                                median_salary=career_data.get('salary', 'Not specified'),
                                job_outlook=career_data.get('job_outlook', 'Stable'),
                                required_skills=career_data.get('required_skills', '')
                            )
                            session.add(career)
                    
                    logger.info(f"Added new careers from scraper")
                except Exception as e:
                    logger.error(f"Error scraping careers: {e}")
            
            # Commit all changes
            await session.commit()
            logger.info("✅ Database population completed successfully!")
            
            # Final count
            result = await session.execute(select(Course))
            total_courses = len(result.scalars().all())
            result = await session.execute(select(College))
            total_colleges = len(result.scalars().all())
            result = await session.execute(select(Career))
            total_careers = len(result.scalars().all())
            
            logger.info(f"📊 Final counts - Courses: {total_courses}, Colleges: {total_colleges}, Careers: {total_careers}")
            
    except Exception as e:
        logger.error(f"❌ Error in population process: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(populate_with_scrapers())
