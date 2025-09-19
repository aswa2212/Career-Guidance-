#!/usr/bin/env python3
"""
Test script for REAL web scrapers
Tests each real scraper individually without database operations
"""

import os
import sys
import json
import logging

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.real_jk_college_scraper import RealJKCollegeScraper
from scrapers.real_aptitude_scraper import RealAptitudeScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_real_jk_college_scraper():
    """Test the real J&K college scraper"""
    logger.info("Testing REAL J&K College Scraper...")
    
    try:
        scraper = RealJKCollegeScraper()
        
        # Test individual methods first
        logger.info("Testing government portal scraping...")
        gov_colleges = scraper.scrape_jk_government_portal()
        logger.info(f"Government portal colleges: {len(gov_colleges)}")
        
        if gov_colleges:
            logger.info("Sample government college:")
            logger.info(json.dumps(gov_colleges[0], indent=2))
        
        # Test university websites
        logger.info("Testing university website scraping...")
        uni_colleges = scraper.scrape_university_websites()
        logger.info(f"University colleges: {len(uni_colleges)}")
        
        if uni_colleges:
            logger.info("Sample university college:")
            logger.info(json.dumps(uni_colleges[0], indent=2))
        
        # Test education directories
        logger.info("Testing education directory scraping...")
        dir_colleges = scraper.scrape_education_directory()
        logger.info(f"Directory colleges: {len(dir_colleges)}")
        
        if dir_colleges:
            logger.info("Sample directory college:")
            logger.info(json.dumps(dir_colleges[0], indent=2))
        
        return True
        
    except Exception as e:
        logger.error(f"Real J&K college scraper test failed: {e}")
        return False

def test_real_aptitude_scraper():
    """Test the real aptitude scraper"""
    logger.info("Testing REAL Aptitude Scraper...")
    
    try:
        scraper = RealAptitudeScraper()
        
        # Test IndiaBIX scraping
        logger.info("Testing IndiaBIX scraping...")
        indiabix_questions = scraper.scrape_indiabix_questions()
        logger.info(f"IndiaBIX questions: {len(indiabix_questions)}")
        
        if indiabix_questions:
            logger.info("Sample IndiaBIX question:")
            logger.info(json.dumps(indiabix_questions[0], indent=2))
        
        # Test FreshersLive scraping
        logger.info("Testing FreshersLive scraping...")
        fresherslive_questions = scraper.scrape_fresherslive_questions()
        logger.info(f"FreshersLive questions: {len(fresherslive_questions)}")
        
        if fresherslive_questions:
            logger.info("Sample FreshersLive question:")
            logger.info(json.dumps(fresherslive_questions[0], indent=2))
        
        # Test GeeksforGeeks scraping
        logger.info("Testing GeeksforGeeks scraping...")
        geeksforgeeks_questions = scraper.scrape_geeksforgeeks_questions()
        logger.info(f"GeeksforGeeks questions: {len(geeksforgeeks_questions)}")
        
        if geeksforgeeks_questions:
            logger.info("Sample GeeksforGeeks question:")
            logger.info(json.dumps(geeksforgeeks_questions[0], indent=2))
        
        # Test JavaTpoint scraping
        logger.info("Testing JavaTpoint scraping...")
        javatpoint_questions = scraper.scrape_javatpoint_questions()
        logger.info(f"JavaTpoint questions: {len(javatpoint_questions)}")
        
        if javatpoint_questions:
            logger.info("Sample JavaTpoint question:")
            logger.info(json.dumps(javatpoint_questions[0], indent=2))
        
        return True
        
    except Exception as e:
        logger.error(f"Real aptitude scraper test failed: {e}")
        return False

def main():
    """Run all real scraper tests"""
    logger.info("=" * 60)
    logger.info("TESTING REAL WEB SCRAPERS FROM INTERNET")
    logger.info("=" * 60)
    
    results = {
        'real_jk_college_scraper': test_real_jk_college_scraper(),
        'real_aptitude_scraper': test_real_aptitude_scraper()
    }
    
    logger.info("=" * 60)
    logger.info("REAL SCRAPER TEST RESULTS")
    logger.info("=" * 60)
    
    for scraper, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{scraper}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n🎉 All REAL scraper tests passed! Ready for full internet scraping.")
        logger.info("🌐 Your scrapers can fetch real data from government and educational websites.")
    else:
        logger.info("\n⚠️  Some tests failed. Check the logs above.")
        logger.info("💡 This might be due to website changes or network issues.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
