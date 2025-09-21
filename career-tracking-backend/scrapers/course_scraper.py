import re
import json
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class CourseScraper(BaseScraper):
    """Scraper for online courses from multiple platforms"""
    
    def __init__(self):
        super().__init__(delay_range=(2, 4))  # Be more respectful to course platforms
        self.courses = []
        self.fallback_courses = self._get_fallback_courses()
    
    def scrape_coursera_search(self, query: str = "programming", max_pages: int = 2) -> List[Dict]:
        """Scrape Coursera search results with fallback to curated data"""
        courses = []
        
        try:
            # Try to scrape real data
            for page in range(1, max_pages + 1):
                url = f"https://www.coursera.org/search?query={query}&page={page}"
                soup = self.get_page(url)
                
                if not soup:
                    continue
                    
                # Updated selectors for current Coursera structure
                course_cards = soup.find_all('div', {'data-testid': 'search-result-card'}) or \
                              soup.find_all('div', class_=re.compile(r'cds-ProductCard|ProductCard'))
                
                for card in course_cards:
                    try:
                        title = self.safe_extract(card, 'h3 a, h2 a, [data-testid="search-result-title"] a')
                        if not title:
                            continue
                            
                        course = {
                            'title': title,
                            'provider': 'Coursera',
                            'description': self.safe_extract(card, '.description, p, [data-testid="search-result-description"]') or f"Learn {query} with this comprehensive course from Coursera",
                            'duration': self.extract_duration(card) or 'Self-paced',
                            'difficulty_level': self.extract_difficulty(card) or 'Beginner',
                            'category': query.title(),
                            'url': self.safe_extract(card, 'h3 a, h2 a', 'href') or '#'
                        }
                        
                        courses.append(course)
                        
                    except Exception as e:
                        logger.warning(f"Error parsing Coursera course: {e}")
                        continue
                        
                if len(courses) >= 10:  # Limit to avoid too many requests
                    break
                    
        except Exception as e:
            logger.error(f"Error scraping Coursera: {e}")
        
        # If we didn't get enough real courses, supplement with curated data
        if len(courses) < 5:
            fallback_courses = [c for c in self.fallback_courses if c['provider'] == 'Coursera' and query.lower() in c['category'].lower()]
            courses.extend(fallback_courses[:10-len(courses)])
        
        logger.info(f"Scraped {len(courses)} courses from Coursera for '{query}'")
        return courses
    
    def scrape_edx_search(self, query: str = "data science", max_pages: int = 2) -> List[Dict]:
        """Scrape edX search results with fallback to curated data"""
        courses = []
        
        try:
            # Try to scrape real data
            for page in range(1, max_pages + 1):
                url = f"https://www.edx.org/search?q={query}&page={page}"
                soup = self.get_page(url)
                
                if not soup:
                    continue
                    
                # Updated selectors for current edX structure
                course_cards = soup.find_all('div', class_=re.compile(r'course-card|discovery-card|pgn__card')) or \
                              soup.find_all('article') or \
                              soup.find_all('div', {'data-testid': 'course-card'})
                
                for card in course_cards:
                    try:
                        title = self.safe_extract(card, 'h3 a, h2 a, .course-title, h3, h2')
                        if not title or len(title) < 5:
                            continue
                            
                        course = {
                            'title': title,
                            'provider': 'edX',
                            'description': self.safe_extract(card, '.course-description, p, .description') or f"Learn {query} with this comprehensive course from edX",
                            'duration': self.extract_duration(card) or 'Self-paced',
                            'difficulty_level': self.extract_difficulty(card) or 'Beginner',
                            'category': query.title(),
                            'url': self.safe_extract(card, 'h3 a, h2 a', 'href') or '#'
                        }
                        
                        courses.append(course)
                        
                    except Exception as e:
                        logger.warning(f"Error parsing edX course: {e}")
                        continue
                        
                if len(courses) >= 8:  # Limit to avoid too many requests
                    break
                    
        except Exception as e:
            logger.error(f"Error scraping edX: {e}")
        
        # If we didn't get enough real courses, supplement with curated data
        if len(courses) < 3:
            fallback_courses = [c for c in self.fallback_courses if c['provider'] == 'edX' and query.lower() in c['category'].lower()]
            courses.extend(fallback_courses[:8-len(courses)])
        
        logger.info(f"Scraped {len(courses)} courses from edX for '{query}'")
        return courses
    
    def scrape_khan_academy(self) -> List[Dict]:
        """Get Khan Academy courses with fallback to curated data"""
        courses = []
        
        try:
            # Khan Academy subjects
            subjects = [
                'math', 'science', 'computing', 'arts-humanities', 
                'economics-finance-domain', 'test-prep'
            ]
            
            for subject in subjects[:3]:  # Limit subjects to avoid too many requests
                try:
                    url = f"https://www.khanacademy.org/{subject}"
                    soup = self.get_page(url)
                    
                    if not soup:
                        continue
                        
                    # Find course/topic links with updated selectors
                    course_links = soup.find_all('a', href=re.compile(r'/' + subject)) or \
                                  soup.find_all('a', class_=re.compile(r'link|course'))
                    
                    for link in course_links[:5]:  # Limit to avoid too many requests
                        try:
                            title = self.clean_text(link.get_text())
                            if len(title) > 10 and len(title) < 100 and title not in [c['title'] for c in courses]:
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
                            
                except Exception as e:
                    logger.warning(f"Error scraping Khan Academy subject {subject}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Khan Academy: {e}")
        
        # Always supplement with curated Khan Academy courses
        fallback_courses = [c for c in self.fallback_courses if c['provider'] == 'Khan Academy']
        courses.extend(fallback_courses[:15-len(courses)])
        
        logger.info(f"Got {len(courses)} courses from Khan Academy")
        return courses
    
    def extract_duration(self, element) -> str:
        """Extract course duration from various text patterns"""
        if not element:
            return 'Self-paced'
            
        text = element.get_text().lower()
        
        # Common duration patterns
        duration_patterns = [
            r'(\d+)\s*weeks?',
            r'(\d+)\s*months?',
            r'(\d+)\s*hours?',
            r'(\d+)-(\d+)\s*weeks?',
            r'(\d+)-(\d+)\s*months?',
            r'self[\s-]?paced',
            r'flexible'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text)
            if match:
                if 'self' in match.group(0) or 'flexible' in match.group(0):
                    return 'Self-paced'
                return match.group(0).title()
        
        return 'Self-paced'
    
    def extract_difficulty(self, element) -> str:
        """Extract difficulty level from text"""
        if not element:
            return 'Beginner'
            
        text = element.get_text().lower()
        
        if 'beginner' in text or 'introductory' in text or 'basic' in text or 'intro' in text:
            return 'Beginner'
        elif 'intermediate' in text or 'medium' in text:
            return 'Intermediate'
        elif 'advanced' in text or 'expert' in text or 'professional' in text:
            return 'Advanced'
        
        return 'Beginner'  # Default
    
    def _get_fallback_courses(self) -> List[Dict]:
        """Get curated course data as fallback"""
        return [
            {
                'title': 'Python for Everybody Specialization',
                'provider': 'Coursera',
                'description': 'Learn to Program and Analyze Data with Python. Develop programs to gather, clean, analyze, and visualize data.',
                'duration': '8 months',
                'difficulty_level': 'Beginner',
                'category': 'Programming',
                'url': 'https://www.coursera.org/specializations/python'
            },
            {
                'title': 'Machine Learning Course',
                'provider': 'Coursera',
                'description': 'Learn about the most effective machine learning techniques, and gain practice implementing them.',
                'duration': '11 weeks',
                'difficulty_level': 'Intermediate',
                'category': 'Machine Learning',
                'url': 'https://www.coursera.org/learn/machine-learning'
            },
            {
                'title': 'CS50: Introduction to Computer Science',
                'provider': 'edX',
                'description': 'An introduction to the intellectual enterprises of computer science and the art of programming.',
                'duration': '12 weeks',
                'difficulty_level': 'Beginner',
                'category': 'Programming',
                'url': 'https://www.edx.org/course/cs50s-introduction-to-computer-science'
            },
            {
                'title': 'Data Science MicroMasters',
                'provider': 'edX',
                'description': 'Master the skills needed to be a data scientist and get hands-on experience with the tools.',
                'duration': '1 year',
                'difficulty_level': 'Advanced',
                'category': 'Data Science',
                'url': 'https://www.edx.org/micromasters/mitx-statistics-and-data-science'
            },
            {
                'title': 'Algebra Basics',
                'provider': 'Khan Academy',
                'description': 'Learn the basics of algebra including variables, expressions, and equations.',
                'duration': 'Self-paced',
                'difficulty_level': 'Beginner',
                'category': 'Math',
                'url': 'https://www.khanacademy.org/math/algebra-basics'
            },
            {
                'title': 'Intro to Programming',
                'provider': 'Khan Academy',
                'description': 'Learn the basics of programming with interactive exercises.',
                'duration': 'Self-paced',
                'difficulty_level': 'Beginner',
                'category': 'Computing',
                'url': 'https://www.khanacademy.org/computing/intro-to-programming'
            },
            {
                'title': 'Web Development Bootcamp',
                'provider': 'Coursera',
                'description': 'Learn HTML, CSS, JavaScript, and modern web development frameworks.',
                'duration': '6 months',
                'difficulty_level': 'Intermediate',
                'category': 'Web Development',
                'url': 'https://www.coursera.org/specializations/web-development'
            },
            {
                'title': 'Digital Marketing Specialization',
                'provider': 'Coursera',
                'description': 'Master digital marketing strategy, analytics, and optimization.',
                'duration': '4 months',
                'difficulty_level': 'Beginner',
                'category': 'Digital Marketing',
                'url': 'https://www.coursera.org/specializations/digital-marketing'
            },
            {
                'title': 'Introduction to Artificial Intelligence',
                'provider': 'edX',
                'description': 'Learn the fundamentals of AI including search, logic, and machine learning.',
                'duration': '16 weeks',
                'difficulty_level': 'Intermediate',
                'category': 'Artificial Intelligence',
                'url': 'https://www.edx.org/course/artificial-intelligence-ai'
            },
            {
                'title': 'Financial Markets',
                'provider': 'Coursera',
                'description': 'Learn about financial institutions, markets, and instruments.',
                'duration': '7 weeks',
                'difficulty_level': 'Beginner',
                'category': 'Finance',
                'url': 'https://www.coursera.org/learn/financial-markets-global'
            }
        ]
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method with improved error handling"""
        all_courses = []
        
        # Define search queries for different categories
        queries = [
            'programming', 'data science', 'machine learning', 'web development',
            'digital marketing', 'business', 'finance'
        ]
        
        try:
            # Try to scrape Coursera
            logger.info("Starting Coursera scraping...")
            for query in queries[:3]:  # Limit to avoid too many requests
                try:
                    courses = self.scrape_coursera_search(query, max_pages=1)
                    all_courses.extend(courses)
                except Exception as e:
                    logger.warning(f"Error scraping Coursera for {query}: {e}")
            
            # Try to scrape edX
            logger.info("Starting edX scraping...")
            for query in queries[3:5]:
                try:
                    courses = self.scrape_edx_search(query, max_pages=1)
                    all_courses.extend(courses)
                except Exception as e:
                    logger.warning(f"Error scraping edX for {query}: {e}")
            
            # Get Khan Academy courses
            logger.info("Getting Khan Academy courses...")
            try:
                khan_courses = self.scrape_khan_academy()
                all_courses.extend(khan_courses)
            except Exception as e:
                logger.warning(f"Error getting Khan Academy courses: {e}")
            
        except Exception as e:
            logger.error(f"Error during course scraping: {e}")
        
        # If we don't have enough courses, use all fallback data
        if len(all_courses) < 20:
            logger.info("Adding more fallback courses to reach minimum count")
            all_courses.extend(self.fallback_courses)
        
        # Remove duplicates based on title
        unique_courses = []
        seen_titles = set()
        
        for course in all_courses:
            if course.get('title') and course['title'] not in seen_titles:
                unique_courses.append(course)
                seen_titles.add(course['title'])
        
        logger.info(f"Total unique courses collected: {len(unique_courses)}")
        return unique_courses[:50]  # Limit to 50 courses
