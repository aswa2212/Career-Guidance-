#!/usr/bin/env python3
"""
Web Scraping and Database Population Script
Scrapes real data from the internet and populates PostgreSQL database
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.course_scraper import CourseScraper
from scrapers.career_scraper import CareerScraper
from scrapers.college_scraper import CollegeScraper

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.course import Course
from app.models.career import Career
from app.models.college import College
from app.database import get_database_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataPopulator:
    """Handles database population with scraped data"""
    
    def __init__(self):
        self.engine = create_engine(get_database_url())
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def populate_courses(self, courses_data: List[Dict]) -> int:
        """Populate courses table with scraped data"""
        session = self.SessionLocal()
        added_count = 0
        
        try:
            for course_data in courses_data:
                # Check if course already exists
                existing = session.query(Course).filter(
                    Course.title == course_data['title']
                ).first()
                
                if not existing:
                    course = Course(
                        title=course_data.get('title', ''),
                        description=course_data.get('description', ''),
                        duration=course_data.get('duration', ''),
                        provider=course_data.get('provider', ''),
                        category=course_data.get('category', ''),
                        difficulty_level=course_data.get('difficulty_level', 'Beginner')
                    )
                    session.add(course)
                    added_count += 1
                    
            session.commit()
            logger.info(f"Added {added_count} new courses to database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error populating courses: {e}")
            raise
        finally:
            session.close()
            
        return added_count
    
    def populate_careers(self, careers_data: List[Dict]) -> int:
        """Populate careers table with scraped data"""
        session = self.SessionLocal()
        added_count = 0
        
        try:
            for career_data in careers_data:
                # Check if career already exists
                existing = session.query(Career).filter(
                    Career.title == career_data['title']
                ).first()
                
                if not existing:
                    career = Career(
                        title=career_data.get('title', ''),
                        description=career_data.get('description', ''),
                        field=career_data.get('field', ''),
                        median_salary=career_data.get('median_salary', ''),
                        job_outlook=career_data.get('job_outlook', ''),
                        required_skills=career_data.get('required_skills', '')
                    )
                    session.add(career)
                    added_count += 1
                    
            session.commit()
            logger.info(f"Added {added_count} new careers to database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error populating careers: {e}")
            raise
        finally:
            session.close()
            
        return added_count
    
    def populate_colleges(self, colleges_data: List[Dict]) -> int:
        """Populate colleges table with scraped data"""
        session = self.SessionLocal()
        added_count = 0
        
        try:
            for college_data in colleges_data:
                # Check if college already exists
                existing = session.query(College).filter(
                    College.name == college_data['name']
                ).first()
                
                if not existing:
                    college = College(
                        name=college_data.get('name', ''),
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
                    added_count += 1
                    
            session.commit()
            logger.info(f"Added {added_count} new colleges to database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error populating colleges: {e}")
            raise
        finally:
            session.close()
            
        return added_count

def save_scraped_data(data: Dict[str, List], timestamp: str):
    """Save scraped data to JSON files for backup"""
    os.makedirs('scraped_data', exist_ok=True)
    
    for data_type, items in data.items():
        filename = f"scraped_data/{data_type}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(items)} {data_type} to {filename}")

def main():
    """Main scraping and population function"""
    logger.info("Starting web scraping and database population process...")
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize scrapers
    course_scraper = CourseScraper()
    career_scraper = CareerScraper()
    college_scraper = CollegeScraper()
    
    # Initialize database populator
    populator = DataPopulator()
    
    scraped_data = {}
    
    try:
        # Scrape courses
        logger.info("Scraping courses...")
        courses = course_scraper.scrape()
        scraped_data['courses'] = courses
        logger.info(f"Scraped {len(courses)} courses")
        
        # Scrape careers
        logger.info("Scraping careers...")
        careers = career_scraper.scrape()
        scraped_data['careers'] = careers
        logger.info(f"Scraped {len(careers)} careers")
        
        # Scrape colleges
        logger.info("Scraping colleges...")
        colleges = college_scraper.scrape()
        scraped_data['colleges'] = colleges
        logger.info(f"Scraped {len(colleges)} colleges")
        
        # Save scraped data to JSON files
        save_scraped_data(scraped_data, timestamp)
        
        # Populate database
        logger.info("Populating database...")
        
        courses_added = populator.populate_courses(courses)
        careers_added = populator.populate_careers(careers)
        colleges_added = populator.populate_colleges(colleges)
        
        # Summary
        logger.info("=" * 50)
        logger.info("SCRAPING AND POPULATION COMPLETE")
        logger.info("=" * 50)
        logger.info(f"Courses added: {courses_added}")
        logger.info(f"Careers added: {careers_added}")
        logger.info(f"Colleges added: {colleges_added}")
        logger.info(f"Total items added: {courses_added + careers_added + colleges_added}")
        logger.info(f"Data backed up with timestamp: {timestamp}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during scraping/population process: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Scraping and database population completed successfully!")
        print("Check the 'scraped_data' folder for JSON backups.")
        print("Check 'scraping.log' for detailed logs.")
    else:
        print("\n❌ Scraping and database population failed!")
        print("Check 'scraping.log' for error details.")
        sys.exit(1)
