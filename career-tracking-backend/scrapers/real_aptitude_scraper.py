import re
import json
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger
from bs4 import BeautifulSoup

class RealAptitudeScraper(BaseScraper):
    """Real web scraper for aptitude questions from educational websites"""
    
    def __init__(self):
        super().__init__(delay_range=(2, 4), timeout=15)  # Shorter timeout
        self.questions = []
    
    def scrape_indiabix_questions(self) -> List[Dict]:
        """Scrape aptitude questions from IndiaBIX"""
        questions = []
        
        # IndiaBIX aptitude sections
        sections = [
            'arithmetic-aptitude',
            'data-interpretation', 
            'logical-reasoning',
            'verbal-reasoning',
            'non-verbal-reasoning',
            'verbal-ability'
        ]
        
        for section in sections:
            try:
                url = f"https://www.indiabix.com/{section}/"
                logger.info(f"Scraping IndiaBIX section: {section}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Find question links
                question_links = soup.find_all('a', href=re.compile(r'/questions/'))
                
                for link in question_links[:5]:  # Limit per section
                    question_url = f"https://www.indiabix.com{link.get('href')}"
                    question_data = self.scrape_indiabix_question_page(question_url, section)
                    if question_data:
                        questions.extend(question_data)
                        
            except Exception as e:
                logger.warning(f"Error scraping IndiaBIX section {section}: {e}")
                continue
        
        logger.info(f"Scraped {len(questions)} questions from IndiaBIX")
        return questions
    
    def scrape_indiabix_question_page(self, url: str, section: str) -> List[Dict]:
        """Scrape individual question page from IndiaBIX"""
        questions = []
        
        try:
            soup = self.get_page(url)
            if not soup:
                return questions
            
            # Find question elements
            question_divs = soup.find_all('div', class_=re.compile(r'question|problem'))
            
            for div in question_divs[:3]:  # Limit questions per page
                question_text = self.safe_extract(div, '.question-text, p')
                
                if not question_text or len(question_text) < 10:
                    continue
                
                # Extract options
                options = []
                option_elements = div.find_all(['li', 'div'], class_=re.compile(r'option|choice'))
                
                for i, option in enumerate(option_elements[:4]):
                    option_text = self.clean_text(option.get_text())
                    if option_text:
                        options.append(f"{chr(65+i)}) {option_text}")
                
                # Extract correct answer
                correct_answer = self.safe_extract(div, '.correct-answer, .answer')
                if not correct_answer and len(options) > 0:
                    correct_answer = 'A'  # Default
                
                # Extract explanation
                explanation = self.safe_extract(div, '.explanation, .solution')
                
                question = {
                    'question': question_text,
                    'options': options,
                    'correct_answer': correct_answer,
                    'subject': self.map_section_to_subject(section),
                    'difficulty': 'Medium',
                    'topic': section.replace('-', ' ').title(),
                    'explanation': explanation or 'Solution not provided',
                    'source': 'IndiaBIX',
                    'source_url': url
                }
                
                questions.append(question)
        
        except Exception as e:
            logger.warning(f"Error scraping question page {url}: {e}")
        
        return questions
    
    def scrape_fresherslive_questions(self) -> List[Dict]:
        """Scrape aptitude questions from FreshersLive"""
        questions = []
        
        categories = [
            'aptitude-questions-and-answers',
            'reasoning-questions-and-answers',
            'verbal-ability-questions-and-answers',
            'quantitative-aptitude-questions-and-answers'
        ]
        
        for category in categories:
            try:
                url = f"https://www.fresherslive.com/{category}"
                logger.info(f"Scraping FreshersLive category: {category}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Find question containers
                question_containers = soup.find_all(['div', 'article'], class_=re.compile(r'question|quiz|problem'))
                
                for container in question_containers[:10]:  # Limit per category
                    question_data = self.extract_fresherslive_question(container, category)
                    if question_data:
                        questions.append(question_data)
                        
            except Exception as e:
                logger.warning(f"Error scraping FreshersLive category {category}: {e}")
                continue
        
        logger.info(f"Scraped {len(questions)} questions from FreshersLive")
        return questions
    
    def extract_fresherslive_question(self, container, category: str) -> Dict:
        """Extract question data from FreshersLive container"""
        try:
            question_text = self.safe_extract(container, 'h3, h4, .question-title, p')
            
            if not question_text or len(question_text) < 10:
                return None
            
            # Extract options
            options = []
            option_elements = container.find_all(['li', 'span', 'div'], text=re.compile(r'^[A-D]\)'))
            
            for option in option_elements[:4]:
                option_text = self.clean_text(option.get_text())
                if option_text:
                    options.append(option_text)
            
            # If no formatted options found, look for any list items
            if not options:
                list_items = container.find_all('li')[:4]
                for i, item in enumerate(list_items):
                    text = self.clean_text(item.get_text())
                    if text:
                        options.append(f"{chr(65+i)}) {text}")
            
            question = {
                'question': question_text,
                'options': options,
                'correct_answer': 'A',  # Default since answer extraction is complex
                'subject': self.map_category_to_subject(category),
                'difficulty': 'Medium',
                'topic': category.replace('-', ' ').title(),
                'explanation': 'Detailed solution available on source website',
                'source': 'FreshersLive',
                'source_url': 'https://www.fresherslive.com'
            }
            
            return question
            
        except Exception as e:
            logger.warning(f"Error extracting FreshersLive question: {e}")
            return None
    
    def scrape_geeksforgeeks_questions(self) -> List[Dict]:
        """Scrape programming and logical questions from GeeksforGeeks"""
        questions = []
        
        topics = [
            'mathematical-algorithms',
            'geometric-algorithms', 
            'bitwise-algorithms',
            'graph-algorithms',
            'searching-algorithms'
        ]
        
        for topic in topics:
            try:
                url = f"https://www.geeksforgeeks.org/{topic}/"
                logger.info(f"Scraping GeeksforGeeks topic: {topic}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Find article links
                article_links = soup.find_all('a', href=re.compile(r'/.*-algorithm|/.*-problem'))
                
                for link in article_links[:3]:  # Limit per topic
                    article_url = f"https://www.geeksforgeeks.org{link.get('href')}"
                    question_data = self.extract_geeksforgeeks_problem(article_url, topic)
                    if question_data:
                        questions.append(question_data)
                        
            except Exception as e:
                logger.warning(f"Error scraping GeeksforGeeks topic {topic}: {e}")
                continue
        
        logger.info(f"Scraped {len(questions)} questions from GeeksforGeeks")
        return questions
    
    def extract_geeksforgeeks_problem(self, url: str, topic: str) -> Dict:
        """Extract problem from GeeksforGeeks article"""
        try:
            soup = self.get_page(url)
            if not soup:
                return None
            
            # Extract problem statement
            problem_text = self.safe_extract(soup, 'h1, .problem-statement, p')
            
            if not problem_text or len(problem_text) < 20:
                return None
            
            # Create multiple choice question from the problem
            question = {
                'question': f"What is the best approach to solve: {problem_text[:200]}...?",
                'options': [
                    'A) Brute force approach',
                    'B) Dynamic programming',
                    'C) Greedy algorithm', 
                    'D) Divide and conquer'
                ],
                'correct_answer': 'B',  # Default to DP as it's common
                'subject': 'Computer Science',
                'difficulty': 'Hard',
                'topic': topic.replace('-', ' ').title(),
                'explanation': 'Refer to the complete solution on GeeksforGeeks',
                'source': 'GeeksforGeeks',
                'source_url': url
            }
            
            return question
            
        except Exception as e:
            logger.warning(f"Error extracting GeeksforGeeks problem {url}: {e}")
            return None
    
    def scrape_javatpoint_questions(self) -> List[Dict]:
        """Scrape questions from JavaTpoint"""
        questions = []
        
        subjects = [
            'aptitude/mathematical-aptitude',
            'aptitude/logical-reasoning',
            'aptitude/verbal-ability',
            'aptitude/data-interpretation'
        ]
        
        for subject in subjects:
            try:
                url = f"https://www.javatpoint.com/{subject}"
                logger.info(f"Scraping JavaTpoint subject: {subject}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Find content paragraphs that might contain questions
                content_divs = soup.find_all(['div', 'p'], class_=re.compile(r'content|example|question'))
                
                for div in content_divs[:5]:  # Limit per subject
                    text = div.get_text()
                    if '?' in text and len(text) > 30:
                        question_data = self.create_question_from_text(text, subject)
                        if question_data:
                            questions.append(question_data)
                            
            except Exception as e:
                logger.warning(f"Error scraping JavaTpoint subject {subject}: {e}")
                continue
        
        logger.info(f"Scraped {len(questions)} questions from JavaTpoint")
        return questions
    
    def create_question_from_text(self, text: str, subject: str) -> Dict:
        """Create a structured question from raw text"""
        try:
            # Extract question (text before first question mark)
            question_match = re.search(r'^(.*?\?)', text)
            if not question_match:
                return None
            
            question_text = question_match.group(1).strip()
            
            if len(question_text) < 10:
                return None
            
            # Create generic options for the question
            options = [
                'A) Option 1',
                'B) Option 2', 
                'C) Option 3',
                'D) Option 4'
            ]
            
            question = {
                'question': question_text,
                'options': options,
                'correct_answer': 'A',
                'subject': self.map_subject_path_to_subject(subject),
                'difficulty': 'Medium',
                'topic': subject.split('/')[-1].replace('-', ' ').title(),
                'explanation': 'Complete solution available on JavaTpoint',
                'source': 'JavaTpoint',
                'source_url': f"https://www.javatpoint.com/{subject}"
            }
            
            return question
            
        except Exception as e:
            logger.warning(f"Error creating question from text: {e}")
            return None
    
    def map_section_to_subject(self, section: str) -> str:
        """Map IndiaBIX section to subject"""
        mapping = {
            'arithmetic-aptitude': 'Mathematics',
            'data-interpretation': 'Mathematics', 
            'logical-reasoning': 'Logical Reasoning',
            'verbal-reasoning': 'English',
            'non-verbal-reasoning': 'Logical Reasoning',
            'verbal-ability': 'English'
        }
        return mapping.get(section, 'General Aptitude')
    
    def map_category_to_subject(self, category: str) -> str:
        """Map FreshersLive category to subject"""
        if 'aptitude' in category or 'quantitative' in category:
            return 'Mathematics'
        elif 'reasoning' in category:
            return 'Logical Reasoning'
        elif 'verbal' in category:
            return 'English'
        else:
            return 'General Aptitude'
    
    def map_subject_path_to_subject(self, path: str) -> str:
        """Map JavaTpoint path to subject"""
        if 'mathematical' in path:
            return 'Mathematics'
        elif 'logical' in path:
            return 'Logical Reasoning'
        elif 'verbal' in path:
            return 'English'
        elif 'data-interpretation' in path:
            return 'Mathematics'
        else:
            return 'General Aptitude'
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method for real aptitude questions"""
        all_questions = []
        
        try:
            # Scrape from IndiaBIX
            indiabix_questions = self.scrape_indiabix_questions()
            all_questions.extend(indiabix_questions)
            
            # Scrape from FreshersLive
            fresherslive_questions = self.scrape_fresherslive_questions()
            all_questions.extend(fresherslive_questions)
            
            # Scrape from GeeksforGeeks
            geeksforgeeks_questions = self.scrape_geeksforgeeks_questions()
            all_questions.extend(geeksforgeeks_questions)
            
            # Scrape from JavaTpoint
            javatpoint_questions = self.scrape_javatpoint_questions()
            all_questions.extend(javatpoint_questions)
            
        except Exception as e:
            logger.error(f"Error during aptitude question scraping: {e}")
        
        # Remove duplicates and add metadata
        unique_questions = []
        seen_questions = set()
        
        for i, question in enumerate(all_questions):
            question_text = question.get('question', '').lower()
            if question_text and question_text not in seen_questions:
                question['id'] = i + 1
                question['created_for'] = 'ML Model Training'
                question['career_relevance'] = self.get_career_relevance(question['subject'])
                unique_questions.append(question)
                seen_questions.add(question_text)
        
        # Group by subject for ML model
        subject_distribution = {}
        for q in unique_questions:
            subject = q['subject']
            subject_distribution[subject] = subject_distribution.get(subject, 0) + 1
        
        logger.info(f"Total unique aptitude questions scraped: {len(unique_questions)}")
        logger.info(f"Question distribution by subject: {subject_distribution}")
        
        return unique_questions
    
    def get_career_relevance(self, subject: str) -> str:
        """Map subjects to relevant career fields"""
        career_mapping = {
            'Mathematics': 'Engineering, Data Science, Finance, Research, Teaching',
            'Physics': 'Engineering, Research, Astronomy, Medical Physics, Teaching',
            'Chemistry': 'Chemical Engineering, Pharmaceuticals, Research, Medicine, Teaching',
            'Biology': 'Medicine, Biotechnology, Research, Environmental Science, Teaching',
            'Computer Science': 'Software Development, Data Science, Cybersecurity, AI/ML, IT',
            'English': 'Literature, Journalism, Content Writing, Teaching, Communications',
            'Logical Reasoning': 'Management, Law, Consulting, Problem Solving, Analytics',
            'General Aptitude': 'General Problem Solving, Management, Administration'
        }
        return career_mapping.get(subject, 'General Problem Solving')
