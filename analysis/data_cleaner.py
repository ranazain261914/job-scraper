"""
Data cleaning and preprocessing for job listings
Handles deduplication, normalization, and quality checks
"""
import pandas as pd
import logging
import os
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class JobDataCleaner:
    """Clean and normalize job listing data"""
    
    def __init__(self, input_file=None, output_file=None):
        """
        Initialize cleaner
        
        Args:
            input_file (str): Path to input CSV/JSON
            output_file (str): Path to save cleaned data
        """
        self.input_file = input_file or '../data/final/jobs.csv'
        self.output_file = output_file or '../data/final/jobs_cleaned.csv'
        self.df = None
        self.original_count = 0
        self.cleaned_count = 0
    
    def load_data(self):
        """Load job data from file"""
        try:
            if self.input_file.endswith('.json'):
                self.df = pd.read_json(self.input_file)
            else:
                self.df = pd.read_csv(self.input_file)
            
            self.original_count = len(self.df)
            logger.info(f"Loaded {self.original_count} job records")
            return self.df
        
        except FileNotFoundError:
            logger.error(f"File not found: {self.input_file}")
            return None
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None
    
    def remove_duplicates(self):
        """Remove duplicate job listings by URL"""
        if self.df is None:
            return
        
        initial_count = len(self.df)
        
        # Remove duplicates based on job_url
        self.df = self.df.drop_duplicates(subset=['job_url'], keep='first')
        
        removed = initial_count - len(self.df)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate job listings")
    
    def clean_text_fields(self):
        """Clean and normalize text fields"""
        if self.df is None:
            return
        
        text_fields = [
            'job_title', 'company_name', 'location', 'department',
            'employment_type', 'experience_level'
        ]
        
        for field in text_fields:
            if field in self.df.columns:
                # Remove extra whitespace
                self.df[field] = self.df[field].fillna('').str.strip()
                self.df[field] = self.df[field].str.replace(r'\s+', ' ', regex=True)
                
                # Remove leading/trailing quotes
                self.df[field] = self.df[field].str.replace(r'^["\']|["\']$', '', regex=True)
    
    def normalize_employment_type(self):
        """Normalize employment type values"""
        if 'employment_type' not in self.df.columns:
            return
        
        def normalize_type(value):
            if pd.isna(value) or value == '':
                return 'Not specified'
            
            value_lower = str(value).lower().strip()
            
            if any(x in value_lower for x in ['intern', 'internship']):
                return 'Internship'
            elif any(x in value_lower for x in ['full', 'full-time', 'fulltime']):
                return 'Full-time'
            elif any(x in value_lower for x in ['part', 'part-time', 'parttime']):
                return 'Part-time'
            elif any(x in value_lower for x in ['contract', 'freelance', 'temporary']):
                return 'Contract'
            elif any(x in value_lower for x in ['apprentice', 'graduate']):
                return 'Graduate/Apprentice'
            else:
                return 'Not specified'
        
        self.df['employment_type'] = self.df['employment_type'].apply(normalize_type)
        logger.info("Normalized employment types")
    
    def normalize_experience_level(self):
        """Normalize experience level values"""
        if 'experience_level' not in self.df.columns:
            return
        
        def normalize_level(value):
            if pd.isna(value) or value == '':
                return 'Not specified'
            
            value_lower = str(value).lower().strip()
            
            if any(x in value_lower for x in ['entry', 'junior', 'grad', 'intern']):
                return 'Junior'
            elif any(x in value_lower for x in ['mid', 'intermediate', 'mid-level', 'mid level']):
                return 'Mid-level'
            elif any(x in value_lower for x in ['senior', 'lead', 'principal', 'staff']):
                return 'Senior'
            elif any(x in value_lower for x in ['manager', 'director', 'executive']):
                return 'Manager/Director'
            else:
                return 'Not specified'
        
        self.df['experience_level'] = self.df['experience_level'].apply(normalize_level)
        logger.info("Normalized experience levels")
    
    def normalize_location(self):
        """Normalize location values"""
        if 'location' not in self.df.columns:
            return
        
        def normalize_loc(value):
            if pd.isna(value) or value == '':
                return 'Not specified'
            
            value_str = str(value).strip()
            
            # Check for remote
            if 'remote' in value_str.lower():
                return 'Remote'
            
            # Normalize common variations
            value_str = value_str.replace(' - ', ', ')
            value_str = value_str.replace(' | ', ', ')
            
            return value_str
        
        self.df['location'] = self.df['location'].apply(normalize_loc)
        logger.info("Normalized locations")
    
    def clean_descriptions(self):
        """Clean job descriptions"""
        if 'job_description' not in self.df.columns:
            return
        
        def clean_desc(text):
            if pd.isna(text) or text == '':
                return ''
            
            # Convert to string
            text = str(text)
            
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            # Remove HTML entities
            text = text.replace('&nbsp;', ' ')
            text = text.replace('&quot;', '"')
            text = text.replace('&amp;', '&')
            text = text.replace('<br>', ' ')
            text = text.replace('<br/>', ' ')
            text = text.replace('<br />', ' ')
            
            # Remove multiple spaces
            text = ' '.join(text.split())
            
            return text.strip()
        
        self.df['job_description'] = self.df['job_description'].apply(clean_desc)
        logger.info("Cleaned job descriptions")
    
    def normalize_skills(self):
        """Normalize skills field"""
        if 'required_skills' not in self.df.columns:
            return
        
        def normalize_skills(value):
            if pd.isna(value) or value == '' or value == '[]':
                return ''
            
            # If it's a string representation of a list
            if isinstance(value, str):
                if value.startswith('[') and value.endswith(']'):
                    # Parse string list
                    try:
                        import json
                        skills = json.loads(value.replace("'", '"'))
                        return '|'.join(skills)
                    except:
                        return value
                elif '|' in value:
                    # Already pipe-separated
                    skills = [s.strip() for s in value.split('|') if s.strip()]
                    return '|'.join(skills)
                else:
                    return value
            
            return str(value)
        
        self.df['required_skills'] = self.df['required_skills'].apply(normalize_skills)
        logger.info("Normalized skills field")
    
    def fill_missing_values(self):
        """Fill missing values with appropriate defaults"""
        if self.df is None:
            return
        
        fill_values = {
            'job_title': 'Not specified',
            'company_name': 'Not specified',
            'location': 'Not specified',
            'department': 'Not specified',
            'employment_type': 'Not specified',
            'experience_level': 'Not specified',
            'posted_date': '',
            'required_skills': '',
            'salary_range': '',
            'benefits': '',
            'source': 'unknown'
        }
        
        for field, default_value in fill_values.items():
            if field in self.df.columns:
                self.df[field] = self.df[field].fillna(default_value)
        
        logger.info("Filled missing values")
    
    def remove_invalid_records(self):
        """Remove records with missing critical fields"""
        if self.df is None:
            return
        
        initial_count = len(self.df)
        
        # Must have at least job title and URL
        self.df = self.df[
            (self.df['job_title'].notna()) & (self.df['job_title'] != 'Not specified') &
            (self.df['job_url'].notna()) & (self.df['job_url'] != '')
        ]
        
        removed = initial_count - len(self.df)
        if removed > 0:
            logger.info(f"Removed {removed} invalid records")
    
    def clean(self):
        """Run all cleaning operations"""
        logger.info("Starting data cleaning process...")
        
        # Load data
        self.load_data()
        if self.df is None:
            return False
        
        # Run cleaning operations
        self.remove_duplicates()
        self.clean_text_fields()
        self.normalize_employment_type()
        self.normalize_experience_level()
        self.normalize_location()
        self.clean_descriptions()
        self.normalize_skills()
        self.fill_missing_values()
        self.remove_invalid_records()
        
        self.cleaned_count = len(self.df)
        
        logger.info("\n" + "="*60)
        logger.info("DATA CLEANING SUMMARY")
        logger.info("="*60)
        logger.info(f"Original records: {self.original_count}")
        logger.info(f"Cleaned records:  {self.cleaned_count}")
        logger.info(f"Records removed:  {self.original_count - self.cleaned_count}")
        logger.info(f"{"="*60}\n")
        
        return True
    
    def save(self):
        """Save cleaned data"""
        if self.df is None:
            logger.error("No data to save")
            return False
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            
            # Save as CSV
            self.df.to_csv(self.output_file, index=False, encoding='utf-8')
            logger.info(f"Saved cleaned data to: {self.output_file}")
            
            # Also save as JSON
            json_output = self.output_file.replace('.csv', '.json')
            self.df.to_json(json_output, orient='records', indent=2)
            logger.info(f"Saved cleaned data to: {json_output}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False
    
    def get_statistics(self):
        """Get data statistics"""
        if self.df is None:
            return None
        
        stats = {
            'total_jobs': len(self.df),
            'unique_companies': self.df['company_name'].nunique(),
            'unique_locations': self.df['location'].nunique(),
            'employment_types': self.df['employment_type'].value_counts().to_dict(),
            'experience_levels': self.df['experience_level'].value_counts().to_dict(),
            'top_companies': self.df['company_name'].value_counts().head(10).to_dict(),
            'top_locations': self.df['location'].value_counts().head(10).to_dict(),
            'sources': self.df['source'].value_counts().to_dict(),
        }
        
        return stats


def main():
    """Main entry point"""
    logger.info("\n" + "="*60)
    logger.info("JOB DATA CLEANING AND NORMALIZATION")
    logger.info("="*60)
    
    cleaner = JobDataCleaner()
    
    # Run cleaning
    if cleaner.clean():
        # Save results
        cleaner.save()
        
        # Print statistics
        stats = cleaner.get_statistics()
        if stats:
            logger.info("\nDATA STATISTICS:")
            logger.info(f"Total jobs: {stats['total_jobs']}")
            logger.info(f"Unique companies: {stats['unique_companies']}")
            logger.info(f"Unique locations: {stats['unique_locations']}")
            logger.info(f"\nEmployment types: {stats['employment_types']}")
            logger.info(f"\nExperience levels: {stats['experience_levels']}")


if __name__ == '__main__':
    main()
