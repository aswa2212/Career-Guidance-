import re
import requests
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger
from bs4 import BeautifulSoup

class RealJKCollegeScraper(BaseScraper):
    """Real web scraper for Jammu & Kashmir colleges from government websites"""
    
    def __init__(self):
        super().__init__(delay_range=(3, 6))  # Be respectful to government sites
        self.colleges = []
    
    def scrape_jk_government_portal(self) -> List[Dict]:
        """Scrape J&K colleges from government education portal"""
        colleges = []
        
        # More reliable URLs with fallbacks
        urls_to_scrape = [
            'https://www.kashmiruniversity.net',
            'https://www.jammuuniversity.ac.in',
            'https://www.cukashmir.ac.in',
            'https://www.cujammu.ac.in'
        ]
        
        for url in urls_to_scrape:
            try:
                logger.info(f"Scraping J&K colleges from: {url}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Look for college listings
                college_elements = self.find_college_elements(soup)
                
                for element in college_elements:
                    college_data = self.extract_college_info(element, url)
                    if college_data:
                        colleges.append(college_data)
                        
            except Exception as e:
                logger.warning(f"Error scraping {url}: {e}")
                continue
        
        logger.info(f"Scraped {len(colleges)} colleges from J&K government websites")
        return colleges
    
    def find_college_elements(self, soup: BeautifulSoup) -> List:
        """Find college listing elements in the page"""
        college_elements = []
        
        # Common patterns for college listings
        selectors = [
            'div.college-item',
            'tr td',  # Table rows
            'li a[href*="college"]',
            'div.institution',
            '.college-list li',
            '.college-name',
            'a[href*="college"]',
            'div[class*="college"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                college_elements.extend(elements)
                break
        
        # If no specific selectors work, look for links with college-related text
        if not college_elements:
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                text = link.get_text().lower()
                if any(word in text for word in ['college', 'university', 'institute', 'school']):
                    college_elements.append(link)
        
        return college_elements[:50]  # Limit to avoid too many requests
    
    def extract_college_info(self, element, source_url: str) -> Dict:
        """Extract college information from HTML element"""
        try:
            # Extract college name
            name = self.safe_extract(element, 'a, h3, h2, .name, .title')
            if not name:
                name = self.clean_text(element.get_text())
            
            if len(name) < 5:  # Skip if name too short
                return None
            
            # Extract additional info if available
            address = self.safe_extract(element, '.address, .location')
            city = self.extract_city_from_text(name + ' ' + address)
            
            # Extract website if available
            website = ''
            link_elem = element.find('a', href=True)
            if link_elem:
                href = link_elem.get('href')
                if href and href.startswith('http'):
                    website = href
            
            college = {
                'name': name,
                'address': address or f"{city}, Jammu and Kashmir, India",
                'city': city,
                'state': 'Jammu and Kashmir',
                'pincode': self.get_jk_pincode_by_city(city),
                'website': website,
                'latitude': self.get_jk_coordinates(city)[0],
                'longitude': self.get_jk_coordinates(city)[1],
                'scholarship_details': 'Government scholarships and merit-based financial assistance available.',
                'source_url': source_url,
                'scraped_from': 'J&K Government Portal'
            }
            
            return college
            
        except Exception as e:
            logger.warning(f"Error extracting college info: {e}")
            return None
    
    def extract_city_from_text(self, text: str) -> str:
        """Extract city name from college name or address"""
        text_lower = text.lower()
        
        jk_cities = [
            'srinagar', 'jammu', 'anantnag', 'baramulla', 'kupwara', 'pulwama',
            'shopian', 'budgam', 'ganderbal', 'bandipora', 'kulgam', 'kathua',
            'udhampur', 'doda', 'rajouri', 'poonch', 'reasi', 'ramban', 'kishtwar', 'samba'
        ]
        
        for city in jk_cities:
            if city in text_lower:
                return city.title()
        
        return 'Srinagar'  # Default
    
    def get_jk_pincode_by_city(self, city: str) -> str:
        """Get pincode for J&K cities"""
        pincode_mapping = {
            'Srinagar': '190001', 'Jammu': '180001', 'Anantnag': '192101',
            'Baramulla': '193101', 'Kupwara': '193222', 'Pulwama': '192301',
            'Shopian': '192303', 'Budgam': '191111', 'Ganderbal': '191201',
            'Bandipora': '193502', 'Kulgam': '192231', 'Kathua': '184101',
            'Udhampur': '182101', 'Doda': '182202', 'Rajouri': '185131',
            'Poonch': '185101', 'Reasi': '182311', 'Ramban': '182144',
            'Kishtwar': '182204', 'Samba': '184121'
        }
        return pincode_mapping.get(city, '190001')
    
    def get_jk_coordinates(self, city: str) -> tuple:
        """Get coordinates for J&K cities"""
        coordinates = {
            'Srinagar': (34.0837, 74.7973), 'Jammu': (32.7266, 74.8570),
            'Anantnag': (33.7311, 75.1480), 'Baramulla': (34.2094, 74.3428),
            'Kupwara': (34.5267, 74.2467), 'Pulwama': (33.8712, 74.8947),
            'Shopian': (33.7081, 74.8308), 'Budgam': (34.0230, 74.7350),
            'Ganderbal': (34.2307, 74.7847), 'Bandipora': (34.4186, 74.6398),
            'Kulgam': (33.6411, 75.0197), 'Kathua': (32.3705, 75.5224),
            'Udhampur': (32.9150, 75.1411), 'Doda': (33.1390, 75.5467),
            'Rajouri': (33.3731, 74.3072), 'Poonch': (33.7739, 74.0894),
            'Reasi': (33.0839, 74.8339), 'Ramban': (33.2431, 75.2339),
            'Kishtwar': (33.3119, 75.7669), 'Samba': (32.5625, 75.1194)
        }
        return coordinates.get(city, (33.7782, 76.5762))
    
    def scrape_university_websites(self) -> List[Dict]:
        """Scrape affiliated colleges from university websites"""
        colleges = []
        
        university_urls = [
            'https://www.kashmiruniversity.net',
            'https://www.jammuuniversity.ac.in',
            'https://www.cukashmir.ac.in',
            'https://www.cujammu.ac.in'
        ]
        
        for url in university_urls:
            try:
                logger.info(f"Scraping university website: {url}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Look for affiliated colleges or departments
                college_links = soup.find_all('a', href=True)
                
                for link in college_links:
                    text = link.get_text().lower()
                    if any(word in text for word in ['college', 'department', 'school', 'institute']):
                        college_data = self.extract_college_info(link, url)
                        if college_data:
                            colleges.append(college_data)
                            
            except Exception as e:
                logger.warning(f"Error scraping university {url}: {e}")
                continue
        
        return colleges
    
    def scrape_education_directory(self) -> List[Dict]:
        """Scrape from education directory websites"""
        colleges = []
        
        # Use more reliable education portals
        directory_urls = [
            'https://www.shiksha.com/college/jammu-kashmir-colleges',
            'https://www.collegedunia.com/jammu-and-kashmir-colleges'
        ]
        
        for url in directory_urls:
            try:
                logger.info(f"Scraping education directory: {url}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Look for college cards or listings
                college_cards = soup.find_all(['div', 'li'], class_=re.compile(r'college|card|item'))
                
                for card in college_cards[:20]:  # Limit per site
                    college_data = self.extract_college_info(card, url)
                    if college_data:
                        colleges.append(college_data)
                        
            except Exception as e:
                logger.warning(f"Error scraping directory {url}: {e}")
                continue
        
        return colleges
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method for real J&K colleges"""
        all_colleges = []
        
        try:
            # Scrape government portals
            gov_colleges = self.scrape_jk_government_portal()
            all_colleges.extend(gov_colleges)
            
            # Scrape university websites
            uni_colleges = self.scrape_university_websites()
            all_colleges.extend(uni_colleges)
            
            # Scrape education directories
            dir_colleges = self.scrape_education_directory()
            all_colleges.extend(dir_colleges)
            
            # If we got very few results, use fallback
            if len(all_colleges) < 5:
                logger.warning("Few colleges scraped, using fallback scraper...")
                from .fallback_jk_scraper import FallbackJKScraper
                fallback_scraper = FallbackJKScraper()
                fallback_colleges = fallback_scraper.scrape()
                all_colleges.extend(fallback_colleges)
            
        except Exception as e:
            logger.error(f"Error during J&K college scraping: {e}")
            # Use fallback on error
            try:
                logger.info("Using fallback scraper due to errors...")
                from .fallback_jk_scraper import FallbackJKScraper
                fallback_scraper = FallbackJKScraper()
                fallback_colleges = fallback_scraper.scrape()
                all_colleges.extend(fallback_colleges)
            except Exception as fallback_error:
                logger.error(f"Fallback scraper also failed: {fallback_error}")
        
        # Remove duplicates based on name
        unique_colleges = []
        seen_names = set()
        
        for college in all_colleges:
            name = college.get('name', '').lower()
            if name and name not in seen_names:
                unique_colleges.append(college)
                seen_names.add(name)
        
        logger.info(f"Total unique J&K colleges scraped: {len(unique_colleges)}")
        return unique_colleges
