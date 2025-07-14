import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
import re
import json
from urllib.parse import urljoin, urlparse
import time
from dataclasses import dataclass

class User(BaseModel):
    name: str
    logo: str
    description: str
    services: List[str]

class WebScraper:
    def __init__(self, delay: float = 1.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = delay
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company/user name from various sources"""
        selectors = [
            'h1',
            '.company-name',
            '.brand-name',
            '.site-title',
            '.logo-text',
            '[class*="company"]',
            '[class*="brand"]',
            'title',
            '.header-title',
            '.main-title'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 2 and len(text) < 100:
                    return text
        
        # Fallback to domain name
        domain = urlparse(url).netloc
        return domain.replace('www.', '').replace('.com', '').title()
    
    def extract_logo(self, soup: BeautifulSoup, base_url: str) -> str:
        """Extract logo URL from various sources"""
        selectors = [
            'img[class*="logo"]',
            '.logo img',
            '[class*="brand"] img',
            'header img',
            '.navbar-brand img',
            '.site-logo img',
            '[alt*="logo" i]',
            '[src*="logo" i]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                src = element.get('src')
                if src:
                    return urljoin(base_url, src)
        
        # Look for any prominent image in header
        header_imgs = soup.select('header img, .header img, nav img')
        if header_imgs:
            src = header_imgs[0].get('src')
            if src:
                return urljoin(base_url, src)
        
        return ""
    
    def extract_description(self, soup: BeautifulSoup) -> str:
        """Extract company description from various sources"""
        # Check meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # Look for about/description sections
        selectors = [
            '.about-us',
            '.description',
            '.company-description',
            '.intro',
            '.summary',
            '[class*="about"]',
            '.hero-text',
            '.lead',
            '.tagline',
            '.subtitle'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 50 and len(text) < 500:
                    return text
        
        # Look for first substantial paragraph
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 50 and len(text) < 500:
                return text
        
        return ""
    
    def extract_services(self, soup: BeautifulSoup) -> List[str]:
        """Extract services/products from various sources"""
        services = []
        
        # Look for services sections
        service_selectors = [
            '.services',
            '.products',
            '.offerings',
            '.solutions',
            '[class*="service"]',
            '[class*="product"]',
            '.features',
            '.capabilities'
        ]
        
        for selector in service_selectors:
            sections = soup.select(selector)
            for section in sections:
                # Extract from list items
                items = section.select('li, .item, .service-item, .product-item')
                for item in items:
                    text = item.get_text(strip=True)
                    if text and len(text) > 3 and len(text) < 100:
                        services.append(text)
                
                # Extract from headings
                headings = section.select('h3, h4, h5, .title, .heading')
                for heading in headings:
                    text = heading.get_text(strip=True)
                    if text and len(text) > 3 and len(text) < 100:
                        services.append(text)
        
        # Look for navigation menu items (potential services)
        nav_items = soup.select('nav a, .menu a, .navigation a')
        for item in nav_items:
            text = item.get_text(strip=True)
            if text and len(text) > 3 and len(text) < 50:
                # Filter out common navigation items
                if text.lower() not in ['home', 'about', 'contact', 'blog', 'news', 'careers']:
                    services.append(text)
        
        # Remove duplicates and clean up
        services = list(dict.fromkeys(services))  # Remove duplicates while preserving order
        return services[:10]  # Limit to top 10 services
    
    def scrape_website(self, url: str) -> Optional[User]:
        """Main method to scrape a website and return User object"""
        print(f"Scraping: {url}")
        
        soup = self.get_page(url)
        if not soup:
            return None
        
        try:
            name = self.extract_name(soup, url)
            logo = self.extract_logo(soup, url)
            description = self.extract_description(soup)
            services = self.extract_services(soup)
            
            user = User(
                name=name,
                logo=logo,
                description=description,
                services=services
            )
            
            return user
            
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None
    
    def scrape_multiple_urls(self, urls: List[str]) -> List[User]:
        """Scrape multiple URLs and return list of User objects"""
        users = []
        
        for url in urls:
            user = self.scrape_website(url)
            if user:
                users.append(user)
            time.sleep(self.delay)  # Be respectful to servers
        
        return users
    
    def save_to_json(self, users: List[User], filename: str):
        """Save scraped data to JSON file"""
        data = [user.dict() for user in users]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")

import concurrent.futures

def get_url_details_without_ai(url: str, timeout: int = 15):
    def scrape():
        try:
            scraper = WebScraper(delay=1.0)
            return scraper.scrape_website(url)
        except Exception as e:
            return f"Scraping error: {e}"

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(scrape)
            return future.result(timeout=timeout)
    except concurrent.futures.TimeoutError:
        return "Timeout Error: Scraping exceeded 15 seconds."
    except Exception as e:
        return f"General Error: {e}"

