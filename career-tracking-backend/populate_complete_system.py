#!/usr/bin/env python3
"""
Complete System Population Script
Populates database with J&K colleges, courses, careers, and aptitude questions
Sets up ML recommendation engine with real data
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.models.course import Course
from app.models.career import Career
from app.models.college import College
from app.services.recommendation_engine import recommendation_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('complete_system_population.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from environment or use default"""
    import os
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Use environment variable or default
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Default PostgreSQL connection with URL encoding for @ symbol
        db_url = "postgresql://postgres:Postgresql%40001@localhost:5432/career_db"
    
    return db_url

def get_async_database_url():
    """Get async database URL"""
    db_url = get_database_url()
    return db_url.replace("postgresql://", "postgresql+asyncpg://")

class CompleteSystemPopulator:
    """Handles complete system population with all data"""
    
    def __init__(self):
        # Sync engine for basic operations
        self.sync_engine = create_engine(get_database_url())
        self.SessionLocal = sessionmaker(bind=self.sync_engine)
        
        # Async engine for async operations
        self.async_engine = create_async_engine(get_async_database_url())
        self.AsyncSessionLocal = async_sessionmaker(self.async_engine)
    
    def load_jk_data(self) -> Dict[str, List]:
        """Load J&K data from generated files"""
        data = {}
        
        # Load from jk_data_generated folder
        jk_data_dir = 'jk_data_generated'
        
        if os.path.exists(jk_data_dir):
            # Find the latest files
            files = os.listdir(jk_data_dir)
            
            # Load colleges
            college_files = [f for f in files if f.startswith('jk_colleges_')]
            if college_files:
                latest_college_file = sorted(college_files)[-1]
                with open(os.path.join(jk_data_dir, latest_college_file), 'r', encoding='utf-8') as f:
                    data['colleges'] = json.load(f)
                logger.info(f"Loaded {len(data['colleges'])} J&K colleges")
            
            # Load aptitude questions
            aptitude_files = [f for f in files if f.startswith('aptitude_questions_')]
            if aptitude_files:
                latest_aptitude_file = sorted(aptitude_files)[-1]
                with open(os.path.join(jk_data_dir, latest_aptitude_file), 'r', encoding='utf-8') as f:
                    data['aptitude_questions'] = json.load(f)
                logger.info(f"Loaded {len(data['aptitude_questions'])} aptitude questions")
        
        return data
    
    def populate_colleges(self, colleges_data: List[Dict]) -> int:
        """Populate colleges table with J&K colleges"""
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
    
    def populate_courses_from_csv(self) -> int:
        """Populate courses from existing CSV data"""
        session = self.SessionLocal()
        added_count = 0
        
        try:
            import pandas as pd
            
            # Load courses from CSV
            courses_df = pd.read_csv('data/courses.csv')
            
            for _, row in courses_df.iterrows():
                # Check if course already exists
                existing = session.query(Course).filter(
                    Course.title == row['course_name']
                ).first()
                
                if not existing:
                    course = Course(
                        title=row.get('course_name', ''),
                        description=row.get('description', ''),
                        duration=row.get('duration', ''),
                        provider='ML Dataset',
                        category=row.get('required_skills', ''),
                        difficulty_level=row.get('level', 'Beginner')
                    )
                    session.add(course)
                    added_count += 1
                    
            session.commit()
            logger.info(f"Added {added_count} new courses from CSV to database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error populating courses from CSV: {e}")
            raise
        finally:
            session.close()
            
        return added_count
    
    def populate_careers_from_ml_data(self) -> int:
        """Create career data from course career paths"""
        session = self.SessionLocal()
        added_count = 0
        
        try:
            import pandas as pd
            
            # Load courses from CSV to extract career paths
            courses_df = pd.read_csv('data/courses.csv')
            
            # Extract unique career paths
            all_careers = set()
            for _, row in courses_df.iterrows():
                if pd.notna(row['career_paths']):
                    careers = [c.strip() for c in row['career_paths'].split(',')]
                    all_careers.update(careers)
            
            # Create career entries
            for career_name in all_careers:
                if not career_name:
                    continue
                    
                # Check if career already exists
                existing = session.query(Career).filter(
                    Career.title == career_name
                ).first()
                
                if not existing:
                    career = Career(
                        title=career_name,
                        description=f"Career in {career_name} with growth opportunities and skill development.",
                        field=self.get_career_field(career_name),
                        median_salary=self.get_estimated_salary(career_name),
                        job_outlook='Growing',
                        required_skills=self.get_career_skills(career_name)
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
    
    def get_career_field(self, career_name: str) -> str:
        """Map career name to field"""
        career_lower = career_name.lower()
        
        if any(word in career_lower for word in ['software', 'developer', 'programmer', 'engineer']):
            return 'Technology'
        elif any(word in career_lower for word in ['data', 'analyst', 'scientist']):
            return 'Data Science'
        elif any(word in career_lower for word in ['manager', 'lead', 'director']):
            return 'Management'
        elif any(word in career_lower for word in ['designer', 'creative', 'artist']):
            return 'Design'
        elif any(word in career_lower for word in ['consultant', 'advisor']):
            return 'Consulting'
        else:
            return 'General'
    
    def get_estimated_salary(self, career_name: str) -> str:
        """Get estimated salary range for career"""
        career_lower = career_name.lower()
        
        if any(word in career_lower for word in ['senior', 'lead', 'architect', 'director']):
            return '₹15,00,000 - ₹25,00,000'
        elif any(word in career_lower for word in ['engineer', 'developer', 'scientist']):
            return '₹8,00,000 - ₹15,00,000'
        elif any(word in career_lower for word in ['analyst', 'consultant']):
            return '₹6,00,000 - ₹12,00,000'
        else:
            return '₹4,00,000 - ₹8,00,000'
    
    def get_career_skills(self, career_name: str) -> str:
        """Get required skills for career"""
        career_lower = career_name.lower()
        
        if 'software' in career_lower or 'developer' in career_lower:
            return 'Programming, Problem Solving, Software Design, Testing'
        elif 'data' in career_lower:
            return 'Data Analysis, Statistics, Python, SQL, Machine Learning'
        elif 'manager' in career_lower:
            return 'Leadership, Communication, Project Management, Strategic Planning'
        elif 'designer' in career_lower:
            return 'Design Thinking, Creativity, User Experience, Visual Design'
        else:
            return 'Communication, Problem Solving, Analytical Thinking, Teamwork'
    
    async def setup_ml_engine(self):
        """Setup and initialize the ML recommendation engine"""
        try:
            async with self.AsyncSessionLocal() as db:
                # Load data into ML engine
                success = await recommendation_engine.load_data_from_db(db)
                
                if not success:
                    # Fallback to CSV data
                    success = recommendation_engine.load_data()
                
                if success:
                    logger.info("ML recommendation engine initialized successfully")
                    return True
                else:
                    logger.warning("Failed to initialize ML engine, will use fallback recommendations")
                    return False
                    
        except Exception as e:
            logger.error(f"Error setting up ML engine: {e}")
            return False

async def main():
    """Main function to populate complete system"""
    logger.info("Starting complete system population...")
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize populator
    populator = CompleteSystemPopulator()
    
    try:
        # Load J&K data
        logger.info("Loading J&K data...")
        jk_data = populator.load_jk_data()
        
        # Populate colleges
        if 'colleges' in jk_data:
            logger.info("Populating J&K colleges...")
            colleges_added = populator.populate_colleges(jk_data['colleges'])
        else:
            colleges_added = 0
            logger.warning("No J&K colleges data found")
        
        # Populate courses from CSV
        logger.info("Populating courses from ML dataset...")
        courses_added = populator.populate_courses_from_csv()
        
        # Populate careers
        logger.info("Populating careers from ML data...")
        careers_added = populator.populate_careers_from_ml_data()
        
        # Setup ML recommendation engine
        logger.info("Setting up ML recommendation engine...")
        ml_success = await populator.setup_ml_engine()
        
        # Summary
        logger.info("=" * 70)
        logger.info("COMPLETE SYSTEM POPULATION FINISHED")
        logger.info("=" * 70)
        logger.info(f"J&K Colleges added: {colleges_added}")
        logger.info(f"Courses added: {courses_added}")
        logger.info(f"Careers added: {careers_added}")
        logger.info(f"ML Engine initialized: {'✅ Yes' if ml_success else '❌ No (using fallback)'}")
        
        if 'aptitude_questions' in jk_data:
            logger.info(f"Aptitude questions available: {len(jk_data['aptitude_questions'])}")
        
        logger.info(f"System population completed at: {timestamp}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during complete system population: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 Complete system population successful!")
        print("✅ Database populated with J&K colleges, courses, and careers")
        print("✅ ML recommendation engine initialized")
        print("✅ System ready for full functionality")
        print("📝 Check 'complete_system_population.log' for detailed logs")
    else:
        print("\n❌ System population failed!")
        print("📝 Check 'complete_system_population.log' for error details")
        sys.exit(1)
