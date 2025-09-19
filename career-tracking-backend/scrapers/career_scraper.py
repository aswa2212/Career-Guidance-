import re
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class CareerScraper(BaseScraper):
    """Scraper for career information from various sources"""
    
    def __init__(self):
        super().__init__(delay_range=(2, 4))
        self.careers = []
    
    def scrape_bls_careers(self) -> List[Dict]:
        """Scrape career data from Bureau of Labor Statistics"""
        careers = []
        
        # BLS Occupational Outlook Handbook categories
        categories = [
            'architecture-and-engineering',
            'arts-design-entertainment-sports-and-media',
            'business-and-financial',
            'computer-and-information-technology',
            'education-training-and-library',
            'healthcare',
            'legal',
            'management',
            'sales'
        ]
        
        for category in categories:
            url = f"https://www.bls.gov/ooh/{category}/home.htm"
            soup = self.get_page(url)
            
            if not soup:
                continue
                
            # Find career links
            career_links = soup.find_all('a', href=re.compile(r'/ooh/' + category + r'/[^/]+\.htm$'))
            
            for link in career_links[:15]:  # Limit per category
                career_url = f"https://www.bls.gov{link.get('href')}"
                career_data = self.scrape_bls_career_detail(career_url, category)
                
                if career_data:
                    careers.append(career_data)
        
        logger.info(f"Scraped {len(careers)} careers from BLS")
        return careers
    
    def scrape_bls_career_detail(self, url: str, field: str) -> Dict:
        """Scrape detailed career information from BLS career page"""
        soup = self.get_page(url)
        
        if not soup:
            return None
            
        try:
            title = self.safe_extract(soup, 'h1')
            
            # Extract salary information
            salary_section = soup.find('div', id='salary') or soup.find('section', id='salary')
            median_salary = "Not specified"
            
            if salary_section:
                salary_text = salary_section.get_text()
                salary_match = re.search(r'\$[\d,]+', salary_text)
                if salary_match:
                    median_salary = salary_match.group(0)
            
            # Extract job outlook
            outlook_section = soup.find('div', id='job-outlook') or soup.find('section', id='job-outlook')
            job_outlook = "Average"
            
            if outlook_section:
                outlook_text = outlook_section.get_text().lower()
                if 'faster than average' in outlook_text or 'much faster' in outlook_text:
                    job_outlook = "Growing"
                elif 'slower than average' in outlook_text or 'decline' in outlook_text:
                    job_outlook = "Declining"
                elif 'as fast as average' in outlook_text:
                    job_outlook = "Stable"
            
            # Extract description
            description = self.safe_extract(soup, '.ooh-tab-content p, .summary p')
            
            # Extract required skills (from education/training section)
            skills_section = soup.find('div', id='education') or soup.find('section', id='education')
            required_skills = []
            
            if skills_section:
                skills_text = skills_section.get_text()
                # Common skill keywords
                skill_keywords = [
                    'bachelor', 'master', 'degree', 'certification', 'license',
                    'communication', 'analytical', 'problem-solving', 'technical',
                    'leadership', 'teamwork', 'computer', 'software'
                ]
                
                for keyword in skill_keywords:
                    if keyword in skills_text.lower():
                        required_skills.append(keyword.title())
            
            career = {
                'title': title,
                'description': description,
                'field': field.replace('-', ' ').title(),
                'median_salary': median_salary,
                'job_outlook': job_outlook,
                'required_skills': ', '.join(required_skills[:5])  # Limit to 5 skills
            }
            
            return career
            
        except Exception as e:
            logger.warning(f"Error parsing BLS career detail {url}: {e}")
            return None
    
    def scrape_indeed_careers(self) -> List[Dict]:
        """Scrape popular career titles from Indeed"""
        careers = []
        
        # Popular job search terms
        job_titles = [
            'software engineer', 'data scientist', 'product manager', 'marketing manager',
            'sales representative', 'nurse', 'teacher', 'accountant', 'graphic designer',
            'project manager', 'business analyst', 'web developer', 'cybersecurity analyst',
            'financial advisor', 'human resources', 'operations manager', 'content writer',
            'social media manager', 'customer service', 'mechanical engineer'
        ]
        
        for title in job_titles:
            try:
                # Create career entry based on common knowledge
                career = {
                    'title': title.title(),
                    'description': f"Professional role in {title} with various responsibilities and growth opportunities.",
                    'field': self.categorize_job_title(title),
                    'median_salary': self.estimate_salary_range(title),
                    'job_outlook': "Average",
                    'required_skills': self.get_common_skills(title)
                }
                careers.append(career)
                
            except Exception as e:
                logger.warning(f"Error creating career entry for {title}: {e}")
                continue
        
        logger.info(f"Created {len(careers)} career entries from common job titles")
        return careers
    
    def categorize_job_title(self, title: str) -> str:
        """Categorize job title into field"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['engineer', 'developer', 'programmer', 'software', 'tech']):
            return 'Technology'
        elif any(word in title_lower for word in ['manager', 'business', 'analyst', 'consultant']):
            return 'Business'
        elif any(word in title_lower for word in ['marketing', 'sales', 'social media', 'content']):
            return 'Marketing'
        elif any(word in title_lower for word in ['nurse', 'doctor', 'healthcare', 'medical']):
            return 'Healthcare'
        elif any(word in title_lower for word in ['teacher', 'education', 'professor']):
            return 'Education'
        elif any(word in title_lower for word in ['finance', 'accounting', 'financial']):
            return 'Finance'
        elif any(word in title_lower for word in ['design', 'creative', 'artist']):
            return 'Design'
        else:
            return 'General'
    
    def estimate_salary_range(self, title: str) -> str:
        """Estimate salary range based on job title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['engineer', 'developer', 'data scientist', 'manager']):
            return '$60,000 - $120,000'
        elif any(word in title_lower for word in ['analyst', 'specialist', 'coordinator']):
            return '$45,000 - $80,000'
        elif any(word in title_lower for word in ['representative', 'assistant', 'clerk']):
            return '$30,000 - $55,000'
        elif any(word in title_lower for word in ['director', 'senior', 'lead']):
            return '$80,000 - $150,000'
        else:
            return '$40,000 - $70,000'
    
    def get_common_skills(self, title: str) -> str:
        """Get common skills for job title"""
        title_lower = title.lower()
        
        skill_mapping = {
            'software': 'Programming, Problem-solving, Teamwork, Communication',
            'data': 'Python, SQL, Statistics, Machine Learning, Visualization',
            'manager': 'Leadership, Communication, Project Management, Strategic Planning',
            'marketing': 'Digital Marketing, Analytics, Content Creation, Social Media',
            'sales': 'Communication, Negotiation, CRM, Customer Service',
            'design': 'Creative Software, Visual Design, User Experience, Typography',
            'nurse': 'Patient Care, Medical Knowledge, Communication, Empathy',
            'teacher': 'Communication, Curriculum Development, Classroom Management',
            'accountant': 'Financial Analysis, Excel, Attention to Detail, Compliance'
        }
        
        for key, skills in skill_mapping.items():
            if key in title_lower:
                return skills
        
        return 'Communication, Problem-solving, Teamwork, Adaptability'
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method"""
        all_careers = []
        
        try:
            # Scrape BLS careers (more detailed but slower)
            bls_careers = self.scrape_bls_careers()
            all_careers.extend(bls_careers)
            
            # Add common careers with estimated data
            indeed_careers = self.scrape_indeed_careers()
            all_careers.extend(indeed_careers)
            
        except Exception as e:
            logger.error(f"Error during career scraping: {e}")
        
        # Remove duplicates based on title
        unique_careers = []
        seen_titles = set()
        
        for career in all_careers:
            if career['title'] not in seen_titles:
                unique_careers.append(career)
                seen_titles.add(career['title'])
        
        logger.info(f"Total unique careers scraped: {len(unique_careers)}")
        return unique_careers
