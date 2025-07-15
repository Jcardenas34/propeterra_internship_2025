'''
Script created by Claude Sonnet 4
LLM: Claude

Prompt:
-----------
Act as an expert in web scraping and data collection from the internet.

I believe this webpage is scre-apable by ethical means, 
https://www.properstar.com/mexico/real-estate-agents
Please write a python script that will collect the information of the real estate professionals on this page as well as the subsequent pages on the page list.
I would like the script to return a .json file of the real estate professional's information with the following fields, name, associated company, bio, social network links, languages spoken and agency page. the script might have to  navigate from the original link and links like it to the page of the professional. 

Please think out your answer step by step and ask clarifying questions if you cannot produce a viable script to collect the information. if the page is not scrapble by ethical means please say so. Do not make up any information.

'''
import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from urllib.parse import urljoin, urlparse
import re
from typing import Dict, List, Set, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('properstar_scraper.log'),
        logging.StreamHandler()
    ]
)

class PropertystarAgentScraper:
    def __init__(self, delay: float = 0.5):
        """
        Initialize the scraper with a delay between requests.
        0.5 seconds is a safe, considerate rate for web scraping.
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.properstar.com"
        self.agents_data = []
        self.processed_agents = set()  # Track processed agent URLs to avoid duplicates
        
    def make_request(self, url: str) -> Optional[BeautifulSoup]:
        """Make a request with proper error handling and rate limiting."""
        try:
            time.sleep(self.delay)  # Rate limiting
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None
    
    def find_agent_profile_links(self, listing_page_url: str) -> List[str]:
        """Find all agent profile links from a listing page."""
        soup = self.make_request(listing_page_url)
        if not soup:
            return []
        
        agent_links = set()
        
        # Look for links that go to agent profiles
        # These typically have patterns like /real-estate-agent/agent-name
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            # Look for agent profile links
            if '/real-estate-agent/' in href:
                full_url = urljoin(self.base_url, href)
                agent_links.add(full_url)
            # Also look for links that might contain agent names or IDs
            elif re.search(r'agent|professional|broker', href, re.IGNORECASE):
                full_url = urljoin(self.base_url, href)
                agent_links.add(full_url)
        
        logging.info(f"Found {len(agent_links)} unique agent profile links")
        return list(agent_links)
    
    def get_all_listing_pages(self, base_url: str) -> List[str]:
        """Get all listing pages with pagination."""
        pages = [base_url]
        soup = self.make_request(base_url)
        if not soup:
            return pages
        
        # Look for pagination links
        pagination_selectors = [
            'a[href*="page="]',
            'a[href*="/page/"]',
            '.pagination a',
            '.pager a',
            'nav a[href*="page"]'
        ]
        
        page_numbers = set()
        for selector in pagination_selectors:
            page_links = soup.select(selector)
            for link in page_links:
                href = link.get('href')
                if href:
                    # Extract page number
                    page_match = re.search(r'page[=/](\d+)', href)
                    if page_match:
                        page_numbers.add(int(page_match.group(1)))
        
        # Generate URLs for all pages
        for page_num in sorted(page_numbers):
            if '?' in base_url:
                page_url = f"{base_url}&page={page_num}"
            else:
                page_url = f"{base_url}?page={page_num}"
            if page_url not in pages:
                pages.append(page_url)
        
        logging.info(f"Found {len(pages)} listing pages to process")
        return pages
    
    def extract_agent_profile_info(self, agent_url: str, region: str) -> Optional[Dict]:
        """Extract detailed information from an agent's profile page."""
        if agent_url in self.processed_agents:
            logging.info(f"Skipping already processed agent: {agent_url}")
            return None
        
        soup = self.make_request(agent_url)
        if not soup:
            return None
        
        self.processed_agents.add(agent_url)
        
        agent_data = {
            "name": "",
            "associated_company": "",
            "bio": "",
            "social_network_links": "",
            "languages_spoken": "",
            "agency_page": "",
            "region": region,
            "url": agent_url,
            "email": "",
            "phone": ""
        }
        
        try:
            # Extract name - look for various selectors
            name_selectors = [
                'h1',
                '.agent-name',
                '.profile-name',
                '.agent-title h1',
                '.agent-title h2',
                'h1.title',
                'h2.title'
            ]
            
            for selector in name_selectors:
                name_element = soup.select_one(selector)
                if name_element:
                    name_text = name_element.get_text(strip=True)
                    if name_text and len(name_text) > 2:  # Basic validation
                        agent_data["name"] = name_text
                        break
            
            # Extract company/agency
            company_selectors = [
                '.agent-company',
                '.agency-name',
                '.company-name',
                '.agent-agency',
                'h2:contains("Company")',
                'div:contains("Agency")'
            ]
            
            for selector in company_selectors:
                if ':contains(' in selector:
                    # Handle pseudo-selectors manually
                    elements = soup.find_all(text=re.compile(r'Company|Agency|Brokerage', re.IGNORECASE))
                    for elem in elements:
                        parent = elem.parent
                        if parent:
                            company_text = parent.get_text(strip=True)
                            if company_text and len(company_text) > 2:
                                agent_data["associated_company"] = company_text
                                break
                else:
                    company_element = soup.select_one(selector)
                    if company_element:
                        company_text = company_element.get_text(strip=True)
                        if company_text and len(company_text) > 2:
                            agent_data["associated_company"] = company_text
                            break
            
            # Extract bio/about me
            bio_selectors = [
                '.agent-bio',
                '.agent-description',
                '.about-agent',
                '.profile-description',
                '.agent-about',
                'div[class*="bio"]',
                'div[class*="about"]',
                'div[class*="description"]'
            ]
            
            for selector in bio_selectors:
                bio_element = soup.select_one(selector)
                if bio_element:
                    bio_text = bio_element.get_text(strip=True)
                    if bio_text and len(bio_text) > 20:  # Look for substantial bio text
                        agent_data["bio"] = bio_text
                        break
            
            # If no dedicated bio section, look for longer paragraphs
            if not agent_data["bio"]:
                paragraphs = soup.find_all('p')
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 100:  # Assume longer text is bio
                        agent_data["bio"] = text
                        break
            
            # Extract email
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            page_text = soup.get_text()
            email_matches = re.findall(email_pattern, page_text)
            if email_matches:
                agent_data["email"] = email_matches[0]
            
            # Extract phone
            phone_patterns = [
                r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}'
            ]
            
            for pattern in phone_patterns:
                phone_matches = re.findall(pattern, page_text)
                if phone_matches:
                    agent_data["phone"] = phone_matches[0]
                    break
            
            # Extract social media links
            social_links = []
            social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com']
            
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if any(domain in href for domain in social_domains):
                    social_links.append(href)
            
            agent_data["social_network_links"] = ", ".join(social_links)
            
            # Extract languages
            language_keywords = ['languages', 'idiomas', 'spoken', 'habla']
            for keyword in language_keywords:
                lang_element = soup.find(text=re.compile(keyword, re.IGNORECASE))
                if lang_element:
                    parent = lang_element.parent
                    if parent:
                        lang_text = parent.get_text(strip=True)
                        # Extract languages after the keyword
                        lang_match = re.search(f'{keyword}[:\s]+([^\\n]+)', lang_text, re.IGNORECASE)
                        if lang_match:
                            agent_data["languages_spoken"] = lang_match.group(1).strip()
                            break
            
            # Extract agency page (if different from current URL)
            agency_links = soup.find_all('a', href=True)
            for link in agency_links:
                href = link['href']
                if 'agency' in href or 'company' in href:
                    agent_data["agency_page"] = urljoin(self.base_url, href)
                    break
            
            logging.info(f"Successfully extracted info for: {agent_data['name']}")
            return agent_data
            
        except Exception as e:
            logging.error(f"Error extracting agent info from {agent_url}: {e}")
            return None
    
    def scrape_region_agents(self, region_url: str, region_name: str = None):
        """Scrape all agents from a specific region."""
        if not region_name:
            # Extract region name from URL
            region_name = region_url.split('/')[-2] if region_url.endswith('/') else region_url.split('/')[-1]
            region_name = region_name.replace('-', ' ').replace('real-estate-agents', '').strip().title()
        
        logging.info(f"Starting scrape for region: {region_name}")
        logging.info(f"Region URL: {region_url}")
        
        # Get all listing pages (with pagination)
        listing_pages = self.get_all_listing_pages(region_url)
        
        # Collect all agent profile links from all listing pages
        all_agent_links = []
        for page_url in listing_pages:
            logging.info(f"Finding agent links on: {page_url}")
            agent_links = self.find_agent_profile_links(page_url)
            all_agent_links.extend(agent_links)
        
        # Remove duplicates
        unique_agent_links = list(set(all_agent_links))
        logging.info(f"Found {len(unique_agent_links)} unique agent profiles to scrape")
        
        # Scrape each agent's profile
        for i, agent_url in enumerate(unique_agent_links, 1):
            logging.info(f"Scraping agent {i}/{len(unique_agent_links)}: {agent_url}")
            agent_data = self.extract_agent_profile_info(agent_url, region_name)
            if agent_data:
                self.agents_data.append(agent_data)
        
        logging.info(f"Successfully scraped {len(self.agents_data)} agents from {region_name}")
    
    def save_to_json(self, filename: str = None):
        """Save scraped data to JSON file."""
        if not filename:
            if self.agents_data:
                region = self.agents_data[0]['region'].lower().replace(' ', '_')
                filename = f"{region}_real_estate_agents.json"
            else:
                filename = "real_estate_agents.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.agents_data, f, ensure_ascii=False, indent=2)
            logging.info(f"Data saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving to JSON: {e}")
            return None

def main():
    """Main function to run the scraper."""
    import sys
    
    # Check if URL is provided as command line argument
    if len(sys.argv) > 1:
        region_url = sys.argv[1]
        region_name = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Default to main Mexico page
        region_url = "https://www.properstar.com/mexico/real-estate-agents"
        region_name = "Mexico"
        print("No region URL provided. Using default Mexico page.")
        print("Usage: python properstar_scraper.py <region_url> [region_name]")
        print("Example: python properstar_scraper.py https://www.properstar.com/mexico/playa-del-carmen/real-estate-agents 'Playa del Carmen'")
    
    scraper = PropertystarAgentScraper(delay=0.5)
    
    try:
        scraper.scrape_region_agents(region_url, region_name)
        filename = scraper.save_to_json()
        
        print(f"\nScraping completed!")
        print(f"Found {len(scraper.agents_data)} unique agents.")
        if filename:
            print(f"Data saved to: {filename}")
        
        # Show sample of collected data
        if scraper.agents_data:
            print(f"\nSample agent data:")
            sample = scraper.agents_data[0]
            for key, value in sample.items():
                print(f"  {key}: {value[:100]}..." if len(str(value)) > 100 else f"  {key}: {value}")
        
    except KeyboardInterrupt:
        logging.info("Scraping interrupted by user")
        filename = scraper.save_to_json("real_estate_agents_partial.json")
        print(f"Partial data saved to: {filename}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        if scraper.agents_data:
            filename = scraper.save_to_json("real_estate_agents_error.json")
            print(f"Error recovery - data saved to: {filename}")

if __name__ == "__main__":
    main()