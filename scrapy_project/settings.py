# Scrapy settings for jobs_spider project

BOT_NAME = 'jobs_spider'

SPIDER_MODULES = ['jobs_spider.spiders']
NEWSPIDER_MODULE = 'jobs_spider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 4
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Override the default user agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Obey these hosts
#ALLOWED_DOMAINS = ['jobs.lever.co', 'boards.greenhouse.io', 'ashbyhq.com']

# Configure pipelines
ITEM_PIPELINES = {
    'jobs_spider.pipelines.JobsPipeline': 300,
    'jobs_spider.pipelines.DuplicateRemovalPipeline': 100,
    'jobs_spider.pipelines.DataCleaningPipeline': 200,
    'jobs_spider.pipelines.CsvExportPipeline': 400,
    'jobs_spider.pipelines.JsonExportPipeline': 500,
}

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [400, 404, 410, 500, 502, 503, 504]

# Configure logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# Retry settings
RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Timeout settings
DOWNLOAD_TIMEOUT = 15

# Enable telnet console (disabled by default)
TELNETCONSOLE_ENABLED = False

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = 'twisted.internet.default.DefaultReactor'
