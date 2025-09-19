#!/usr/bin/env python3
"""
Simple Data Populator for J&K Career Guidance
Creates J&K colleges and aptitude questions without web scraping
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.course import Course
from app.models.career import Career
from app.models.college import College

# Import database URL function
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_data_population.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleDataPopulator:
    """Handles database population with J&K focused data"""
    
    def __init__(self):
        self.engine = create_engine(get_database_url())
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def create_jk_colleges_data(self) -> List[Dict]:
        """Create J&K colleges data"""
        colleges = [
            {
                'name': 'University of Kashmir',
                'address': 'Hazratbal, Srinagar, Jammu and Kashmir, India',
                'city': 'Srinagar',
                'state': 'Jammu and Kashmir',
                'pincode': '190006',
                'website': 'https://www.kashmiruniversity.net',
                'latitude': 34.1269,
                'longitude': 74.8370,
                'scholarship_details': 'UGC scholarships, Merit scholarships, SC/ST/OBC scholarships, State government scholarships available.'
            },
            {
                'name': 'University of Jammu',
                'address': 'Baba Saheb Ambedkar Road, Jammu, Jammu and Kashmir, India',
                'city': 'Jammu',
                'state': 'Jammu and Kashmir',
                'pincode': '180006',
                'website': 'https://www.jammuuniversity.ac.in',
                'latitude': 32.7266,
                'longitude': 74.8570,
                'scholarship_details': 'UGC scholarships, Merit scholarships, SC/ST/OBC scholarships, State government scholarships available.'
            },
            {
                'name': 'Central University of Kashmir',
                'address': 'Nunar, Ganderbal, Jammu and Kashmir, India',
                'city': 'Ganderbal',
                'state': 'Jammu and Kashmir',
                'pincode': '191201',
                'website': 'https://www.cukashmir.ac.in',
                'latitude': 34.2307,
                'longitude': 74.7847,
                'scholarship_details': 'Central government scholarships, UGC scholarships, Merit scholarships, Research fellowships available.'
            },
            {
                'name': 'Central University of Jammu',
                'address': 'Bagla, Rahya-Suchani, Samba, Jammu and Kashmir, India',
                'city': 'Samba',
                'state': 'Jammu and Kashmir',
                'pincode': '181143',
                'website': 'https://www.cujammu.ac.in',
                'latitude': 32.5625,
                'longitude': 75.1194,
                'scholarship_details': 'Central government scholarships, UGC scholarships, Merit scholarships, Research fellowships available.'
            },
            {
                'name': 'National Institute of Technology Srinagar',
                'address': 'Hazratbal, Srinagar, Jammu and Kashmir, India',
                'city': 'Srinagar',
                'state': 'Jammu and Kashmir',
                'pincode': '190006',
                'website': 'https://www.nitsri.ac.in',
                'latitude': 34.1269,
                'longitude': 74.8370,
                'scholarship_details': 'Technical education scholarships, Merit scholarships, Industry scholarships, JEE-based scholarships available.'
            },
            {
                'name': 'Government Medical College Srinagar',
                'address': 'Karan Nagar, Srinagar, Jammu and Kashmir, India',
                'city': 'Srinagar',
                'state': 'Jammu and Kashmir',
                'pincode': '190010',
                'website': 'https://www.gmcsrinagar.edu.in',
                'latitude': 34.0837,
                'longitude': 74.7973,
                'scholarship_details': 'Medical education scholarships, NEET-based scholarships, Government medical scholarships available.'
            },
            {
                'name': 'Government Medical College Jammu',
                'address': 'Sector 5, Bhagwati Nagar, Jammu, Jammu and Kashmir, India',
                'city': 'Jammu',
                'state': 'Jammu and Kashmir',
                'pincode': '180016',
                'website': 'https://www.gmcjammu.nic.in',
                'latitude': 32.7266,
                'longitude': 74.8570,
                'scholarship_details': 'Medical education scholarships, NEET-based scholarships, Government medical scholarships available.'
            },
            {
                'name': 'Government Degree College Srinagar',
                'address': 'M.A. Road, Srinagar, Jammu and Kashmir, India',
                'city': 'Srinagar',
                'state': 'Jammu and Kashmir',
                'pincode': '190001',
                'website': 'https://www.gdcsrinagar.edu.in',
                'latitude': 34.0837,
                'longitude': 74.7973,
                'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.'
            },
            {
                'name': 'Government Degree College Jammu',
                'address': 'Canal Road, Jammu, Jammu and Kashmir, India',
                'city': 'Jammu',
                'state': 'Jammu and Kashmir',
                'pincode': '180001',
                'website': 'https://www.gdcjammu.edu.in',
                'latitude': 32.7266,
                'longitude': 74.8570,
                'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.'
            },
            {
                'name': 'Government College for Women Srinagar',
                'address': 'M.A. Road, Srinagar, Jammu and Kashmir, India',
                'city': 'Srinagar',
                'state': 'Jammu and Kashmir',
                'pincode': '190001',
                'website': 'https://www.gcwsrinagar.edu.in',
                'latitude': 34.0837,
                'longitude': 74.7973,
                'scholarship_details': 'Women empowerment scholarships, Merit scholarships, State government scholarships available.'
            }
        ]
        
        return colleges
    
    def create_aptitude_questions_data(self) -> List[Dict]:
        """Create aptitude questions for ML model"""
        questions = [
            {
                'id': 1,
                'question': 'If 2x + 3 = 11, what is the value of x?',
                'options': ['A) 3', 'B) 4', 'C) 5', 'D) 6'],
                'correct_answer': 'B',
                'subject': 'Mathematics',
                'difficulty': 'Easy',
                'topic': 'Algebra',
                'explanation': 'Solving: 2x + 3 = 11, 2x = 8, x = 4',
                'source': 'Educational Database',
                'career_relevance': 'Engineering, Data Science, Finance, Research, Teaching'
            },
            {
                'id': 2,
                'question': 'What is the area of a circle with radius 7 cm?',
                'options': ['A) 154 cm²', 'B) 144 cm²', 'C) 164 cm²', 'D) 174 cm²'],
                'correct_answer': 'A',
                'subject': 'Mathematics',
                'difficulty': 'Medium',
                'topic': 'Geometry',
                'explanation': 'Area = πr² = (22/7) × 7² = 154 cm²',
                'source': 'Educational Database',
                'career_relevance': 'Engineering, Data Science, Finance, Research, Teaching'
            },
            {
                'id': 3,
                'question': 'What is the SI unit of force?',
                'options': ['A) Joule', 'B) Newton', 'C) Watt', 'D) Pascal'],
                'correct_answer': 'B',
                'subject': 'Physics',
                'difficulty': 'Easy',
                'topic': 'Mechanics',
                'explanation': 'Newton (N) is the SI unit of force',
                'source': 'Educational Database',
                'career_relevance': 'Engineering, Research, Astronomy, Medical Physics, Teaching'
            },
            {
                'id': 4,
                'question': 'What is the chemical symbol for Gold?',
                'options': ['A) Go', 'B) Au', 'C) Ag', 'D) Gd'],
                'correct_answer': 'B',
                'subject': 'Chemistry',
                'difficulty': 'Easy',
                'topic': 'Periodic Table',
                'explanation': 'Au is the chemical symbol for Gold (from Latin: Aurum)',
                'source': 'Educational Database',
                'career_relevance': 'Chemical Engineering, Pharmaceuticals, Research, Medicine, Teaching'
            },
            {
                'id': 5,
                'question': 'What is the powerhouse of the cell?',
                'options': ['A) Nucleus', 'B) Mitochondria', 'C) Ribosome', 'D) Chloroplast'],
                'correct_answer': 'B',
                'subject': 'Biology',
                'difficulty': 'Easy',
                'topic': 'Cell Biology',
                'explanation': 'Mitochondria are called the powerhouse of the cell as they produce ATP',
                'source': 'Educational Database',
                'career_relevance': 'Medicine, Biotechnology, Research, Environmental Science, Teaching'
            },
            {
                'id': 6,
                'question': 'What does CPU stand for?',
                'options': ['A) Central Processing Unit', 'B) Computer Personal Unit', 'C) Central Program Unit', 'D) Computer Processing Unit'],
                'correct_answer': 'A',
                'subject': 'Computer Science',
                'difficulty': 'Easy',
                'topic': 'Computer Hardware',
                'explanation': 'CPU stands for Central Processing Unit',
                'source': 'Educational Database',
                'career_relevance': 'Software Development, Data Science, Cybersecurity, AI/ML, IT'
            },
            {
                'id': 7,
                'question': 'What is the synonym of "Happy"?',
                'options': ['A) Sad', 'B) Joyful', 'C) Angry', 'D) Tired'],
                'correct_answer': 'B',
                'subject': 'English',
                'difficulty': 'Easy',
                'topic': 'Vocabulary',
                'explanation': 'Joyful is a synonym of Happy',
                'source': 'Educational Database',
                'career_relevance': 'Literature, Journalism, Content Writing, Teaching, Communications'
            },
            {
                'id': 8,
                'question': 'What comes next in the series: 2, 4, 8, 16, ?',
                'options': ['A) 24', 'B) 32', 'C) 20', 'D) 18'],
                'correct_answer': 'B',
                'subject': 'Logical Reasoning',
                'difficulty': 'Easy',
                'topic': 'Number Series',
                'explanation': 'Each number is doubled: 2×2=4, 4×2=8, 8×2=16, 16×2=32',
                'source': 'Educational Database',
                'career_relevance': 'Management, Law, Consulting, Problem Solving, Analytics'
            }
        ]
        
        return questions
        
    def populate_colleges(self, colleges_data: List[Dict]) -> int:
        """Populate colleges table"""
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

def save_data_to_json(data: Dict[str, List], timestamp: str):
    """Save data to JSON files for backup"""
    os.makedirs('simple_data_backup', exist_ok=True)
    
    for data_type, items in data.items():
        filename = f"simple_data_backup/{data_type}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(items)} {data_type} to {filename}")

def main():
    """Main function to populate database with J&K data"""
    logger.info("Starting simple J&K data population...")
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize populator
    populator = SimpleDataPopulator()
    
    try:
        # Create J&K colleges data
        logger.info("Creating J&K colleges data...")
        jk_colleges = populator.create_jk_colleges_data()
        
        # Create aptitude questions data
        logger.info("Creating aptitude questions data...")
        aptitude_questions = populator.create_aptitude_questions_data()
        
        # Save data to JSON
        data_to_save = {
            'jk_colleges': jk_colleges,
            'aptitude_questions': aptitude_questions
        }
        save_data_to_json(data_to_save, timestamp)
        
        # Populate database
        logger.info("Populating database...")
        colleges_added = populator.populate_colleges(jk_colleges)
        
        # Summary
        logger.info("=" * 60)
        logger.info("SIMPLE J&K DATA POPULATION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"J&K Colleges added: {colleges_added}")
        logger.info(f"Aptitude questions created: {len(aptitude_questions)}")
        logger.info(f"Data backed up with timestamp: {timestamp}")
        
        # Print colleges by city
        logger.info("\nJ&K COLLEGES BY CITY:")
        city_count = {}
        for college in jk_colleges:
            city = college['city']
            city_count[city] = city_count.get(city, 0) + 1
        
        for city, count in city_count.items():
            logger.info(f"  {city}: {count} colleges")
        
        # Print questions by subject
        logger.info("\nAPTITUDE QUESTIONS BY SUBJECT:")
        subject_count = {}
        for question in aptitude_questions:
            subject = question['subject']
            subject_count[subject] = subject_count.get(subject, 0) + 1
        
        for subject, count in subject_count.items():
            logger.info(f"  {subject}: {count} questions")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during data population: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ J&K data population completed successfully!")
        print("📁 Check the 'simple_data_backup' folder for JSON backups.")
        print("🏫 J&K colleges populated in database.")
        print("🧠 Aptitude questions created for ML model.")
        print("📝 Check 'simple_data_population.log' for detailed logs.")
    else:
        print("\n❌ Data population failed!")
        print("📝 Check 'simple_data_population.log' for error details.")
        sys.exit(1)
