"""
Main orchestration script for Selenium web scraping
Runs all job board scrapers and combines results
"""
import logging
import os
import csv
from datetime import datetime
from greenhouse_scraper import run_greenhouse_scraper
from lever_scraper import run_lever_scraper
from ashby_scraper import run_ashby_scraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobLinkAggregator:
    """Combine job links from multiple sources"""
    
    def __init__(self, output_dir='../data/raw'):
        self.output_dir = output_dir
        self.all_links = {}
        os.makedirs(output_dir, exist_ok=True)
    
    def run_all_scrapers(self, headless=False):
        """
        Run all job board scrapers
        
        Args:
            headless (bool): Run browsers in headless mode
        """
        scrapers = [
            ('Greenhouse', run_greenhouse_scraper),
            ('Lever', run_lever_scraper),
            ('Ashby', run_ashby_scraper)
        ]
        
        for name, scraper_func in scrapers:
            try:
                logger.info(f"\n{'='*60}")
                logger.info(f"Starting {name} scraper...")
                logger.info(f"{'='*60}")
                
                output_file = os.path.join(
                    self.output_dir,
                    f'{name.lower()}_links.csv'
                )
                
                links = scraper_func(output_file=output_file, headless=headless)
                self.all_links[name.lower()] = links
                
                logger.info(f"✓ {name} scraper completed: {len(links)} links found")
            
            except Exception as e:
                logger.error(f"✗ {name} scraper failed: {str(e)}")
    
    def combine_links(self, output_file=None):
        """
        Combine all job links from different sources
        
        Args:
            output_file (str): Path to save combined links
        
        Returns:
            dict: Statistics about combined links
        """
        if output_file is None:
            output_file = os.path.join(self.output_dir, 'job_links.csv')
        
        all_unique_links = set()
        source_counts = {}
        
        # Combine all links
        for source, links in self.all_links.items():
            source_counts[source] = len(links)
            all_unique_links.update(links)
        
        # Save combined CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'source', 'added_at'])
            writer.writeheader()
            
            for source, links in self.all_links.items():
                for link in links:
                    writer.writerow({
                        'url': link,
                        'source': source,
                        'added_at': datetime.now().isoformat()
                    })
        
        logger.info(f"\n{'='*60}")
        logger.info("SUMMARY OF JOB LINK COLLECTION")
        logger.info(f"{'='*60}")
        
        for source, count in source_counts.items():
            logger.info(f"{source:.<20} {count:>5} links")
        
        logger.info(f"{'-'*60}")
        logger.info(f"{'Total unique':.<20} {len(all_unique_links):>5} links")
        logger.info(f"{'='*60}\n")
        
        return {
            'total_links': len(all_unique_links),
            'source_breakdown': source_counts,
            'output_file': output_file
        }


def main():
    """Main entry point"""
    logger.info("\n" + "="*60)
    logger.info("JOB LISTING SELENIUM SCRAPER - MAIN")
    logger.info("="*60)
    
    aggregator = JobLinkAggregator()
    
    # Run all scrapers
    aggregator.run_all_scrapers(headless=False)
    
    # Combine results
    stats = aggregator.combine_links()
    
    logger.info(f"Job links saved to: {stats['output_file']}")
    logger.info("Ready for Scrapy spider to extract detailed job data!")
    
    return stats


if __name__ == '__main__':
    main()
