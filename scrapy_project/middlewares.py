"""
Scrapy middlewares for job scraping
"""
import logging

logger = logging.getLogger(__name__)


class JobsSpiderMiddleware:
    """Spider middleware for handling requests/responses"""
    
    def process_spider_input(self, response, spider):
        """Called for each response processed by the spider"""
        return None
    
    def process_spider_output(self, response, result, spider):
        """Called with the results returned from the Spider"""
        for i in result:
            yield i
    
    def process_spider_exception(self, response, exception, spider):
        """Called if the spider or process_spider_input() raises an exception"""
        logger.error(f"Spider error: {exception}")
        pass


class JobsDownloaderMiddleware:
    """Downloader middleware for handling requests/responses"""
    
    def process_request(self, request, spider):
        """Called for each request sent to the downloader"""
        # Set a reasonable user agent
        request.headers.setdefault(
            'User-Agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        return None
    
    def process_response(self, request, response, spider):
        """Called with the response returned from the downloader"""
        return response
    
    def process_exception(self, request, exception, spider):
        """Called when a download error or any other error occurred"""
        logger.warning(f"Request error for {request.url}: {exception}")
        pass
