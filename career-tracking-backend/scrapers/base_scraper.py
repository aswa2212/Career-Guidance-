import requests
import time
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all scrapers with common functionality"""
    
    def __init__(self, delay_range: tuple = (1, 3), timeout: int = 30):
        self.delay_range = delay_range
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set common headers to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_page(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with retry logic"""
        for attempt in range(retries):
            try:
                logger.info(f"Fetching: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # Random delay to be respectful
                time.sleep(random.uniform(*self.delay_range))
                
                return BeautifulSoup(response.content, 'html.parser')
                
            except requests.RequestException as e:
                logger.warning(f"Error fetching {url}: {e}")
                if attempt == retries - 1:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
                time.sleep(random.uniform(2, 5))  # Longer delay on error
        
        return None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        return ' '.join(text.strip().split())
    
    def safe_extract(self, element, selector: str, attribute: str = None) -> str:
        """Safely extract text or attribute from element"""
        try:
            found = element.select_one(selector)
            if found:
                if attribute:
                    return found.get(attribute, "").strip()
                return self.clean_text(found.get_text())
            return ""
        except Exception as e:
            logger.warning(f"Error extracting {selector}: {e}")
            return ""
    
    def save_to_json(self, data: List[Dict], filename: str):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(data)} items to {filename}")
        except Exception as e:
            logger.error(f"Error saving to {filename}: {e}")
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """Abstract method to be implemented by specific scrapers"""
        pass
    
    def __del__(self):
        """Clean up session"""
        if hasattr(self, 'session'):
            self.session.close()
