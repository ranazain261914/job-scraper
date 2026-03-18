"""
Scrapy pipelines for data processing and export
"""
import csv
import json
import logging
from datetime import datetime
from itemadapter import ItemAdapter
import scrapy

logger = logging.getLogger(__name__)


class JobsPipeline:
    """
    Base pipeline for job items
    """
    
    def open_spider(self, spider):
        """Called when spider is opened"""
        logger.info(f"Opened spider: {spider.name}")
    
    def close_spider(self, spider):
        """Called when spider is closed"""
        logger.info(f"Closed spider: {spider.name}")
    
    def process_item(self, item, spider):
        """Process item"""
        return item


class DuplicateRemovalPipeline:
    """
    Remove duplicate job URLs
    """
    
    def __init__(self):
        self.ids_seen = set()
    
    def process_item(self, item, spider):
        """Check for duplicate URLs"""
        adapter = ItemAdapter(item)
        
        job_url = adapter.get('job_url', '').strip().lower()
        
        if job_url in self.ids_seen:
            logger.debug(f"Duplicate job dropped: {job_url}")
            raise scrapy.DropItem(f"Duplicate item found: {job_url}")
        else:
            self.ids_seen.add(job_url)
            return item


class DataCleaningPipeline:
    """
    Clean and normalize job data
    """
    
    def process_item(self, item, spider):
        """Clean and normalize fields"""
        adapter = ItemAdapter(item)
        
        # Clean text fields
        for field in ['job_title', 'company_name', 'location', 'department',
                      'employment_type', 'experience_level', 'job_description']:
            if field in adapter:
                value = adapter.get(field, '').strip()
                # Remove extra whitespace
                value = ' '.join(value.split())
                adapter[field] = value
        
        # Normalize employment type
        if 'employment_type' in adapter:
            emp_type = adapter['employment_type'].lower()
            if any(x in emp_type for x in ['internship', 'intern']):
                adapter['employment_type'] = 'Internship'
            elif any(x in emp_type for x in ['full time', 'full-time']):
                adapter['employment_type'] = 'Full-time'
            elif any(x in emp_type for x in ['part time', 'part-time']):
                adapter['employment_type'] = 'Part-time'
            elif any(x in emp_type for x in ['contract', 'freelance']):
                adapter['employment_type'] = 'Contract'
            else:
                adapter['employment_type'] = 'Not specified'
        
        # Normalize location
        if 'location' in adapter:
            location = adapter['location'].lower()
            if 'remote' in location:
                adapter['location'] = 'Remote'
            else:
                # Keep location as-is but clean it
                adapter['location'] = adapter['location'].strip()
        
        # Ensure experience level
        if not adapter.get('experience_level'):
            adapter['experience_level'] = 'Not specified'
        
        # Ensure skills is a list
        if 'required_skills' in adapter:
            skills = adapter['required_skills']
            if isinstance(skills, str):
                adapter['required_skills'] = [s.strip() for s in skills.split(',') if s.strip()]
            elif not isinstance(skills, list):
                adapter['required_skills'] = []
        else:
            adapter['required_skills'] = []
        
        # Set scraped_at timestamp
        adapter['scraped_at'] = datetime.now().isoformat()
        
        return item


class CsvExportPipeline:
    """
    Export job items to CSV
    """
    
    def __init__(self):
        self.csv_file = None
        self.csv_writer = None
    
    def open_spider(self, spider):
        """Open CSV file for writing"""
        self.csv_file = open('../data/final/jobs.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(
            self.csv_file,
            fieldnames=[
                'job_title', 'company_name', 'location', 'department',
                'employment_type', 'experience_level', 'posted_date',
                'job_url', 'source', 'required_skills', 'job_description',
                'salary_range', 'scraped_at'
            ]
        )
        self.csv_writer.writeheader()
        logger.info("Opened CSV file for export")
    
    def close_spider(self, spider):
        """Close CSV file"""
        if self.csv_file:
            self.csv_file.close()
            logger.info("Closed CSV file")
    
    def process_item(self, item, spider):
        """Write item to CSV"""
        adapter = ItemAdapter(item)
        
        row = {
            'job_title': adapter.get('job_title', ''),
            'company_name': adapter.get('company_name', ''),
            'location': adapter.get('location', ''),
            'department': adapter.get('department', ''),
            'employment_type': adapter.get('employment_type', ''),
            'experience_level': adapter.get('experience_level', ''),
            'posted_date': adapter.get('posted_date', ''),
            'job_url': adapter.get('job_url', ''),
            'source': adapter.get('source', ''),
            'required_skills': '|'.join(adapter.get('required_skills', [])),
            'job_description': adapter.get('job_description', ''),
            'salary_range': adapter.get('salary_range', ''),
            'scraped_at': adapter.get('scraped_at', '')
        }
        
        self.csv_writer.writerow(row)
        return item


class JsonExportPipeline:
    """
    Export job items to JSON
    """
    
    def __init__(self):
        self.json_file = None
        self.items = []
    
    def open_spider(self, spider):
        """Initialize JSON export"""
        logger.info("Initialized JSON export")
    
    def close_spider(self, spider):
        """Close JSON file and write all items"""
        json_file_path = '../data/final/jobs.json'
        with open(json_file_path, 'w', encoding='utf-8') as f:
            # Convert items to dicts for JSON serialization
            json_items = []
            for item in self.items:
                adapter = ItemAdapter(item)
                json_items.append(dict(adapter))
            
            json.dump(json_items, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Exported {len(self.items)} items to {json_file_path}")
    
    def process_item(self, item, spider):
        """Collect items for JSON export"""
        self.items.append(item)
        return item
