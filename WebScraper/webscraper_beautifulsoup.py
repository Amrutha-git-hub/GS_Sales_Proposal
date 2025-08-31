import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import time
import json
import concurrent.futures

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

    def trace_redirect(self, url):
        try:
            response = self.session.head(url, allow_redirects=True, timeout=10)
            print("Redirect chain:")
            for resp in response.history:
                print(f"{resp.status_code} → {resp.url}")
            print(f"Final URL: {response.url}")
        except Exception as e:
            print(f"Error tracing redirect: {e}")

    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage with redirect handling"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            print(f"[INFO] Final redirected URL: {response.url}")
            print(f"[INFO] Redirect history: {[r.status_code for r in response.history]}")
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"[WARN] Error fetching {url}: {e}")
            return None

    def extract_name(self, soup: BeautifulSoup, url: str) -> str:
        selectors = [
            'h1', '.company-name', '.brand-name', '.site-title', '.logo-text',
            '[class*="company"]', '[class*="brand"]', 'title',
            '.header-title', '.main-title'
        ]
        for selector in selectors:
            for el in soup.select(selector):
                text = el.get_text(strip=True)
                if 2 < len(text) < 100:
                    return text
        domain = urlparse(url).netloc
        return domain.replace('www.', '').replace('.com', '').title()

    def extract_logo(self, soup: BeautifulSoup, base_url: str) -> str:
        selectors = [
            'img[class*="logo"]', '.logo img', '[class*="brand"] img', 'header img',
            '.navbar-brand img', '.site-logo img', '[alt*="logo" i]', '[src*="logo" i]'
        ]
        for selector in selectors:
            for el in soup.select(selector):
                src = el.get('src')
                if src:
                    return urljoin(base_url, src)
        header_imgs = soup.select('header img, .header img, nav img')
        if header_imgs:
            src = header_imgs[0].get('src')
            if src:
                return urljoin(base_url, src)
        return ""

    def extract_description(self, soup: BeautifulSoup) -> str:
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        selectors = [
            '.about-us', '.description', '.company-description', '.intro', '.summary',
            '[class*="about"]', '.hero-text', '.lead', '.tagline', '.subtitle'
        ]
        for selector in selectors:
            for el in soup.select(selector):
                text = el.get_text(strip=True)
                if 50 < len(text) < 500:
                    return text
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if 50 < len(text) < 500:
                return text
        return ""

    def extract_services(self, soup: BeautifulSoup) -> List[str]:
        services = []
        service_selectors = [
            '.services', '.products', '.offerings', '.solutions',
            '[class*="service"]', '[class*="product"]', '.features', '.capabilities'
        ]
        for selector in service_selectors:
            for section in soup.select(selector):
                for item in section.select('li, .item, .service-item, .product-item'):
                    text = item.get_text(strip=True)
                    if 3 < len(text) < 100:
                        services.append(text)
                for heading in section.select('h3, h4, h5, .title, .heading'):
                    text = heading.get_text(strip=True)
                    if 3 < len(text) < 100:
                        services.append(text)
        for item in soup.select('nav a, .menu a, .navigation a'):
            text = item.get_text(strip=True).lower()
            if 3 < len(text) < 50 and text not in ['home', 'about', 'contact', 'blog', 'news', 'careers']:
                services.append(text)
        return list(dict.fromkeys(services))[:10]

    def scrape_website(self, url: str) -> Optional[User]:
        print(f"\n[SCRAPING] {url}")
        soup = self.get_page(url)

        # Retry with www if not successful
        if not soup and 'www.' not in url:
            alt_url = url.replace("https://", "https://www.")
            print(f"[RETRY] Trying with www: {alt_url}")
            soup = self.get_page(alt_url)

        if not soup:
            return None

        try:
            name = self.extract_name(soup, url)
            logo = self.extract_logo(soup, url)
            description = self.extract_description(soup)
            services = self.extract_services(soup)
            return User(name=name, logo=logo, description=description, services=services)
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None

    def scrape_multiple_urls(self, urls: List[str]) -> List[User]:
        users = []
        for url in urls:
            user = self.scrape_website(url)
            if user:
                users.append(user)
            time.sleep(self.delay)
        return users

    def save_to_json(self, users: List[User], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([user.dict() for user in users], f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")

def get_url_details_with_bs4(url: str, timeout: int = 15):
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

