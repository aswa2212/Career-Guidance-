import re
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class CollegeScraper(BaseScraper):
    """Scraper for college and university information"""
    
    def __init__(self):
        super().__init__(delay_range=(3, 5))  # Be more respectful to educational sites
        self.colleges = []
    
    def scrape_indian_colleges(self) -> List[Dict]:
        """Scrape Indian colleges and universities"""
        colleges = []
        
        # Create comprehensive list of well-known Indian institutions
        indian_institutions = [
            # IITs
            {'name': 'Indian Institute of Technology Bombay', 'city': 'Mumbai', 'state': 'Maharashtra', 'type': 'Engineering'},
            {'name': 'Indian Institute of Technology Delhi', 'city': 'New Delhi', 'state': 'Delhi', 'type': 'Engineering'},
            {'name': 'Indian Institute of Technology Kanpur', 'city': 'Kanpur', 'state': 'Uttar Pradesh', 'type': 'Engineering'},
            {'name': 'Indian Institute of Technology Kharagpur', 'city': 'Kharagpur', 'state': 'West Bengal', 'type': 'Engineering'},
            {'name': 'Indian Institute of Technology Madras', 'city': 'Chennai', 'state': 'Tamil Nadu', 'type': 'Engineering'},
            {'name': 'Indian Institute of Technology Roorkee', 'city': 'Roorkee', 'state': 'Uttarakhand', 'type': 'Engineering'},
            {'name': 'Indian Institute of Technology Guwahati', 'city': 'Guwahati', 'state': 'Assam', 'type': 'Engineering'},
            {'name': 'Indian Institute of Technology Hyderabad', 'city': 'Hyderabad', 'state': 'Telangana', 'type': 'Engineering'},
            
            # IIMs
            {'name': 'Indian Institute of Management Ahmedabad', 'city': 'Ahmedabad', 'state': 'Gujarat', 'type': 'Management'},
            {'name': 'Indian Institute of Management Bangalore', 'city': 'Bangalore', 'state': 'Karnataka', 'type': 'Management'},
            {'name': 'Indian Institute of Management Calcutta', 'city': 'Kolkata', 'state': 'West Bengal', 'type': 'Management'},
            {'name': 'Indian Institute of Management Lucknow', 'city': 'Lucknow', 'state': 'Uttar Pradesh', 'type': 'Management'},
            {'name': 'Indian Institute of Management Indore', 'city': 'Indore', 'state': 'Madhya Pradesh', 'type': 'Management'},
            
            # Medical Colleges
            {'name': 'All India Institute of Medical Sciences Delhi', 'city': 'New Delhi', 'state': 'Delhi', 'type': 'Medical'},
            {'name': 'Christian Medical College Vellore', 'city': 'Vellore', 'state': 'Tamil Nadu', 'type': 'Medical'},
            {'name': 'Armed Forces Medical College', 'city': 'Pune', 'state': 'Maharashtra', 'type': 'Medical'},
            {'name': 'King George Medical University', 'city': 'Lucknow', 'state': 'Uttar Pradesh', 'type': 'Medical'},
            
            # Universities
            {'name': 'University of Delhi', 'city': 'New Delhi', 'state': 'Delhi', 'type': 'University'},
            {'name': 'Jawaharlal Nehru University', 'city': 'New Delhi', 'state': 'Delhi', 'type': 'University'},
            {'name': 'University of Mumbai', 'city': 'Mumbai', 'state': 'Maharashtra', 'type': 'University'},
            {'name': 'University of Calcutta', 'city': 'Kolkata', 'state': 'West Bengal', 'type': 'University'},
            {'name': 'Banaras Hindu University', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'type': 'University'},
            {'name': 'Aligarh Muslim University', 'city': 'Aligarh', 'state': 'Uttar Pradesh', 'type': 'University'},
            {'name': 'Anna University', 'city': 'Chennai', 'state': 'Tamil Nadu', 'type': 'University'},
            {'name': 'Pune University', 'city': 'Pune', 'state': 'Maharashtra', 'type': 'University'},
            
            # Private Universities
            {'name': 'Manipal Academy of Higher Education', 'city': 'Manipal', 'state': 'Karnataka', 'type': 'Private'},
            {'name': 'Birla Institute of Technology and Science', 'city': 'Pilani', 'state': 'Rajasthan', 'type': 'Private'},
            {'name': 'Vellore Institute of Technology', 'city': 'Vellore', 'state': 'Tamil Nadu', 'type': 'Private'},
            {'name': 'SRM Institute of Science and Technology', 'city': 'Chennai', 'state': 'Tamil Nadu', 'type': 'Private'},
            {'name': 'Amity University', 'city': 'Noida', 'state': 'Uttar Pradesh', 'type': 'Private'},
            {'name': 'Lovely Professional University', 'city': 'Phagwara', 'state': 'Punjab', 'type': 'Private'},
            
            # State Universities
            {'name': 'Osmania University', 'city': 'Hyderabad', 'state': 'Telangana', 'type': 'State University'},
            {'name': 'University of Madras', 'city': 'Chennai', 'state': 'Tamil Nadu', 'type': 'State University'},
            {'name': 'Gujarat University', 'city': 'Ahmedabad', 'state': 'Gujarat', 'type': 'State University'},
            {'name': 'University of Rajasthan', 'city': 'Jaipur', 'state': 'Rajasthan', 'type': 'State University'},
        ]
        
        for institution in indian_institutions:
            try:
                college = {
                    'name': institution['name'],
                    'address': f"{institution['city']}, {institution['state']}, India",
                    'city': institution['city'],
                    'state': institution['state'],
                    'pincode': self.get_sample_pincode(institution['state']),
                    'website': self.generate_website_url(institution['name']),
                    'latitude': self.get_approximate_coordinates(institution['city'], institution['state'])[0],
                    'longitude': self.get_approximate_coordinates(institution['city'], institution['state'])[1],
                    'scholarship_details': self.get_scholarship_info(institution['type'])
                }
                colleges.append(college)
                
            except Exception as e:
                logger.warning(f"Error creating college entry for {institution['name']}: {e}")
                continue
        
        logger.info(f"Created {len(colleges)} Indian college entries")
        return colleges
    
    def scrape_us_colleges(self) -> List[Dict]:
        """Create entries for major US universities"""
        colleges = []
        
        us_institutions = [
            {'name': 'Harvard University', 'city': 'Cambridge', 'state': 'Massachusetts'},
            {'name': 'Stanford University', 'city': 'Stanford', 'state': 'California'},
            {'name': 'Massachusetts Institute of Technology', 'city': 'Cambridge', 'state': 'Massachusetts'},
            {'name': 'California Institute of Technology', 'city': 'Pasadena', 'state': 'California'},
            {'name': 'University of California Berkeley', 'city': 'Berkeley', 'state': 'California'},
            {'name': 'Princeton University', 'city': 'Princeton', 'state': 'New Jersey'},
            {'name': 'Yale University', 'city': 'New Haven', 'state': 'Connecticut'},
            {'name': 'Columbia University', 'city': 'New York', 'state': 'New York'},
            {'name': 'University of Chicago', 'city': 'Chicago', 'state': 'Illinois'},
            {'name': 'Cornell University', 'city': 'Ithaca', 'state': 'New York'},
        ]
        
        for institution in us_institutions:
            try:
                college = {
                    'name': institution['name'],
                    'address': f"{institution['city']}, {institution['state']}, USA",
                    'city': institution['city'],
                    'state': institution['state'],
                    'pincode': '00000',  # US uses ZIP codes
                    'website': self.generate_website_url(institution['name']),
                    'latitude': self.get_us_coordinates(institution['city'], institution['state'])[0],
                    'longitude': self.get_us_coordinates(institution['city'], institution['state'])[1],
                    'scholarship_details': 'Merit-based and need-based scholarships available. International student financial aid programs.'
                }
                colleges.append(college)
                
            except Exception as e:
                logger.warning(f"Error creating US college entry for {institution['name']}: {e}")
                continue
        
        logger.info(f"Created {len(colleges)} US college entries")
        return colleges
    
    def generate_website_url(self, college_name: str) -> str:
        """Generate likely website URL for college"""
        # Simplify name for URL generation
        name_parts = college_name.lower().split()
        
        # Common patterns for educational institution websites
        if 'iit' in college_name.lower():
            city = name_parts[-1] if len(name_parts) > 3 else 'main'
            return f"https://www.iit{city}.ac.in"
        elif 'iim' in college_name.lower():
            city = name_parts[-1] if len(name_parts) > 3 else 'main'
            return f"https://www.iim{city}.ac.in"
        elif 'university' in college_name.lower():
            # Extract main word before 'university'
            main_word = name_parts[0] if name_parts else 'university'
            return f"https://www.{main_word}university.edu"
        else:
            # Generic pattern
            main_word = name_parts[0] if name_parts else 'college'
            return f"https://www.{main_word}.edu"
    
    def get_sample_pincode(self, state: str) -> str:
        """Get sample pincode for Indian states"""
        pincode_mapping = {
            'Maharashtra': '400001',
            'Delhi': '110001',
            'Karnataka': '560001',
            'Tamil Nadu': '600001',
            'West Bengal': '700001',
            'Gujarat': '380001',
            'Uttar Pradesh': '201301',
            'Rajasthan': '302001',
            'Telangana': '500001',
            'Assam': '781001',
            'Uttarakhand': '248001',
            'Madhya Pradesh': '452001',
            'Punjab': '144411'
        }
        return pincode_mapping.get(state, '000001')
    
    def get_approximate_coordinates(self, city: str, state: str) -> tuple:
        """Get approximate coordinates for Indian cities"""
        coordinates = {
            ('Mumbai', 'Maharashtra'): (19.0760, 72.8777),
            ('New Delhi', 'Delhi'): (28.6139, 77.2090),
            ('Bangalore', 'Karnataka'): (12.9716, 77.5946),
            ('Chennai', 'Tamil Nadu'): (13.0827, 80.2707),
            ('Kolkata', 'West Bengal'): (22.5726, 88.3639),
            ('Ahmedabad', 'Gujarat'): (23.0225, 72.5714),
            ('Pune', 'Maharashtra'): (18.5204, 73.8567),
            ('Hyderabad', 'Telangana'): (17.3850, 78.4867),
            ('Kanpur', 'Uttar Pradesh'): (26.4499, 80.3319),
            ('Jaipur', 'Rajasthan'): (26.9124, 75.7873),
            ('Lucknow', 'Uttar Pradesh'): (26.8467, 80.9462),
            ('Guwahati', 'Assam'): (26.1445, 91.7362),
            ('Roorkee', 'Uttarakhand'): (29.8543, 77.8880),
            ('Indore', 'Madhya Pradesh'): (22.7196, 75.8577),
            ('Vellore', 'Tamil Nadu'): (12.9165, 79.1325),
            ('Varanasi', 'Uttar Pradesh'): (25.3176, 82.9739),
            ('Aligarh', 'Uttar Pradesh'): (27.8974, 78.0880),
            ('Pilani', 'Rajasthan'): (28.3670, 75.6032),
            ('Manipal', 'Karnataka'): (13.3467, 74.7854),
            ('Noida', 'Uttar Pradesh'): (28.5355, 77.3910),
            ('Phagwara', 'Punjab'): (31.2244, 75.7729)
        }
        return coordinates.get((city, state), (20.5937, 78.9629))  # Default to India center
    
    def get_us_coordinates(self, city: str, state: str) -> tuple:
        """Get approximate coordinates for US cities"""
        coordinates = {
            ('Cambridge', 'Massachusetts'): (42.3736, -71.1097),
            ('Stanford', 'California'): (37.4419, -122.1430),
            ('Pasadena', 'California'): (34.1478, -118.1445),
            ('Berkeley', 'California'): (37.8715, -122.2730),
            ('Princeton', 'New Jersey'): (40.3573, -74.6672),
            ('New Haven', 'Connecticut'): (41.3083, -72.9279),
            ('New York', 'New York'): (40.7128, -74.0060),
            ('Chicago', 'Illinois'): (41.8781, -87.6298),
            ('Ithaca', 'New York'): (42.4430, -76.5019)
        }
        return coordinates.get((city, state), (39.8283, -98.5795))  # Default to US center
    
    def get_scholarship_info(self, institution_type: str) -> str:
        """Get scholarship information based on institution type"""
        scholarship_mapping = {
            'Engineering': 'Merit scholarships, SC/ST scholarships, State government scholarships, Industry-sponsored scholarships available.',
            'Management': 'Merit-based scholarships, Need-based financial aid, Alumni scholarships, Corporate sponsorships available.',
            'Medical': 'Government scholarships, Merit scholarships, Minority scholarships, State quota benefits available.',
            'University': 'Various scholarships including merit-based, need-based, research scholarships, and government schemes.',
            'Private': 'Merit scholarships, Alumni scholarships, Corporate tie-up scholarships, Educational loans assistance.',
            'State University': 'State government scholarships, Central government schemes, Merit scholarships, Fee concessions available.'
        }
        return scholarship_mapping.get(institution_type, 'Various scholarship programs available for eligible students.')
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method"""
        all_colleges = []
        
        try:
            # Add Indian colleges
            indian_colleges = self.scrape_indian_colleges()
            all_colleges.extend(indian_colleges)
            
            # Add US colleges
            us_colleges = self.scrape_us_colleges()
            all_colleges.extend(us_colleges)
            
        except Exception as e:
            logger.error(f"Error during college scraping: {e}")
        
        logger.info(f"Total colleges created: {len(all_colleges)}")
        return all_colleges
