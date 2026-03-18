"""
Utility functions for Selenium web scraping
"""
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_driver(headless=False):
    """
    Initialize Chrome WebDriver
    
    Args:
        headless (bool): Run browser in headless mode (no GUI)
    
    Returns:
        WebDriver: Configured Chrome WebDriver instance
    """
    options = webdriver.ChromeOptions()
    
    if headless:
        options.add_argument('--headless')
    
    # Common options
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    try:
        driver = webdriver.Chrome(options=options)
        logger.info("WebDriver initialized successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {str(e)}")
        logger.error("Make sure ChromeDriver is installed and in PATH")
        raise


def wait_for_element(driver, by, value, timeout=10):
    """
    Wait for an element to be present in the DOM
    
    Args:
        driver: WebDriver instance
        by: By locator type (e.g., By.CSS_SELECTOR)
        value: Locator value
        timeout: Maximum wait time in seconds
    
    Returns:
        WebElement or None: The element if found, None otherwise
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        logger.debug(f"Element found: {value}")
        return element
    except TimeoutException:
        logger.warning(f"Timeout waiting for element: {value}")
        return None


def wait_for_clickable(driver, by, value, timeout=10):
    """
    Wait for an element to be clickable
    
    Args:
        driver: WebDriver instance
        by: By locator type
        value: Locator value
        timeout: Maximum wait time in seconds
    
    Returns:
        WebElement or None: The element if found and clickable, None otherwise
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        logger.debug(f"Element clickable: {value}")
        return element
    except TimeoutException:
        logger.warning(f"Timeout waiting for clickable element: {value}")
        return None


def safe_click(driver, element, retries=3):
    """
    Safely click an element with retry logic
    
    Args:
        driver: WebDriver instance
        element: WebElement to click
        retries: Number of retry attempts
    
    Returns:
        bool: True if click succeeded, False otherwise
    """
    for attempt in range(retries):
        try:
            element.click()
            logger.debug("Element clicked successfully")
            return True
        except StaleElementReferenceException:
            logger.warning(f"Stale element reference (attempt {attempt + 1}/{retries})")
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"Click failed (attempt {attempt + 1}/{retries}): {str(e)}")
            time.sleep(0.5)
    
    return False


def scroll_to_bottom(driver, pause_time=2):
    """
    Scroll to the bottom of the page
    
    Args:
        driver: WebDriver instance
        pause_time: Time to pause after each scroll in seconds
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        
        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        
        last_height = new_height
    
    logger.info("Reached bottom of page")


def extract_text(element, selector=None):
    """
    Safely extract text from an element
    
    Args:
        element: WebElement or WebDriver
        selector: CSS selector (optional, for finding child element)
    
    Returns:
        str: Extracted text or empty string
    """
    try:
        if selector:
            el = element.find_element(By.CSS_SELECTOR, selector)
        else:
            el = element
        
        return el.text.strip()
    except (NoSuchElementException, AttributeError):
        return ""


def extract_attribute(element, attribute, selector=None):
    """
    Safely extract an attribute from an element
    
    Args:
        element: WebElement or WebDriver
        attribute: Attribute name (e.g., 'href')
        selector: CSS selector (optional, for finding child element)
    
    Returns:
        str: Attribute value or empty string
    """
    try:
        if selector:
            el = element.find_element(By.CSS_SELECTOR, selector)
        else:
            el = element
        
        return el.get_attribute(attribute) or ""
    except (NoSuchElementException, AttributeError):
        return ""


def respectful_delay():
    """
    Add a respectful delay between requests to avoid aggressive scraping
    Uses a random delay between 2-5 seconds
    """
    import random
    delay = random.uniform(2, 5)
    time.sleep(delay)


class ScrapingSession:
    """Context manager for managing Selenium sessions"""
    
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
    
    def __enter__(self):
        self.driver = init_driver(headless=self.headless)
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
        
        if exc_type is not None:
            logger.error(f"Error occurred: {exc_val}")
            return False
        
        return True
