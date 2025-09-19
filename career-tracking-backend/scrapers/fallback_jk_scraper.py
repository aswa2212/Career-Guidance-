import re
import requests
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class FallbackJKScraper(BaseScraper):
    """Fallback scraper for J&K colleges when websites are unavailable"""
    
    def __init__(self):
        super().__init__(delay_range=(1, 2))
        self.colleges = []
    
    def scrape_wikipedia_jk_colleges(self) -> List[Dict]:
        """Scrape J&K colleges from Wikipedia (more reliable)"""
        colleges = []
        
        try:
            # Wikipedia pages are more reliable
            urls = [
                'https://en.wikipedia.org/wiki/List_of_universities_in_Jammu_and_Kashmir',
                'https://en.wikipedia.org/wiki/University_of_Kashmir',
                'https://en.wikipedia.org/wiki/University_of_Jammu'
            ]
            
            for url in urls:
                logger.info(f"Scraping Wikipedia: {url}")
                soup = self.get_page(url)
                
                if not soup:
                    continue
                
                # Find tables or lists with college information
                tables = soup.find_all('table', class_='wikitable')
                lists = soup.find_all('ul')
                
                # Extract from tables
                for table in tables:
                    rows = table.find_all('tr')[1:]  # Skip header
                    for row in rows[:10]:  # Limit
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            name = self.clean_text(cells[0].get_text())
                            location = self.clean_text(cells[1].get_text()) if len(cells) > 1 else 'Jammu and Kashmir'
                            
                            if len(name) > 5 and any(word in name.lower() for word in ['college', 'university', 'institute']):
                                college = self.create_college_entry(name, location)
                                if college:
                                    colleges.append(college)
                
                # Extract from lists
                for ul in lists:
                    items = ul.find_all('li')
                    for item in items[:15]:  # Limit
                        text = self.clean_text(item.get_text())
                        if len(text) > 10 and any(word in text.lower() for word in ['college', 'university', 'institute']):
                            college = self.create_college_entry(text, 'Jammu and Kashmir')
                            if college:
                                colleges.append(college)
        
        except Exception as e:
            logger.warning(f"Error scraping Wikipedia: {e}")
        
        logger.info(f"Scraped {len(colleges)} colleges from Wikipedia")
        return colleges
    
    def create_college_entry(self, name: str, location: str) -> Dict:
        """Create a college entry from name and location"""
        try:
            city = self.extract_city_from_text(name + ' ' + location)
            
            college = {
                'name': name,
                'address': f"{city}, Jammu and Kashmir, India",
                'city': city,
                'state': 'Jammu and Kashmir',
                'pincode': self.get_jk_pincode_by_city(city),
                'website': self.generate_website_url(name),
                'latitude': self.get_jk_coordinates(city)[0],
                'longitude': self.get_jk_coordinates(city)[1],
                'scholarship_details': 'Government scholarships and merit-based financial assistance available.',
                'source_url': 'Wikipedia',
                'scraped_from': 'Wikipedia Fallback'
            }
            
            return college
            
        except Exception as e:
            logger.warning(f"Error creating college entry: {e}")
            return None
    
    def scrape_known_jk_colleges(self) -> List[Dict]:
        """Create entries for well-known J&K colleges (fallback data)"""
        colleges = []
        
        # Well-known J&K institutions (as fallback when scraping fails)
        known_colleges = [
            {'name': 'University of Kashmir', 'city': 'Srinagar', 'type': 'University'},
            {'name': 'University of Jammu', 'city': 'Jammu', 'type': 'University'},
            {'name': 'Central University of Kashmir', 'city': 'Ganderbal', 'type': 'Central University'},
            {'name': 'Central University of Jammu', 'city': 'Samba', 'type': 'Central University'},
            {'name': 'National Institute of Technology Srinagar', 'city': 'Srinagar', 'type': 'Engineering'},
            {'name': 'Government Medical College Srinagar', 'city': 'Srinagar', 'type': 'Medical'},
            {'name': 'Government Medical College Jammu', 'city': 'Jammu', 'type': 'Medical'},
            {'name': 'Government Degree College Srinagar', 'city': 'Srinagar', 'type': 'Degree College'},
            {'name': 'Government Degree College Jammu', 'city': 'Jammu', 'type': 'Degree College'},
            {'name': 'Government College for Women Srinagar', 'city': 'Srinagar', 'type': 'Women College'},
            {'name': 'Government College for Women Jammu', 'city': 'Jammu', 'type': 'Women College'},
            {'name': 'Government Degree College Anantnag', 'city': 'Anantnag', 'type': 'Degree College'},
            {'name': 'Government Degree College Baramulla', 'city': 'Baramulla', 'type': 'Degree College'},
            {'name': 'Government Degree College Kupwara', 'city': 'Kupwara', 'type': 'Degree College'},
            {'name': 'Government Degree College Pulwama', 'city': 'Pulwama', 'type': 'Degree College'},
            {'name': 'Government Degree College Kathua', 'city': 'Kathua', 'type': 'Degree College'},
            {'name': 'Government Degree College Udhampur', 'city': 'Udhampur', 'type': 'Degree College'},
            {'name': 'Government Degree College Rajouri', 'city': 'Rajouri', 'type': 'Degree College'},
            {'name': 'Government Degree College Poonch', 'city': 'Poonch', 'type': 'Degree College'},
            {'name': 'Government Polytechnic Jammu', 'city': 'Jammu', 'type': 'Polytechnic'},
            {'name': 'Government Polytechnic Srinagar', 'city': 'Srinagar', 'type': 'Polytechnic'}
        ]
        
        for college_info in known_colleges:
            college = {
                'name': college_info['name'],
                'address': f"{college_info['city']}, Jammu and Kashmir, India",
                'city': college_info['city'],
                'state': 'Jammu and Kashmir',
                'pincode': self.get_jk_pincode_by_city(college_info['city']),
                'website': self.generate_website_url(college_info['name']),
                'latitude': self.get_jk_coordinates(college_info['city'])[0],
                'longitude': self.get_jk_coordinates(college_info['city'])[1],
                'scholarship_details': self.get_scholarship_info(college_info['type']),
                'source_url': 'Fallback Database',
                'scraped_from': 'Known Institutions Fallback'
            }
            colleges.append(college)
        
        logger.info(f"Created {len(colleges)} known J&K college entries")
        return colleges
    
    def extract_city_from_text(self, text: str) -> str:
        """Extract city name from text"""
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
    
    def generate_website_url(self, college_name: str) -> str:
        """Generate likely website URL"""
        name_lower = college_name.lower()
        
        if 'university of kashmir' in name_lower:
            return 'https://www.kashmiruniversity.net'
        elif 'university of jammu' in name_lower:
            return 'https://www.jammuuniversity.ac.in'
        elif 'central university of kashmir' in name_lower:
            return 'https://www.cukashmir.ac.in'
        elif 'central university of jammu' in name_lower:
            return 'https://www.cujammu.ac.in'
        elif 'nit srinagar' in name_lower:
            return 'https://www.nitsri.ac.in'
        else:
            return 'https://www.jkeducation.gov.in'
    
    def get_scholarship_info(self, college_type: str) -> str:
        """Get scholarship information"""
        scholarship_mapping = {
            'University': 'UGC scholarships, Merit scholarships, SC/ST/OBC scholarships, State government scholarships.',
            'Central University': 'Central government scholarships, UGC scholarships, Merit scholarships, Research fellowships.',
            'Engineering': 'Technical education scholarships, Merit scholarships, Industry scholarships, JEE-based scholarships.',
            'Medical': 'Medical education scholarships, NEET-based scholarships, Government medical scholarships.',
            'Degree College': 'State government scholarships, Merit scholarships, Need-based financial assistance.',
            'Women College': 'Women empowerment scholarships, Merit scholarships, State government scholarships.',
            'Polytechnic': 'Technical education scholarships, Skill development scholarships, Merit scholarships.'
        }
        return scholarship_mapping.get(college_type, 'Various government scholarships and merit-based financial assistance available.')
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method with fallback options"""
        all_colleges = []
        
        try:
            # Try Wikipedia first (more reliable)
            wiki_colleges = self.scrape_wikipedia_jk_colleges()
            all_colleges.extend(wiki_colleges)
            
            # Add known colleges as fallback
            known_colleges = self.scrape_known_jk_colleges()
            all_colleges.extend(known_colleges)
            
        except Exception as e:
            logger.error(f"Error during fallback scraping: {e}")
        
        # Remove duplicates
        unique_colleges = []
        seen_names = set()
        
        for college in all_colleges:
            name = college.get('name', '').lower()
            if name and name not in seen_names:
                unique_colleges.append(college)
                seen_names.add(name)
        
        logger.info(f"Total fallback colleges: {len(unique_colleges)}")
        return unique_colleges
