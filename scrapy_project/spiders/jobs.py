"""
Scrapy spider for scraping job listings from various job boards
"""
import logging
import csv
from urllib.parse import urljoin
from datetime import datetime
import scrapy
from ..items import JobItem

logger = logging.getLogger(__name__)


class JobsSpider(scrapy.Spider):
    """
    Spider for scraping job listings from multiple sources
    Reads job URLs from CSV and extracts detailed job information
    """
    
    name = 'jobs'
    allowed_domains = ['greenhouse.io', 'lever.co', 'ashbyhq.com']
    
    def __init__(self, *args, **kwargs):
        super(JobsSpider, self).__init__(*args, **kwargs)
        self.job_urls = []
        self.load_job_urls()
    
    def load_job_urls(self):
        """Load job URLs from CSV file"""
        try:
            csv_file = '../data/raw/job_links.csv'
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('url', '').strip()
                    if url:
                        self.job_urls.append({
                            'url': url,
                            'source': row.get('source', 'unknown')
                        })
            
            logger.info(f"Loaded {len(self.job_urls)} job URLs from {csv_file}")
        
        except FileNotFoundError:
            logger.error(f"Job URLs CSV file not found: {csv_file}")
            logger.error("Please run selenium/main_scraper.py first to generate job links")
        except Exception as e:
            logger.error(f"Error loading job URLs: {str(e)}")
    
    def start_requests(self):
        """Generate requests for job URLs"""
        for job_info in self.job_urls:
            yield scrapy.Request(
                url=job_info['url'],
                callback=self.parse,
                meta={'source': job_info['source']},
                dont_filter=True
            )
    
    def parse(self, response):
        """Parse job listing page"""
        source = response.meta.get('source', 'unknown')
        
        logger.info(f"Parsing job from {source}: {response.url}")
        
        if 'greenhouse' in source.lower() or 'greenhouse' in response.url.lower():
            yield from self.parse_greenhouse(response)
        elif 'lever' in source.lower() or 'lever' in response.url.lower():
            yield from self.parse_lever(response)
        elif 'ashby' in source.lower() or 'ashby' in response.url.lower():
            yield from self.parse_ashby(response)
        else:
            yield from self.parse_generic(response)
    
    def parse_greenhouse(self, response):
        """Parse Greenhouse job listing"""
        item = JobItem()
        
        item['job_url'] = response.url
        item['source'] = 'greenhouse'
        
        # Extract title
        item['job_title'] = response.css('h2.gh-jobs-board-title::text').get('').strip() or \
                           response.css('h1::text').get('').strip() or \
                           response.css('h1.job-title::text').get('').strip()
        
        # Extract company name
        item['company_name'] = response.css('.company-name::text').get('').strip() or \
                              response.css('h2.organization::text').get('').strip() or \
                              response.css('[data-company-name]::text').get('').strip()
        
        # Extract location
        item['location'] = response.css('[data-job-location]::text').get('').strip() or \
                          response.css('.job-location::text').get('').strip() or \
                          response.css('span[data-location]::text').get('').strip()
        
        # Extract department
        item['department'] = response.css('[data-job-department]::text').get('').strip() or \
                            response.css('.job-department::text').get('').strip()
        
        # Extract employment type
        item['employment_type'] = response.css('[data-employment-type]::text').get('').strip()
        
        # Extract job description
        item['job_description'] = ' '.join(
            response.css('#job-content ::text').getall()
        ).strip() or \
        ' '.join(response.css('.job-description ::text').getall()).strip()
        
        # Extract skills from description
        item['required_skills'] = self.extract_skills(item.get('job_description', ''))
        
        # Set posted date (Greenhouse doesn't always show it)
        item['posted_date'] = response.css('[data-date]::text').get('').strip()
        
        item['experience_level'] = ''
        
        yield item
    
    def parse_lever(self, response):
        """Parse Lever job listing"""
        item = JobItem()
        
        item['job_url'] = response.url
        item['source'] = 'lever'
        
        # Extract title
        item['job_title'] = response.css('.posting-headline h2::text').get('').strip() or \
                           response.css('h2::text').get('').strip()
        
        # Extract company name
        item['company_name'] = response.css('.posting-headline h3::text').get('').strip() or \
                              response.css('[data-company-name]::text').get('').strip()
        
        # Extract location
        item['location'] = response.css('[data-location]::text').get('').strip() or \
                          response.css('.posting-category-tag::text').getall()
        
        if isinstance(item['location'], list):
            item['location'] = ' | '.join(item['location']).strip()
        
        # Extract department
        item['department'] = response.css('div.posting-category:contains("Department")::text').get('').strip()
        
        # Extract employment type
        item['employment_type'] = response.css('div.posting-category:contains("Type")::text').get('').strip()
        
        # Extract job description
        item['job_description'] = ' '.join(
            response.css('.posting-content ::text').getall()
        ).strip() or \
        ' '.join(response.css('[data-job-description] ::text').getall()).strip()
        
        # Extract skills
        item['required_skills'] = self.extract_skills(item.get('job_description', ''))
        
        # Posted date
        item['posted_date'] = response.css('.posting-date::text').get('').strip()
        
        item['experience_level'] = ''
        
        yield item
    
    def parse_ashby(self, response):
        """Parse Ashby job listing"""
        item = JobItem()
        
        item['job_url'] = response.url
        item['source'] = 'ashby'
        
        # Extract title
        item['job_title'] = response.css('h1::text').get('').strip() or \
                           response.css('[data-job-title]::text').get('').strip()
        
        # Extract company name
        item['company_name'] = response.css('[data-company]::text').get('').strip() or \
                              response.css('h2.company-name::text').get('').strip()
        
        # Extract location
        item['location'] = response.css('[data-location]::text').get('').strip() or \
                          response.css('.job-location::text').get('').strip()
        
        # Extract department
        item['department'] = response.css('[data-department]::text').get('').strip()
        
        # Extract employment type
        item['employment_type'] = response.css('[data-job-type]::text').get('').strip()
        
        # Extract job description
        item['job_description'] = ' '.join(
            response.css('[data-job-description] ::text').getall()
        ).strip() or \
        ' '.join(response.css('.job-description ::text').getall()).strip()
        
        # Extract skills
        item['required_skills'] = self.extract_skills(item.get('job_description', ''))
        
        # Posted date
        item['posted_date'] = response.css('[data-posted-date]::text').get('').strip()
        
        item['experience_level'] = ''
        
        yield item
    
    def parse_generic(self, response):
        """Generic parser for unknown job board formats"""
        item = JobItem()
        
        item['job_url'] = response.url
        item['source'] = 'unknown'
        
        # Try to extract basic info from common HTML patterns
        item['job_title'] = response.css('h1::text').get('').strip() or \
                           response.css('h1.title::text').get('').strip()
        
        item['company_name'] = response.css('h2::text').get('').strip() or \
                              response.css('[data-company]::text').get('').strip()
        
        item['location'] = response.css('.location::text').get('').strip() or \
                          response.css('[data-location]::text').get('').strip()
        
        item['department'] = ''
        item['employment_type'] = ''
        item['posted_date'] = ''
        item['experience_level'] = ''
        
        # Extract all text for description
        item['job_description'] = ' '.join(
            response.css('body ::text').getall()
        ).strip()
        
        item['required_skills'] = self.extract_skills(item.get('job_description', ''))
        
        yield item
    
    @staticmethod
    def extract_skills(text):
        """
        Extract technical skills from job description
        Uses keyword matching for common technical skills
        
        Args:
            text (str): Job description text
        
        Returns:
            list: List of identified skills
        """
        if not text:
            return []
        
        text_lower = text.lower()
        
        # Common technical skills to search for
        skills_keywords = {
            'Python': ['python', 'py'],
            'JavaScript': ['javascript', 'js', 'typescript', 'ts'],
            'Java': ['java ', 'java.'],
            'C++': ['c++', 'cpp'],
            'C#': ['c#', 'csharp', 'c sharp'],
            'PHP': ['php'],
            'Ruby': ['ruby', 'rails'],
            'Go': ['golang', ' go '],
            'Rust': ['rust'],
            'SQL': ['sql', 'postgresql', 'postgres', 'mysql', 'oracle', 'tsql'],
            'React': ['react', 'reactjs', 'react.js'],
            'Angular': ['angular', 'angularjs'],
            'Vue': ['vue', 'vuejs', 'vue.js'],
            'Node.js': ['node.js', 'nodejs', 'node js'],
            'Django': ['django'],
            'Flask': ['flask'],
            'Spring': ['spring', 'springboot'],
            'AWS': ['aws', 'amazon web services'],
            'Azure': ['azure', 'microsoft azure'],
            'GCP': ['gcp', 'google cloud'],
            'Docker': ['docker'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'Git': ['git', 'github', 'gitlab', 'bitbucket'],
            'Jenkins': ['jenkins'],
            'CI/CD': ['ci/cd', 'continuous integration', 'continuous deployment'],
            'REST API': ['rest api', 'restful', 'rest'],
            'GraphQL': ['graphql'],
            'MongoDB': ['mongodb', 'mongo'],
            'Redis': ['redis'],
            'Machine Learning': ['machine learning', 'ml ', 'deep learning'],
            'TensorFlow': ['tensorflow'],
            'PyTorch': ['pytorch'],
            'Scrum': ['scrum', 'agile'],
            'Jira': ['jira'],
            'Linux': ['linux', 'unix'],
            'Bash': ['bash', 'shell scripting'],
        }
        
        found_skills = set()
        
        for skill, keywords in skills_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_skills.add(skill)
                    break
        
        return list(found_skills)
