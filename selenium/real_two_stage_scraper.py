"""
Real Job Board Scraper - Two-stage scraping
Stage 1: Scrape job listing pages to collect job URLs
Stage 2: Follow each job URL to extract detailed information

Targets:
- https://www.greenhouse.com/careers/opportunities
- https://www.ashbyhq.com/careers
- https://jobs.punjab.gov.pk/new_recruit/jobs
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import csv
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealJobBoardScraper:
    """Two-stage scraper: Stage 1 collect URLs, Stage 2 get details"""
    
    def __init__(self):
        self.driver = None
        self.job_urls = set()  # Stage 1: Collect job URLs
        self.job_details = []  # Stage 2: Detailed job information
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("✓ Chrome WebDriver initialized")
        except Exception as e:
            logger.error(f"Failed to initialize driver: {e}")
            logger.info("Make sure you have Chrome browser installed")
    
    # ============================================================
    # STAGE 1: COLLECT JOB URLs FROM LISTING PAGES
    # ============================================================
    
    def stage1_greenhouse_urls(self):
        """Stage 1: Extract job URLs from Greenhouse careers page"""
        logger.info("\n" + "="*70)
        logger.info("STAGE 1: GREENHOUSE - Collecting Job URLs")
        logger.info("="*70)
        
        if not self.driver:
            return
        
        try:
            url = "https://www.greenhouse.com/careers/opportunities"
            logger.info(f"Loading: {url}")
            self.driver.get(url)
            time.sleep(4)
            
            # Scroll to load all jobs
            logger.info("Scrolling to load all job listings...")
            for _ in range(5):
                self.driver.execute_script("window.scrollBy(0, window.innerHeight)")
                time.sleep(2)
            
            # Find all job listing links
            job_links = self.driver.find_elements(
                By.CSS_SELECTOR, 
                "a[href*='greenhouse'], a[href*='job']"
            )
            
            logger.info(f"Found {len(job_links)} potential job links")
            
            for link in job_links:
                try:
                    href = link.get_attribute('href')
                    title = link.text.strip()
                    
                    # Filter for actual job URLs
                    if href and ('job' in href.lower() or 'greenhouse' in href.lower()):
                        self.job_urls.add(href)
                        logger.info(f"  ✓ {title[:50]}")
                except:
                    continue
            
            logger.info(f"\n✓ Greenhouse: Collected {len(self.job_urls)} unique job URLs")
        
        except Exception as e:
            logger.error(f"Error in Greenhouse Stage 1: {e}")
    
    def stage1_ashby_urls(self):
        """Stage 1: Extract job URLs from Ashby careers page"""
        logger.info("\n" + "="*70)
        logger.info("STAGE 1: ASHBY - Collecting Job URLs")
        logger.info("="*70)
        
        if not self.driver:
            return
        
        try:
            url = "https://www.ashbyhq.com/careers"
            logger.info(f"Loading: {url}")
            self.driver.get(url)
            time.sleep(4)
            
            # Scroll to load jobs
            logger.info("Scrolling to load all job listings...")
            for _ in range(5):
                self.driver.execute_script("window.scrollBy(0, window.innerHeight)")
                time.sleep(2)
            
            # Find job links
            job_links = self.driver.find_elements(
                By.CSS_SELECTOR,
                "a[href*='job'], a[href*='careers']"
            )
            
            logger.info(f"Found {len(job_links)} potential job links")
            
            for link in job_links:
                try:
                    href = link.get_attribute('href')
                    title = link.text.strip()
                    
                    if href and 'job' in href.lower():
                        # Convert relative to absolute URLs
                        if href.startswith('/'):
                            href = urljoin("https://www.ashbyhq.com", href)
                        
                        self.job_urls.add(href)
                        logger.info(f"  ✓ {title[:50]}")
                except:
                    continue
            
            logger.info(f"\n✓ Ashby: Collected {len(self.job_urls)} unique job URLs")
        
        except Exception as e:
            logger.error(f"Error in Ashby Stage 1: {e}")
    
    def stage1_punjab_jobs_urls(self):
        """Stage 1: Extract job URLs from Punjab Jobs Portal"""
        logger.info("\n" + "="*70)
        logger.info("STAGE 1: PUNJAB JOBS PORTAL - Collecting Job URLs")
        logger.info("="*70)
        
        if not self.driver:
            return
        
        try:
            url = "https://jobs.punjab.gov.pk/new_recruit/jobs"
            logger.info(f"Loading: {url}")
            self.driver.get(url)
            time.sleep(4)
            
            # Scroll to load all jobs
            logger.info("Scrolling to load all job listings (77 total)...")
            for _ in range(8):
                self.driver.execute_script("window.scrollBy(0, window.innerHeight)")
                time.sleep(2)
            
            # Find all job listing links
            job_links = self.driver.find_elements(
                By.CSS_SELECTOR,
                "a[href*='job'], a[href*='view'], tr td a"
            )
            
            logger.info(f"Found {len(job_links)} potential job links")
            
            for link in job_links:
                try:
                    href = link.get_attribute('href')
                    title = link.text.strip()
                    
                    if href and len(title) > 3:  # Filter out empty links
                        # Convert relative to absolute URLs
                        if href.startswith('/'):
                            href = urljoin("https://jobs.punjab.gov.pk", href)
                        
                        self.job_urls.add(href)
                        logger.info(f"  ✓ {title[:60]}")
                except:
                    continue
            
            logger.info(f"\n✓ Punjab Jobs Portal: Collected {len(self.job_urls)} unique job URLs")
        
        except Exception as e:
            logger.error(f"Error in Punjab Jobs Portal Stage 1: {e}")
    
    # ============================================================
    # STAGE 2: EXTRACT DETAILED JOB INFORMATION FROM EACH URL
    # ============================================================
    
    def stage2_extract_details(self):
        """Stage 2: Visit each job URL and extract detailed information"""
        logger.info("\n" + "="*70)
        logger.info("STAGE 2: EXTRACTING JOB DETAILS FROM EACH URL")
        logger.info("="*70)
        
        if not self.driver or not self.job_urls:
            logger.warning("No job URLs to process!")
            return
        
        logger.info(f"Processing {len(self.job_urls)} job URLs...")
        
        for idx, job_url in enumerate(list(self.job_urls)[:100], 1):  # Limit to 100
            try:
                logger.info(f"\n[{idx}] Fetching: {job_url[:70]}")
                self.driver.get(job_url)
                time.sleep(2)
                
                # Extract job details
                job_title = self.extract_text(By.CSS_SELECTOR, "h1, h2, .title, [class*='title']", "Job Title")
                company = self.extract_text(By.CSS_SELECTOR, ".company, [class*='company']", "Unknown Company")
                location = self.extract_text(By.CSS_SELECTOR, ".location, [class*='location']", "Not Specified")
                description = self.extract_text(By.CSS_SELECTOR, ".description, [class*='description'], p", "N/A")
                
                job_data = {
                    'job_title': job_title[:100],
                    'company_name': company[:50],
                    'location': location[:50],
                    'job_url': job_url,
                    'job_description': description[:200],
                    'source': self.get_source(job_url),
                    'posted_date': datetime.now().strftime('%Y-%m-%d')
                }
                
                self.job_details.append(job_data)
                logger.info(f"  ✓ {job_title[:50]} | {company[:30]}")
            
            except StaleElementReferenceException:
                logger.warning(f"  ⚠ Stale element (page changed), skipping...")
                continue
            except Exception as e:
                logger.debug(f"  Error processing {job_url[:60]}: {str(e)[:50]}")
                # Still save URL without details
                self.job_details.append({
                    'job_title': 'Job Posting',
                    'company_name': 'Unknown',
                    'location': 'Not Specified',
                    'job_url': job_url,
                    'job_description': 'Details not available',
                    'source': self.get_source(job_url),
                    'posted_date': datetime.now().strftime('%Y-%m-%d')
                })
                continue
        
        logger.info(f"\n✓ Extracted details from {len(self.job_details)} jobs")
    
    def extract_text(self, by, selector, default="N/A"):
        """Helper: Extract text from element, return default if not found"""
        try:
            element = self.driver.find_element(by, selector)
            text = element.text.strip()
            return text if text else default
        except:
            return default
    
    def get_source(self, url):
        """Determine job board source from URL"""
        if 'greenhouse' in url.lower():
            return 'greenhouse'
        elif 'ashby' in url.lower():
            return 'ashby'
        elif 'punjab' in url.lower():
            return 'punjab'
        else:
            return 'other'
    
    def save_to_csv(self):
        """Save collected job data to CSV"""
        if not self.job_details:
            logger.warning("No job details to save!")
            return
        
        try:
            filename = '../data/raw/real_job_links.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['job_title', 'company_name', 'location', 'job_url', 'job_description', 'source', 'posted_date']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.job_details)
            
            logger.info(f"\n✓ Saved {len(self.job_details)} real job listings to: {filename}")
        
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
    
    def run(self):
        """Execute full two-stage scraping process"""
        logger.info("\n" + "="*70)
        logger.info("REAL JOB BOARD SCRAPER - TWO STAGE PROCESS")
        logger.info("="*70)
        
        if not self.driver:
            logger.error("Failed to initialize WebDriver!")
            return
        
        try:
            # STAGE 1: Collect job URLs from listing pages
            logger.info("\n>>> STAGE 1: COLLECTING JOB URLs <<<")
            self.stage1_greenhouse_urls()
            time.sleep(2)
            
            self.stage1_ashby_urls()
            time.sleep(2)
            
            self.stage1_punjab_jobs_urls()
            time.sleep(2)
            
            logger.info(f"\n>>> TOTAL JOB URLs COLLECTED: {len(self.job_urls)} <<<\n")
            
            # STAGE 2: Extract detailed information from each job URL
            logger.info("\n>>> STAGE 2: EXTRACTING JOB DETAILS <<<")
            self.stage2_extract_details()
            
            # Save results
            logger.info("\n>>> SAVING RESULTS <<<")
            self.save_to_csv()
            
            logger.info("\n" + "="*70)
            logger.info(f"✓ SCRAPING COMPLETE")
            logger.info(f"✓ Total job URLs found: {len(self.job_urls)}")
            logger.info(f"✓ Total jobs with details: {len(self.job_details)}")
            logger.info("="*70 + "\n")
        
        finally:
            self.close()


if __name__ == '__main__':
    scraper = RealJobBoardScraper()
    scraper.run()
