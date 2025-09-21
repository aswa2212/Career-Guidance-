#!/usr/bin/env python3
"""
Test script for improved scrapers
Tests the enhanced course, college, and aptitude scrapers
"""

import sys
import os
import asyncio
import logging
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.course_scraper import CourseScraper
from scrapers.college_scraper import CollegeScraper
from scrapers.aptitude_scraper import AptitudeScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_course_scraper():
    """Test the improved course scraper"""
    logger.info("=" * 50)
    logger.info("TESTING COURSE SCRAPER")
    logger.info("=" * 50)
    
    try:
        scraper = CourseScraper()
        courses = scraper.scrape()
        
        logger.info(f"✅ Course scraper returned {len(courses)} courses")
        
        if courses:
            # Display sample courses
            logger.info("Sample courses:")
            for i, course in enumerate(courses[:3]):
                logger.info(f"  {i+1}. {course.get('title', 'No title')} - {course.get('provider', 'No provider')}")
                logger.info(f"     Category: {course.get('category', 'No category')}")
                logger.info(f"     Duration: {course.get('duration', 'No duration')}")
                logger.info(f"     Difficulty: {course.get('difficulty_level', 'No difficulty')}")
                logger.info("")
        
        return True, len(courses)
        
    except Exception as e:
        logger.error(f"❌ Course scraper failed: {e}")
        return False, 0

def test_college_scraper():
    """Test the college scraper"""
    logger.info("=" * 50)
    logger.info("TESTING COLLEGE SCRAPER")
    logger.info("=" * 50)
    
    try:
        scraper = CollegeScraper()
        colleges = scraper.scrape()
        
        logger.info(f"✅ College scraper returned {len(colleges)} colleges")
        
        if colleges:
            # Display sample colleges
            logger.info("Sample colleges:")
            for i, college in enumerate(colleges[:3]):
                logger.info(f"  {i+1}. {college.get('name', 'No name')}")
                logger.info(f"     Address: {college.get('address', 'No address')}")
                logger.info(f"     Website: {college.get('website', 'No website')}")
                logger.info(f"     Scholarships: {college.get('scholarship_details', 'No scholarship info')[:100]}...")
                logger.info("")
        
        return True, len(colleges)
        
    except Exception as e:
        logger.error(f"❌ College scraper failed: {e}")
        return False, 0

def test_aptitude_scraper():
    """Test the improved aptitude scraper"""
    logger.info("=" * 50)
    logger.info("TESTING APTITUDE SCRAPER")
    logger.info("=" * 50)
    
    try:
        scraper = AptitudeScraper()
        questions = scraper.scrape()
        
        logger.info(f"✅ Aptitude scraper returned {len(questions)} questions")
        
        if questions:
            # Count by subject
            subject_counts = {}
            for question in questions:
                subject = question.get('subject', 'Unknown')
                subject_counts[subject] = subject_counts.get(subject, 0) + 1
            
            logger.info("Questions by subject:")
            for subject, count in subject_counts.items():
                logger.info(f"  {subject}: {count} questions")
            
            # Display sample questions
            logger.info("\nSample questions:")
            for i, question in enumerate(questions[:3]):
                logger.info(f"  {i+1}. {question.get('question', 'No question')}")
                logger.info(f"     Subject: {question.get('subject', 'No subject')}")
                logger.info(f"     Difficulty: {question.get('difficulty', 'No difficulty')}")
                logger.info(f"     Options: {question.get('options', [])}")
                logger.info(f"     Answer: {question.get('correct_answer', 'No answer')}")
                logger.info("")
        
        return True, len(questions)
        
    except Exception as e:
        logger.error(f"❌ Aptitude scraper failed: {e}")
        return False, 0

def test_scraper_performance():
    """Test scraper performance and reliability"""
    logger.info("=" * 50)
    logger.info("TESTING SCRAPER PERFORMANCE")
    logger.info("=" * 50)
    
    results = {
        'course_scraper': {'success': False, 'count': 0, 'time': 0},
        'college_scraper': {'success': False, 'count': 0, 'time': 0},
        'aptitude_scraper': {'success': False, 'count': 0, 'time': 0}
    }
    
    # Test course scraper
    start_time = datetime.now()
    success, count = test_course_scraper()
    end_time = datetime.now()
    results['course_scraper'] = {
        'success': success,
        'count': count,
        'time': (end_time - start_time).total_seconds()
    }
    
    # Test college scraper
    start_time = datetime.now()
    success, count = test_college_scraper()
    end_time = datetime.now()
    results['college_scraper'] = {
        'success': success,
        'count': count,
        'time': (end_time - start_time).total_seconds()
    }
    
    # Test aptitude scraper
    start_time = datetime.now()
    success, count = test_aptitude_scraper()
    end_time = datetime.now()
    results['aptitude_scraper'] = {
        'success': success,
        'count': count,
        'time': (end_time - start_time).total_seconds()
    }
    
    return results

def main():
    """Main test function"""
    logger.info("🚀 Starting scraper tests...")
    logger.info(f"Test started at: {datetime.now()}")
    
    try:
        results = test_scraper_performance()
        
        # Print summary
        logger.info("=" * 50)
        logger.info("TEST SUMMARY")
        logger.info("=" * 50)
        
        total_success = 0
        total_items = 0
        
        for scraper_name, result in results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            logger.info(f"{scraper_name}: {status}")
            logger.info(f"  Items scraped: {result['count']}")
            logger.info(f"  Time taken: {result['time']:.2f} seconds")
            logger.info("")
            
            if result['success']:
                total_success += 1
            total_items += result['count']
        
        logger.info(f"Overall Results:")
        logger.info(f"  Scrapers passed: {total_success}/3")
        logger.info(f"  Total items scraped: {total_items}")
        
        if total_success == 3:
            logger.info("🎉 All scrapers are working correctly!")
            return True
        else:
            logger.warning("⚠️  Some scrapers need attention")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Scraper tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Scraper tests failed!")
        sys.exit(1)
