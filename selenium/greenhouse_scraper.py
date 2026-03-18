"""
Scraper for Greenhouse job boards (boards.greenhouse.io)
"""
import logging
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import (
    init_driver,
    wait_for_element,
    wait_for_clickable,
    safe_click,
    scroll_to_bottom,
    extract_text,
    extract_attribute,
    respectful_delay,
    ScrapingSession
)

logger = logging.getLogger(__name__)


class GreenhouseScraper:
    """
    Scraper for Greenhouse job boards
    Targets: boards.greenhouse.io
    """
    
    BASE_URLS = {
        'greenhouse': 'https://boards.greenhouse.io/greenhouse'
    }
    
    SEARCH_QUERIES = [
        "Software Engineer",
        "Data Analyst",
        "Intern",
        "QA Engineer"
    ]
    
    def __init__(self, driver=None):
        """
        Initialize Greenhouse scraper
        
        Args:
            driver: Selenium WebDriver instance (optional)
        """
        self.driver = driver
        self.job_links = set()
        self.session = None
    
    def scrape(self, headless=False):
        """
        Main scraping method
        
        Args:
            headless (bool): Run in headless mode
        
        Returns:
            list: Unique job URLs
        """
        with ScrapingSession(headless=headless) as driver:
            self.driver = driver
            
            logger.info("Starting Greenhouse scraper...")
            
            for query in self.SEARCH_QUERIES:
                try:
                    self._search_and_extract(query)
                except Exception as e:
                    logger.error(f"Error scraping query '{query}': {str(e)}")
            
            return list(self.job_links)
    
    def _search_and_extract(self, query):
        """
        Search for jobs and extract URLs
        
        Args:
            query (str): Search query (e.g., "Software Engineer")
        """
        try:
            # Navigate to Greenhouse job board
            logger.info(f"Navigating to Greenhouse board...")
            self.driver.get(self.BASE_URLS['greenhouse'])
            
            # Wait for page load
            time.sleep(3)
            
            # Find search input
            search_input = wait_for_element(
                self.driver,
                By.CSS_SELECTOR,
                'input[placeholder*="Search"], input[type="search"]',
                timeout=10
            )
            
            if not search_input:
                logger.warning("Search input not found, trying alternative selectors")
                search_input = wait_for_element(
                    self.driver,
                    By.CSS_SELECTOR,
                    'input[class*="search"]',
                    timeout=5
                )
            
            if search_input:
                # Clear and type search query
                search_input.clear()
                search_input.send_keys(query)
                search_input.send_keys(Keys.RETURN)
                
                logger.info(f"Searching for: {query}")
                
                # Wait for results
                time.sleep(3)
                
                # Extract job links from results
                self._extract_job_links()
                
                respectful_delay()
            else:
                logger.warning("Could not find search input on Greenhouse board")
        
        except Exception as e:
            logger.error(f"Error during search for '{query}': {str(e)}")
    
    def _extract_job_links(self):
        """Extract all job links from current page"""
        try:
            # Common Greenhouse job link selectors
            selectors = [
                'a[href*="/jobs/"]',
                '.job-title > a',
                'a[data-job-id]',
                '.job-link'
            ]
            
            links = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    links.extend(elements)
                except:
                    pass
            
            # Extract href attributes
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href and 'greenhouse' in href and 'job' in href.lower():
                        # Ensure absolute URL
                        if not href.startswith('http'):
                            href = 'https://boards.greenhouse.io' + href
                        
                        self.job_links.add(href)
                        logger.debug(f"Added job link: {href}")
                
                except Exception as e:
                    logger.debug(f"Error extracting href: {str(e)}")
            
            logger.info(f"Total unique jobs found so far: {len(self.job_links)}")
        
        except Exception as e:
            logger.error(f"Error extracting job links: {str(e)}")


def run_greenhouse_scraper(output_file=None, headless=False):
    """
    Run Greenhouse scraper and save results
    
    Args:
        output_file (str): Path to save job links CSV
        headless (bool): Run in headless mode
    
    Returns:
        list: Job URLs
    """
    import os
    from datetime import datetime
    
    if output_file is None:
        output_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            'raw',
            'greenhouse_links.csv'
        )
    
    scraper = GreenhouseScraper()
    job_links = scraper.scrape(headless=headless)
    
    logger.info(f"Found {len(job_links)} unique job links")
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'source', 'scraped_at'])
        writer.writeheader()
        
        for url in job_links:
            writer.writerow({
                'url': url,
                'source': 'greenhouse',
                'scraped_at': datetime.now().isoformat()
            })
    
    logger.info(f"Saved {len(job_links)} links to {output_file}")
    
    return job_links


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    run_greenhouse_scraper(headless=False)
