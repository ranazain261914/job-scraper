"""
Selenium web scraping module for job boards
"""

__version__ = '1.0.0'
__author__ = 'Job Scraper Team'

from .greenhouse_scraper import GreenhouseScraper, run_greenhouse_scraper
from .lever_scraper import LeverScraper, run_lever_scraper
from .ashby_scraper import AsbyhrScraper, run_ashby_scraper
from .utils import (
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

__all__ = [
    'GreenhouseScraper',
    'LeverScraper',
    'AsbyhrScraper',
    'init_driver',
    'wait_for_element',
    'wait_for_clickable',
    'safe_click',
    'scroll_to_bottom',
    'extract_text',
    'extract_attribute',
    'respectful_delay',
    'ScrapingSession',
    'run_greenhouse_scraper',
    'run_lever_scraper',
    'run_ashby_scraper',
]
