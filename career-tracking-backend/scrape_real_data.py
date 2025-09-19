#!/usr/bin/env python3
"""
Real Web Scraping Script for J&K Career Guidance
Scrapes real J&K colleges and aptitude questions from internet sources
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.real_jk_college_scraper import RealJKCollegeScraper
from scrapers.real_aptitude_scraper import RealAptitudeScraper
from scrapers.course_scraper import CourseScraper
from scrapers.career_scraper import CareerScraper

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.course import Course
from app.models.career import Career
from app.models.college import College

# Import database URL function
def get_database_url():
    """Get database URL from environment or use default"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Use environment variable or default
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Default PostgreSQL connection with URL encoding for @ symbol
        db_url = "postgresql://postgres:Postgresql%40001@localhost:5432/career_db"
    
    return db_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('real_scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealDataPopulator:
    """Handles database population with real scraped data"""
    
    def __init__(self):
        self.engine = create_engine(get_database_url())
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def populate_colleges(self, colleges_data: List[Dict]) -> int:
        """Populate colleges table with real J&K colleges"""
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
            logger.info(f"Added {added_count} new real colleges to database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error populating colleges: {e}")
            raise
        finally:
            session.close()
            
        return added_count
    
    def populate_courses(self, courses_data: List[Dict]) -> int:
        """Populate courses table with real course data"""
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
        """Populate careers table with career data"""
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

def save_scraped_data(data: Dict[str, List], timestamp: str):
    """Save scraped data to JSON files for backup"""
    os.makedirs('real_scraped_data', exist_ok=True)
    
    for data_type, items in data.items():
        filename = f"real_scraped_data/{data_type}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(items)} {data_type} to {filename}")

def create_ml_aptitude_dataset(questions: List[Dict], timestamp: str):
    """Create specialized ML dataset from real aptitude questions"""
    
    # Group questions by subject for ML training
    subject_groups = {}
    for question in questions:
        subject = question['subject']
        if subject not in subject_groups:
            subject_groups[subject] = []
        subject_groups[subject].append(question)
    
    # Create ML training dataset
    ml_dataset = {
        'metadata': {
            'created_at': timestamp,
            'total_questions': len(questions),
            'subjects': list(subject_groups.keys()),
            'purpose': 'Real Student Interest Analysis for Career Guidance',
            'sources': list(set([q.get('source', 'Unknown') for q in questions]))
        },
        'questions_by_subject': subject_groups,
        'all_questions': questions,
        'statistics': {
            'by_difficulty': {},
            'by_source': {},
            'by_subject': {}
        }
    }
    
    # Calculate statistics
    for question in questions:
        # By difficulty
        difficulty = question.get('difficulty', 'Unknown')
        ml_dataset['statistics']['by_difficulty'][difficulty] = ml_dataset['statistics']['by_difficulty'].get(difficulty, 0) + 1
        
        # By source
        source = question.get('source', 'Unknown')
        ml_dataset['statistics']['by_source'][source] = ml_dataset['statistics']['by_source'].get(source, 0) + 1
        
        # By subject
        subject = question.get('subject', 'Unknown')
        ml_dataset['statistics']['by_subject'][subject] = ml_dataset['statistics']['by_subject'].get(subject, 0) + 1
    
    # Save ML dataset
    ml_filename = f"real_scraped_data/real_ml_aptitude_dataset_{timestamp}.json"
    with open(ml_filename, 'w', encoding='utf-8') as f:
        json.dump(ml_dataset, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Created real ML dataset with {len(questions)} questions from internet sources")
    logger.info(f"Sources: {ml_dataset['metadata']['sources']}")
    logger.info(f"Subject distribution: {ml_dataset['statistics']['by_subject']}")
    
    return ml_dataset

def main():
    """Main scraping function for real data from internet"""
    logger.info("Starting REAL web scraping from internet sources...")
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize real scrapers
    real_jk_college_scraper = RealJKCollegeScraper()
    real_aptitude_scraper = RealAptitudeScraper()
    course_scraper = CourseScraper()
    career_scraper = CareerScraper()
    
    # Initialize database populator
    populator = RealDataPopulator()
    
    scraped_data = {}
    
    try:
        # Scrape REAL J&K Colleges from government websites
        logger.info("Scraping REAL J&K colleges from government and education websites...")
        real_jk_colleges = real_jk_college_scraper.scrape()
        scraped_data['real_jk_colleges'] = real_jk_colleges
        logger.info(f"Scraped {len(real_jk_colleges)} REAL J&K colleges from internet")
        
        # Scrape REAL Aptitude Questions from educational websites
        logger.info("Scraping REAL aptitude questions from educational websites...")
        real_aptitude_questions = real_aptitude_scraper.scrape()
        scraped_data['real_aptitude_questions'] = real_aptitude_questions
        logger.info(f"Scraped {len(real_aptitude_questions)} REAL aptitude questions from internet")
        
        # Scrape some courses (limited for faster execution)
        logger.info("Scraping limited course data...")
        courses = course_scraper.scrape_khan_academy()  # Just Khan Academy for speed
        scraped_data['courses'] = courses
        logger.info(f"Scraped {len(courses)} courses")
        
        # Create career data
        logger.info("Creating career data...")
        careers = career_scraper.scrape_indeed_careers()  # Use generated career data
        scraped_data['careers'] = careers
        logger.info(f"Created {len(careers)} careers")
        
        # Save scraped data to JSON files
        save_scraped_data(scraped_data, timestamp)
        
        # Create specialized ML dataset for real aptitude questions
        ml_dataset = create_ml_aptitude_dataset(real_aptitude_questions, timestamp)
        
        # Populate database
        logger.info("Populating database with REAL scraped data...")
        
        colleges_added = populator.populate_colleges(real_jk_colleges)
        courses_added = populator.populate_courses(courses)
        careers_added = populator.populate_careers(careers)
        
        # Summary
        logger.info("=" * 70)
        logger.info("REAL WEB SCRAPING FROM INTERNET COMPLETE")
        logger.info("=" * 70)
        logger.info(f"REAL J&K Colleges scraped from internet: {colleges_added}")
        logger.info(f"REAL Aptitude questions scraped from internet: {len(real_aptitude_questions)}")
        logger.info(f"Courses added: {courses_added}")
        logger.info(f"Careers added: {careers_added}")
        logger.info(f"Total database entries: {colleges_added + courses_added + careers_added}")
        logger.info(f"ML dataset created with {len(real_aptitude_questions)} REAL questions")
        logger.info(f"Data backed up with timestamp: {timestamp}")
        
        # Print real colleges summary
        logger.info("\nREAL J&K COLLEGES BY SOURCE:")
        college_sources = {}
        for college in real_jk_colleges:
            source = college.get('scraped_from', 'Unknown')
            college_sources[source] = college_sources.get(source, 0) + 1
        
        for source, count in college_sources.items():
            logger.info(f"  {source}: {count} colleges")
        
        # Print real aptitude questions summary
        logger.info("\nREAL APTITUDE QUESTIONS BY SOURCE:")
        for source, count in ml_dataset['statistics']['by_source'].items():
            logger.info(f"  {source}: {count} questions")
        
        logger.info("\nREAL APTITUDE QUESTIONS BY SUBJECT:")
        for subject, count in ml_dataset['statistics']['by_subject'].items():
            logger.info(f"  {subject}: {count} questions")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during real web scraping process: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ REAL web scraping from internet completed successfully!")
        print("🌐 Data scraped from actual government and educational websites")
        print("📁 Check the 'real_scraped_data' folder for JSON backups.")
        print("📊 Real ML aptitude dataset created from internet sources.")
        print("🏫 Real J&K colleges populated in database from government portals.")
        print("📝 Check 'real_scraping.log' for detailed logs.")
        print("\n🎯 Your ML model now has REAL data from the internet!")
    else:
        print("\n❌ Real web scraping failed!")
        print("📝 Check 'real_scraping.log' for error details.")
        sys.exit(1)
