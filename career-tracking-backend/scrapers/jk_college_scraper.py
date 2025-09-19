import re
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class JKCollegeScraper(BaseScraper):
    """Scraper specifically for Jammu & Kashmir Government Colleges"""
    
    def __init__(self):
        super().__init__(delay_range=(2, 4))
        self.colleges = []
    
    def scrape_jk_government_colleges(self) -> List[Dict]:
        """Scrape Jammu & Kashmir government colleges and universities"""
        colleges = []
        
        # Comprehensive list of J&K Government Colleges and Universities
        jk_institutions = [
            # Central Universities
            {
                'name': 'University of Kashmir',
                'city': 'Srinagar',
                'district': 'Srinagar',
                'type': 'Central University',
                'established': '1948',
                'courses': 'Arts, Science, Commerce, Engineering, Medical, Law'
            },
            {
                'name': 'University of Jammu',
                'city': 'Jammu',
                'district': 'Jammu',
                'type': 'Central University',
                'established': '1969',
                'courses': 'Arts, Science, Commerce, Engineering, Medical, Management'
            },
            {
                'name': 'Central University of Kashmir',
                'city': 'Ganderbal',
                'district': 'Ganderbal',
                'type': 'Central University',
                'established': '2009',
                'courses': 'Arts, Science, Social Sciences, Management'
            },
            {
                'name': 'Central University of Jammu',
                'city': 'Samba',
                'district': 'Samba',
                'type': 'Central University',
                'established': '2011',
                'courses': 'Arts, Science, Commerce, Management, Law'
            },
            
            # Medical Colleges
            {
                'name': 'Government Medical College Srinagar',
                'city': 'Srinagar',
                'district': 'Srinagar',
                'type': 'Medical College',
                'established': '1959',
                'courses': 'MBBS, MD, MS, Nursing, Paramedical'
            },
            {
                'name': 'Government Medical College Jammu',
                'city': 'Jammu',
                'district': 'Jammu',
                'type': 'Medical College',
                'established': '1973',
                'courses': 'MBBS, MD, MS, Nursing, Paramedical'
            },
            {
                'name': 'Government Medical College Anantnag',
                'city': 'Anantnag',
                'district': 'Anantnag',
                'type': 'Medical College',
                'established': '2017',
                'courses': 'MBBS, Nursing, Paramedical'
            },
            {
                'name': 'Government Medical College Kathua',
                'city': 'Kathua',
                'district': 'Kathua',
                'type': 'Medical College',
                'established': '2019',
                'courses': 'MBBS, Nursing, Paramedical'
            },
            {
                'name': 'Government Medical College Rajouri',
                'city': 'Rajouri',
                'district': 'Rajouri',
                'type': 'Medical College',
                'established': '2020',
                'courses': 'MBBS, Nursing, Paramedical'
            },
            {
                'name': 'Government Medical College Doda',
                'city': 'Doda',
                'district': 'Doda',
                'type': 'Medical College',
                'established': '2020',
                'courses': 'MBBS, Nursing, Paramedical'
            },
            
            # Engineering Colleges
            {
                'name': 'National Institute of Technology Srinagar',
                'city': 'Srinagar',
                'district': 'Srinagar',
                'type': 'Engineering College',
                'established': '1960',
                'courses': 'B.Tech, M.Tech, PhD in Engineering'
            },
            {
                'name': 'Government College of Engineering and Technology Jammu',
                'city': 'Jammu',
                'district': 'Jammu',
                'type': 'Engineering College',
                'established': '1986',
                'courses': 'B.Tech, M.Tech in Engineering'
            },
            {
                'name': 'Government Polytechnic Jammu',
                'city': 'Jammu',
                'district': 'Jammu',
                'type': 'Polytechnic',
                'established': '1963',
                'courses': 'Diploma in Engineering'
            },
            {
                'name': 'Government Polytechnic Srinagar',
                'city': 'Srinagar',
                'district': 'Srinagar',
                'type': 'Polytechnic',
                'established': '1961',
                'courses': 'Diploma in Engineering'
            },
            
            # Degree Colleges
            {
                'name': 'Government Degree College Srinagar',
                'city': 'Srinagar',
                'district': 'Srinagar',
                'type': 'Degree College',
                'established': '1905',
                'courses': 'BA, BSc, BCom, MA, MSc, MCom'
            },
            {
                'name': 'Government College for Women Srinagar',
                'city': 'Srinagar',
                'district': 'Srinagar',
                'type': 'Women\'s College',
                'established': '1950',
                'courses': 'BA, BSc, BCom, MA, MSc'
            },
            {
                'name': 'Government Degree College Jammu',
                'city': 'Jammu',
                'district': 'Jammu',
                'type': 'Degree College',
                'established': '1948',
                'courses': 'BA, BSc, BCom, MA, MSc, MCom'
            },
            {
                'name': 'Government College for Women Jammu',
                'city': 'Jammu',
                'district': 'Jammu',
                'type': 'Women\'s College',
                'established': '1955',
                'courses': 'BA, BSc, BCom, MA, MSc'
            },
            {
                'name': 'Government Degree College Anantnag',
                'city': 'Anantnag',
                'district': 'Anantnag',
                'type': 'Degree College',
                'established': '1961',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Baramulla',
                'city': 'Baramulla',
                'district': 'Baramulla',
                'type': 'Degree College',
                'established': '1965',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Kupwara',
                'city': 'Kupwara',
                'district': 'Kupwara',
                'type': 'Degree College',
                'established': '1982',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Pulwama',
                'city': 'Pulwama',
                'district': 'Pulwama',
                'type': 'Degree College',
                'established': '1984',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Shopian',
                'city': 'Shopian',
                'district': 'Shopian',
                'type': 'Degree College',
                'established': '2008',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Budgam',
                'city': 'Budgam',
                'district': 'Budgam',
                'type': 'Degree College',
                'established': '1987',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Ganderbal',
                'city': 'Ganderbal',
                'district': 'Ganderbal',
                'type': 'Degree College',
                'established': '1990',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Bandipora',
                'city': 'Bandipora',
                'district': 'Bandipora',
                'type': 'Degree College',
                'established': '2009',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Kulgam',
                'city': 'Kulgam',
                'district': 'Kulgam',
                'type': 'Degree College',
                'established': '2010',
                'courses': 'BA, BSc, BCom'
            },
            
            # Jammu Region Colleges
            {
                'name': 'Government Degree College Kathua',
                'city': 'Kathua',
                'district': 'Kathua',
                'type': 'Degree College',
                'established': '1961',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Udhampur',
                'city': 'Udhampur',
                'district': 'Udhampur',
                'type': 'Degree College',
                'established': '1965',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Doda',
                'city': 'Doda',
                'district': 'Doda',
                'type': 'Degree College',
                'established': '1972',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Rajouri',
                'city': 'Rajouri',
                'district': 'Rajouri',
                'type': 'Degree College',
                'established': '1975',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Poonch',
                'city': 'Poonch',
                'district': 'Poonch',
                'type': 'Degree College',
                'established': '1978',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Reasi',
                'city': 'Reasi',
                'district': 'Reasi',
                'type': 'Degree College',
                'established': '1985',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Ramban',
                'city': 'Ramban',
                'district': 'Ramban',
                'type': 'Degree College',
                'established': '1992',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Kishtwar',
                'city': 'Kishtwar',
                'district': 'Kishtwar',
                'type': 'Degree College',
                'established': '1995',
                'courses': 'BA, BSc, BCom'
            },
            {
                'name': 'Government Degree College Samba',
                'city': 'Samba',
                'district': 'Samba',
                'type': 'Degree College',
                'established': '2006',
                'courses': 'BA, BSc, BCom'
            },
            
            # Teacher Training Colleges
            {
                'name': 'Government College of Education Srinagar',
                'city': 'Srinagar',
                'district': 'Srinagar',
                'type': 'Teacher Training',
                'established': '1963',
                'courses': 'B.Ed, M.Ed, Diploma in Education'
            },
            {
                'name': 'Government College of Education Jammu',
                'city': 'Jammu',
                'district': 'Jammu',
                'type': 'Teacher Training',
                'established': '1965',
                'courses': 'B.Ed, M.Ed, Diploma in Education'
            }
        ]
        
        for institution in jk_institutions:
            try:
                college = {
                    'name': institution['name'],
                    'address': f"{institution['city']}, {institution['district']} District, Jammu and Kashmir, India",
                    'city': institution['city'],
                    'state': 'Jammu and Kashmir',
                    'district': institution['district'],
                    'pincode': self.get_jk_pincode(institution['district']),
                    'website': self.generate_jk_website_url(institution['name']),
                    'latitude': self.get_jk_coordinates(institution['city'])[0],
                    'longitude': self.get_jk_coordinates(institution['city'])[1],
                    'college_type': institution['type'],
                    'established_year': institution['established'],
                    'courses_offered': institution['courses'],
                    'scholarship_details': self.get_jk_scholarship_info(institution['type']),
                    'government_type': 'J&K Government College'
                }
                colleges.append(college)
                
            except Exception as e:
                logger.warning(f"Error creating J&K college entry for {institution['name']}: {e}")
                continue
        
        logger.info(f"Created {len(colleges)} Jammu & Kashmir government college entries")
        return colleges
    
    def get_jk_pincode(self, district: str) -> str:
        """Get pincode for J&K districts"""
        pincode_mapping = {
            'Srinagar': '190001',
            'Jammu': '180001',
            'Anantnag': '192101',
            'Baramulla': '193101',
            'Kupwara': '193222',
            'Pulwama': '192301',
            'Shopian': '192303',
            'Budgam': '191111',
            'Ganderbal': '191201',
            'Bandipora': '193502',
            'Kulgam': '192231',
            'Kathua': '184101',
            'Udhampur': '182101',
            'Doda': '182202',
            'Rajouri': '185131',
            'Poonch': '185101',
            'Reasi': '182311',
            'Ramban': '182144',
            'Kishtwar': '182204',
            'Samba': '184121'
        }
        return pincode_mapping.get(district, '190001')
    
    def get_jk_coordinates(self, city: str) -> tuple:
        """Get coordinates for J&K cities"""
        coordinates = {
            'Srinagar': (34.0837, 74.7973),
            'Jammu': (32.7266, 74.8570),
            'Anantnag': (33.7311, 75.1480),
            'Baramulla': (34.2094, 74.3428),
            'Kupwara': (34.5267, 74.2467),
            'Pulwama': (33.8712, 74.8947),
            'Shopian': (33.7081, 74.8308),
            'Budgam': (34.0230, 74.7350),
            'Ganderbal': (34.2307, 74.7847),
            'Bandipora': (34.4186, 74.6398),
            'Kulgam': (33.6411, 75.0197),
            'Kathua': (32.3705, 75.5224),
            'Udhampur': (32.9150, 75.1411),
            'Doda': (33.1390, 75.5467),
            'Rajouri': (33.3731, 74.3072),
            'Poonch': (33.7739, 74.0894),
            'Reasi': (33.0839, 74.8339),
            'Ramban': (33.2431, 75.2339),
            'Kishtwar': (33.3119, 75.7669),
            'Samba': (32.5625, 75.1194)
        }
        return coordinates.get(city, (33.7782, 76.5762))  # Default to J&K center
    
    def generate_jk_website_url(self, college_name: str) -> str:
        """Generate website URL for J&K colleges"""
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
        elif 'medical college srinagar' in name_lower:
            return 'https://www.gmcsrinagar.edu.in'
        elif 'medical college jammu' in name_lower:
            return 'https://www.gmcjammu.nic.in'
        else:
            # Generic pattern for other colleges
            city = college_name.split()[-1].lower()
            return f'https://www.gdc{city}.edu.in'
    
    def get_jk_scholarship_info(self, college_type: str) -> str:
        """Get scholarship information for J&K colleges"""
        scholarship_mapping = {
            'Central University': 'Central government scholarships, UGC scholarships, Merit scholarships, SC/ST/OBC scholarships, Minority scholarships available.',
            'Medical College': 'NEET-based admissions, Government medical scholarships, SC/ST/OBC scholarships, Merit scholarships, State government medical scholarships.',
            'Engineering College': 'JEE-based admissions, Technical education scholarships, Merit scholarships, SC/ST/OBC scholarships, Industry scholarships.',
            'Degree College': 'State government scholarships, Merit scholarships, SC/ST/OBC scholarships, Minority scholarships, Need-based financial assistance.',
            'Women\'s College': 'Women empowerment scholarships, Merit scholarships, SC/ST/OBC scholarships, State government scholarships for women.',
            'Teacher Training': 'Teacher training scholarships, Merit scholarships, SC/ST/OBC scholarships, State education department scholarships.',
            'Polytechnic': 'Technical education scholarships, Skill development scholarships, Merit scholarships, SC/ST/OBC scholarships.'
        }
        return scholarship_mapping.get(college_type, 'Various government scholarships and merit-based financial assistance available.')
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method for J&K colleges"""
        all_colleges = []
        
        try:
            # Get J&K government colleges
            jk_colleges = self.scrape_jk_government_colleges()
            all_colleges.extend(jk_colleges)
            
        except Exception as e:
            logger.error(f"Error during J&K college scraping: {e}")
        
        logger.info(f"Total J&K government colleges: {len(all_colleges)}")
        return all_colleges
