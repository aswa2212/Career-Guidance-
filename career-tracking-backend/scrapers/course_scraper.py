import re
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class CourseScraper(BaseScraper):
    """Scraper for online courses from multiple platforms"""
    
    def __init__(self):
        super().__init__(delay_range=(2, 4))  # Be more respectful to course platforms
        self.courses = []
    
    def scrape_coursera_search(self, query: str = "programming", max_pages: int = 3) -> List[Dict]:
        """Scrape Coursera search results"""
        courses = []
        
        for page in range(1, max_pages + 1):
            url = f"https://www.coursera.org/search?query={query}&page={page}"
            soup = self.get_page(url)
            
            if not soup:
                continue
                
            # Find course cards
            course_cards = soup.find_all('div', class_=re.compile(r'ProductCard'))
            
            for card in course_cards:
                try:
                    course = {
                        'title': self.safe_extract(card, 'h3 a, h2 a'),
                        'provider': 'Coursera',
                        'description': self.safe_extract(card, '.description, p'),
                        'duration': self.extract_duration(card),
                        'difficulty_level': self.extract_difficulty(card),
                        'category': query.title(),
                        'url': self.safe_extract(card, 'h3 a, h2 a', 'href')
                    }
                    
                    if course['title']:
                        courses.append(course)
                        
                except Exception as e:
                    logger.warning(f"Error parsing Coursera course: {e}")
                    continue
        
        logger.info(f"Scraped {len(courses)} courses from Coursera for '{query}'")
        return courses
    
    def scrape_edx_search(self, query: str = "data science", max_pages: int = 2) -> List[Dict]:
        """Scrape edX search results"""
        courses = []
        
        for page in range(1, max_pages + 1):
            url = f"https://www.edx.org/search?q={query}&page={page}"
            soup = self.get_page(url)
            
            if not soup:
                continue
                
            # Find course cards
            course_cards = soup.find_all('div', class_=re.compile(r'course-card|discovery-card'))
            
            for card in course_cards:
                try:
                    course = {
                        'title': self.safe_extract(card, 'h3 a, h2 a, .course-title'),
                        'provider': 'edX',
                        'description': self.safe_extract(card, '.course-description, p'),
                        'duration': self.extract_duration(card),
                        'difficulty_level': self.extract_difficulty(card),
                        'category': query.title(),
                        'url': self.safe_extract(card, 'h3 a, h2 a', 'href')
                    }
                    
                    if course['title']:
                        courses.append(course)
                        
                except Exception as e:
                    logger.warning(f"Error parsing edX course: {e}")
                    continue
        
        logger.info(f"Scraped {len(courses)} courses from edX for '{query}'")
        return courses
    
    def scrape_khan_academy(self) -> List[Dict]:
        """Scrape Khan Academy courses"""
        courses = []
        
        # Khan Academy subjects
        subjects = [
            'math', 'science', 'computing', 'arts-humanities', 
            'economics-finance-domain', 'test-prep'
        ]
        
        for subject in subjects:
            url = f"https://www.khanacademy.org/{subject}"
            soup = self.get_page(url)
            
            if not soup:
                continue
                
            # Find course/topic links
            course_links = soup.find_all('a', href=re.compile(r'/' + subject))
            
            for link in course_links[:10]:  # Limit to avoid too many requests
                try:
                    title = self.clean_text(link.get_text())
                    if len(title) > 10 and title not in [c['title'] for c in courses]:
                        course = {
                            'title': title,
                            'provider': 'Khan Academy',
                            'description': f"Free {subject.replace('-', ' ')} course from Khan Academy",
                            'duration': 'Self-paced',
                            'difficulty_level': 'Beginner',
                            'category': subject.replace('-', ' ').title(),
                            'url': f"https://www.khanacademy.org{link.get('href', '')}"
                        }
                        courses.append(course)
                        
                except Exception as e:
                    logger.warning(f"Error parsing Khan Academy course: {e}")
                    continue
        
        logger.info(f"Scraped {len(courses)} courses from Khan Academy")
        return courses
    
    def extract_duration(self, element) -> str:
        """Extract course duration from various text patterns"""
        text = element.get_text().lower()
        
        # Common duration patterns
        duration_patterns = [
            r'(\d+)\s*weeks?',
            r'(\d+)\s*months?',
            r'(\d+)\s*hours?',
            r'(\d+)-(\d+)\s*weeks?',
            r'(\d+)-(\d+)\s*months?'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return 'Variable'
    
    def extract_difficulty(self, element) -> str:
        """Extract difficulty level from text"""
        text = element.get_text().lower()
        
        if 'beginner' in text or 'introductory' in text:
            return 'Beginner'
        elif 'intermediate' in text:
            return 'Intermediate'
        elif 'advanced' in text or 'expert' in text:
            return 'Advanced'
        
        return 'Beginner'  # Default
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method"""
        all_courses = []
        
        # Define search queries for different categories
        queries = [
            'programming', 'data science', 'machine learning', 'web development',
            'mobile development', 'cybersecurity', 'digital marketing', 'business',
            'design', 'photography', 'finance', 'healthcare', 'engineering'
        ]
        
        try:
            # Scrape Coursera
            for query in queries[:5]:  # Limit to avoid too many requests
                courses = self.scrape_coursera_search(query, max_pages=2)
                all_courses.extend(courses)
            
            # Scrape edX
            for query in queries[5:8]:
                courses = self.scrape_edx_search(query, max_pages=2)
                all_courses.extend(courses)
            
            # Scrape Khan Academy
            khan_courses = self.scrape_khan_academy()
            all_courses.extend(khan_courses)
            
        except Exception as e:
            logger.error(f"Error during course scraping: {e}")
        
        # Remove duplicates based on title
        unique_courses = []
        seen_titles = set()
        
        for course in all_courses:
            if course['title'] not in seen_titles:
                unique_courses.append(course)
                seen_titles.add(course['title'])
        
        logger.info(f"Total unique courses scraped: {len(unique_courses)}")
        return unique_courses
