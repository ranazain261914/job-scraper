"""
Scraper for Lever job boards (jobs.lever.co)
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
    extract_attribute,
    respectful_delay,
    ScrapingSession
)

logger = logging.getLogger(__name__)


class LeverScraper:
    """
    Scraper for Lever job boards
    Targets: jobs.lever.co
    """
    
    BASE_URLS = {
        'lever': 'https://jobs.lever.co'
    }
    
    SEARCH_QUERIES = [
        "Software Engineer",
        "Data Analyst",
        "Intern",
        "QA Engineer"
    ]
    
    def __init__(self, driver=None):
        """
        Initialize Lever scraper
        
        Args:
            driver: Selenium WebDriver instance (optional)
        """
        self.driver = driver
        self.job_links = set()
    
    def scrape(self, headless=False):
        """
        Main scraping method for Lever
        
        Args:
            headless (bool): Run in headless mode
        
        Returns:
            list: Unique job URLs
        """
        with ScrapingSession(headless=headless) as driver:
            self.driver = driver
            
            logger.info("Starting Lever scraper...")
            
            for query in self.SEARCH_QUERIES:
                try:
                    self._search_and_extract(query)
                except Exception as e:
                    logger.error(f"Error scraping query '{query}': {str(e)}")
            
            return list(self.job_links)
    
    def _search_and_extract(self, query):
        """
        Search for jobs on Lever and extract URLs
        
        Args:
            query (str): Search query (e.g., "Software Engineer")
        """
        try:
            # Navigate to Lever
            logger.info(f"Navigating to Lever job board...")
            self.driver.get(self.BASE_URLS['lever'])
            
            # Wait for page load
            time.sleep(3)
            
            # Look for search functionality
            # Lever uses different structures for different companies
            search_input = wait_for_element(
                self.driver,
                By.CSS_SELECTOR,
                'input[placeholder*="Search"], input[type="search"], .search-input',
                timeout=10
            )
            
            if search_input:
                search_input.clear()
                search_input.send_keys(query)
                search_input.send_keys(Keys.RETURN)
                
                logger.info(f"Searching for: {query}")
                time.sleep(3)
            else:
                logger.info(f"No search found, browsing all jobs")
            
            # Extract job listings
            self._extract_job_links()
            
            respectful_delay()
        
        except Exception as e:
            logger.error(f"Error during search for '{query}': {str(e)}")
    
    def _extract_job_links(self):
        """
        Extract all job links from Lever job listings page
        """
        try:
            # Common Lever job link selectors
            selectors = [
                'a.posting-title',
                'a[href*="/jobs/"]',
                '.posting > a',
                'a[data-posting-id]',
                '.leverage-posting-item a'
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
                    if href and 'lever.co' in href and 'job' in href.lower():
                        # Ensure absolute URL
                        if not href.startswith('http'):
                            href = 'https://jobs.lever.co' + href
                        
                        self.job_links.add(href)
                        logger.debug(f"Added job link: {href}")
                
                except Exception as e:
                    logger.debug(f"Error extracting href: {str(e)}")
            
            logger.info(f"Total unique jobs found so far: {len(self.job_links)}")
        
        except Exception as e:
            logger.error(f"Error extracting job links: {str(e)}")


def run_lever_scraper(output_file=None, headless=False):
    """
    Run Lever scraper and save results
    
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
            'lever_links.csv'
        )
    
    scraper = LeverScraper()
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
                'source': 'lever',
                'scraped_at': datetime.now().isoformat()
            })
    
    logger.info(f"Saved {len(job_links)} links to {output_file}")
    
    return job_links


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    run_lever_scraper(headless=False)
