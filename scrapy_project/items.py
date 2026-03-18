"""
Scrapy item definitions for job listings
"""
import scrapy


class JobItem(scrapy.Item):
    """
    Job listing item with all extracted fields
    """
    # Basic information
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    department = scrapy.Field()
    
    # Employment details
    employment_type = scrapy.Field()  # Full-time, Part-time, Intern, Contract, etc.
    experience_level = scrapy.Field()  # Junior, Mid, Senior, etc.
    
    # Dates and links
    posted_date = scrapy.Field()
    job_url = scrapy.Field()
    
    # Content
    job_description = scrapy.Field()
    required_skills = scrapy.Field()  # List of skills
    
    # Metadata
    source = scrapy.Field()  # greenhouse, lever, ashby
    scraped_at = scrapy.Field()
    salary_range = scrapy.Field()  # Optional
    benefits = scrapy.Field()  # Optional
