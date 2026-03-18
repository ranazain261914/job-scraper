"""
Scraper for Ashby job boards (ashbyhq.com/careers)
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
    extract_attribute,
    respectful_delay,
    ScrapingSession
)

logger = logging.getLogger(__name__)


class AsbyhrScraper:
    """
    Scraper for Ashby job boards
    Targets: ashbyhq.com/careers
    """
    
    BASE_URLS = {
        'ashby': 'https://www.ashbyhq.com/careers'
    }
    
    SEARCH_QUERIES = [
        "Software Engineer",
        "Data Analyst",
        "Intern",
        "QA Engineer"
    ]
    
    def __init__(self, driver=None):
        """
        Initialize Ashby scraper
        
        Args:
            driver: Selenium WebDriver instance (optional)
        """
        self.driver = driver
        self.job_links = set()
    
    def scrape(self, headless=False):
        """
        Main scraping method for Ashby
        
        Args:
            headless (bool): Run in headless mode
        
        Returns:
            list: Unique job URLs
        """
        with ScrapingSession(headless=headless) as driver:
            self.driver = driver
            
            logger.info("Starting Ashby scraper...")
            
            # Ashby shows all jobs on one page with search/filter
            self._search_and_extract()
            
            return list(self.job_links)
    
    def _search_and_extract(self):
        """
        Search for jobs on Ashby and extract URLs
        """
        try:
            # Navigate to Ashby
            logger.info("Navigating to Ashby job board...")
            self.driver.get(self.BASE_URLS['ashby'])
            
            # Wait for page load and jobs to load
            time.sleep(5)
            
            # Try to scroll to load more jobs
            self._scroll_and_load_jobs()
            
            # Extract all job links from page
            self._extract_job_links()
            
            respectful_delay()
        
        except Exception as e:
            logger.error(f"Error during Ashby scraping: {str(e)}")
    
    def _scroll_and_load_jobs(self):
        """
        Scroll page to load all available jobs
        """
        try:
            logger.info("Scrolling to load all jobs...")
            
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 5
            
            while scroll_attempts < max_scrolls:
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Get new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                
                last_height = new_height
                scroll_attempts += 1
            
            logger.info(f"Finished scrolling after {scroll_attempts} attempts")
        
        except Exception as e:
            logger.warning(f"Error during scrolling: {str(e)}")
    
    def _extract_job_links(self):
        """
        Extract all job links from Ashby job listings
        """
        try:
            # Common Ashby job link selectors
            selectors = [
                'a[href*="/careers/"]',
                '.job-posting > a',
                '[data-testid*="job"] a',
                'a.job-card-link',
                '.posting a'
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
                    if href and ('ashby' in href.lower() or 'job' in href.lower()):
                        # Ensure absolute URL
                        if not href.startswith('http'):
                            href = 'https://www.ashbyhq.com' + href
                        
                        self.job_links.add(href)
                        logger.debug(f"Added job link: {href}")
                
                except Exception as e:
                    logger.debug(f"Error extracting href: {str(e)}")
            
            logger.info(f"Total unique jobs found: {len(self.job_links)}")
        
        except Exception as e:
            logger.error(f"Error extracting job links: {str(e)}")


def run_ashby_scraper(output_file=None, headless=False):
    """
    Run Ashby scraper and save results
    
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
            'ashby_links.csv'
        )
    
    scraper = AsbyhrScraper()
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
                'source': 'ashby',
                'scraped_at': datetime.now().isoformat()
            })
    
    logger.info(f"Saved {len(job_links)} links to {output_file}")
    
    return job_links


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    run_ashby_scraper(headless=False)
