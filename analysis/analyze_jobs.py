"""
Job market analysis and reporting
Analyzes job listings data to generate insights
"""
import pandas as pd
import logging
import os
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class JobAnalyzer:
    """Analyze job listing data"""
    
    def __init__(self, input_file=None, output_dir='./'):
        """
        Initialize analyzer
        
        Args:
            input_file (str): Path to cleaned job data
            output_dir (str): Directory for output reports
        """
        self.input_file = input_file or '../data/final/jobs_cleaned.csv'
        self.output_dir = output_dir
        self.df = None
        self.analysis = {}
    
    def load_data(self):
        """Load cleaned job data"""
        try:
            if self.input_file.endswith('.json'):
                self.df = pd.read_json(self.input_file)
            else:
                self.df = pd.read_csv(self.input_file)
            
            logger.info(f"Loaded {len(self.df)} job records for analysis")
            return self.df
        
        except FileNotFoundError:
            logger.error(f"File not found: {self.input_file}")
            return None
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None
    
    def analyze_skills(self):
        """Analyze required skills frequency"""
        if self.df is None or 'required_skills' not in self.df.columns:
            return {}
        
        skills_counter = {}
        
        for skills_str in self.df['required_skills'].dropna():
            if isinstance(skills_str, str) and skills_str:
                # Split skills by pipe separator
                skills = [s.strip() for s in skills_str.split('|') if s.strip()]
                for skill in skills:
                    skills_counter[skill] = skills_counter.get(skill, 0) + 1
        
        # Sort by frequency
        sorted_skills = sorted(skills_counter.items(), key=lambda x: x[1], reverse=True)
        
        self.analysis['top_skills'] = sorted_skills[:20]
        logger.info(f"Analyzed {len(skills_counter)} unique skills")
        
        return dict(self.analysis['top_skills'])
    
    def analyze_locations(self):
        """Analyze job locations"""
        if self.df is None or 'location' not in self.df.columns:
            return {}
        
        location_counts = self.df['location'].value_counts().head(15)
        self.analysis['top_locations'] = location_counts.to_dict()
        
        logger.info(f"Analyzed {len(location_counts)} top locations")
        return self.analysis['top_locations']
    
    def analyze_companies(self):
        """Analyze companies hiring most"""
        if self.df is None or 'company_name' not in self.df.columns:
            return {}
        
        company_counts = self.df['company_name'].value_counts().head(15)
        self.analysis['top_companies'] = company_counts.to_dict()
        
        logger.info(f"Analyzed {len(company_counts)} top companies")
        return self.analysis['top_companies']
    
    def analyze_employment_types(self):
        """Analyze employment type distribution"""
        if self.df is None or 'employment_type' not in self.df.columns:
            return {}
        
        emp_type_counts = self.df['employment_type'].value_counts()
        self.analysis['employment_types'] = emp_type_counts.to_dict()
        
        logger.info("Analyzed employment type distribution")
        return self.analysis['employment_types']
    
    def analyze_experience_levels(self):
        """Analyze experience level distribution"""
        if self.df is None or 'experience_level' not in self.df.columns:
            return {}
        
        exp_level_counts = self.df['experience_level'].value_counts()
        self.analysis['experience_levels'] = exp_level_counts.to_dict()
        
        logger.info("Analyzed experience level distribution")
        return self.analysis['experience_levels']
    
    def analyze_job_titles(self):
        """Analyze most common job titles"""
        if self.df is None or 'job_title' not in self.df.columns:
            return {}
        
        title_counts = self.df['job_title'].value_counts().head(15)
        self.analysis['top_job_titles'] = title_counts.to_dict()
        
        logger.info(f"Analyzed {len(title_counts)} top job titles")
        return self.analysis['top_job_titles']
    
    def analyze_departments(self):
        """Analyze job departments"""
        if self.df is None or 'department' not in self.df.columns:
            return {}
        
        # Filter out empty departments
        dept_counts = self.df[self.df['department'] != 'Not specified']['department'].value_counts().head(10)
        
        if len(dept_counts) > 0:
            self.analysis['top_departments'] = dept_counts.to_dict()
        else:
            self.analysis['top_departments'] = {}
        
        logger.info("Analyzed job departments")
        return self.analysis['top_departments']
    
    def analyze_sources(self):
        """Analyze job distribution by source"""
        if self.df is None or 'source' not in self.df.columns:
            return {}
        
        source_counts = self.df['source'].value_counts()
        self.analysis['sources'] = source_counts.to_dict()
        
        logger.info("Analyzed job sources")
        return self.analysis['sources']
    
    def generate_summary(self):
        """Generate overall summary statistics"""
        if self.df is None:
            return {}
        
        summary = {
            'total_jobs': len(self.df),
            'unique_companies': self.df['company_name'].nunique(),
            'unique_locations': self.df['location'].nunique(),
            'date_analyzed': datetime.now().isoformat(),
            'data_source': 'Job scraping project',
        }
        
        self.analysis['summary'] = summary
        return summary
    
    def run_all_analysis(self):
        """Run all analysis operations"""
        logger.info("Starting job market analysis...")
        
        # Load data
        self.load_data()
        if self.df is None:
            return False
        
        # Run all analyses
        self.generate_summary()
        self.analyze_skills()
        self.analyze_locations()
        self.analyze_companies()
        self.analyze_employment_types()
        self.analyze_experience_levels()
        self.analyze_job_titles()
        self.analyze_departments()
        self.analyze_sources()
        
        return True
    
    def save_analysis(self):
        """Save analysis results"""
        if not self.analysis:
            logger.error("No analysis to save")
            return False
        
        try:
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Save as JSON
            json_file = os.path.join(self.output_dir, 'analysis_report.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved analysis report to: {json_file}")
            
            # Save as text report
            report_file = os.path.join(self.output_dir, 'analysis_report.txt')
            self._save_text_report(report_file)
            
            return True
        
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
            return False
    
    def _save_text_report(self, filepath):
        """Save analysis as formatted text report"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("JOB MARKET ANALYSIS REPORT\n")
                f.write("="*80 + "\n\n")
                
                # Summary
                summary = self.analysis.get('summary', {})
                f.write("EXECUTIVE SUMMARY\n")
                f.write("-"*80 + "\n")
                f.write(f"Total Job Listings: {summary.get('total_jobs', 0)}\n")
                f.write(f"Unique Companies: {summary.get('unique_companies', 0)}\n")
                f.write(f"Unique Locations: {summary.get('unique_locations', 0)}\n")
                f.write(f"Analysis Date: {summary.get('date_analyzed', 'N/A')}\n\n")
                
                # Top Skills
                f.write("TOP 20 REQUIRED SKILLS\n")
                f.write("-"*80 + "\n")
                skills = self.analysis.get('top_skills', [])
                for i, (skill, count) in enumerate(skills, 1):
                    f.write(f"{i:2}. {skill:.<50} {count:>6} jobs\n")
                f.write("\n")
                
                # Top Companies
                f.write("TOP 15 HIRING COMPANIES\n")
                f.write("-"*80 + "\n")
                companies = self.analysis.get('top_companies', {})
                for i, (company, count) in enumerate(companies.items(), 1):
                    f.write(f"{i:2}. {company:.<50} {count:>6} jobs\n")
                f.write("\n")
                
                # Top Locations
                f.write("TOP 15 JOB LOCATIONS\n")
                f.write("-"*80 + "\n")
                locations = self.analysis.get('top_locations', {})
                for i, (location, count) in enumerate(locations.items(), 1):
                    f.write(f"{i:2}. {location:.<50} {count:>6} jobs\n")
                f.write("\n")
                
                # Employment Types
                f.write("EMPLOYMENT TYPE DISTRIBUTION\n")
                f.write("-"*80 + "\n")
                emp_types = self.analysis.get('employment_types', {})
                for emp_type, count in emp_types.items():
                    percentage = (count / summary.get('total_jobs', 1)) * 100
                    f.write(f"{emp_type:.<40} {count:>6} ({percentage:>5.1f}%)\n")
                f.write("\n")
                
                # Experience Levels
                f.write("EXPERIENCE LEVEL DISTRIBUTION\n")
                f.write("-"*80 + "\n")
                exp_levels = self.analysis.get('experience_levels', {})
                for level, count in exp_levels.items():
                    percentage = (count / summary.get('total_jobs', 1)) * 100
                    f.write(f"{level:.<40} {count:>6} ({percentage:>5.1f}%)\n")
                f.write("\n")
                
                # Job Title
                f.write("TOP 15 JOB TITLES\n")
                f.write("-"*80 + "\n")
                titles = self.analysis.get('top_job_titles', {})
                for i, (title, count) in enumerate(titles.items(), 1):
                    f.write(f"{i:2}. {title:.<50} {count:>6} jobs\n")
                f.write("\n")
                
                # Departments
                f.write("TOP DEPARTMENTS\n")
                f.write("-"*80 + "\n")
                depts = self.analysis.get('top_departments', {})
                if depts:
                    for dept, count in depts.items():
                        f.write(f"{dept:.<40} {count:>6} jobs\n")
                else:
                    f.write("No department data available\n")
                f.write("\n")
                
                # Sources
                f.write("JOB DISTRIBUTION BY SOURCE\n")
                f.write("-"*80 + "\n")
                sources = self.analysis.get('sources', {})
                for source, count in sources.items():
                    percentage = (count / summary.get('total_jobs', 1)) * 100
                    f.write(f"{source:.<40} {count:>6} ({percentage:>5.1f}%)\n")
                f.write("\n")
                
                f.write("="*80 + "\n")
                f.write("End of Report\n")
                f.write("="*80 + "\n")
            
            logger.info(f"Saved text report to: {filepath}")
        
        except Exception as e:
            logger.error(f"Error saving text report: {str(e)}")
    
    def print_analysis(self):
        """Print analysis to console"""
        if not self.analysis:
            logger.error("No analysis to display")
            return
        
        print("\n" + "="*80)
        print("JOB MARKET ANALYSIS REPORT")
        print("="*80 + "\n")
        
        # Summary
        summary = self.analysis.get('summary', {})
        print("EXECUTIVE SUMMARY")
        print("-"*80)
        print(f"Total Job Listings: {summary.get('total_jobs', 0)}")
        print(f"Unique Companies: {summary.get('unique_companies', 0)}")
        print(f"Unique Locations: {summary.get('unique_locations', 0)}\n")
        
        # Top Skills
        print("TOP 20 REQUIRED SKILLS")
        print("-"*80)
        skills = self.analysis.get('top_skills', [])
        for i, (skill, count) in enumerate(skills, 1):
            print(f"{i:2}. {skill:.<50} {count:>6} jobs")
        print()
        
        # Top Companies
        print("TOP 15 HIRING COMPANIES")
        print("-"*80)
        companies = self.analysis.get('top_companies', {})
        for i, (company, count) in enumerate(companies.items(), 1):
            print(f"{i:2}. {company:.<50} {count:>6} jobs")
        print()
        
        # Top Locations
        print("TOP 15 JOB LOCATIONS")
        print("-"*80)
        locations = self.analysis.get('top_locations', {})
        for i, (location, count) in enumerate(locations.items(), 1):
            print(f"{i:2}. {location:.<50} {count:>6} jobs")
        print()
        
        # Employment Types
        print("EMPLOYMENT TYPE DISTRIBUTION")
        print("-"*80)
        emp_types = self.analysis.get('employment_types', {})
        for emp_type, count in emp_types.items():
            percentage = (count / summary.get('total_jobs', 1)) * 100
            print(f"{emp_type:.<40} {count:>6} ({percentage:>5.1f}%)")
        print()
        
        # Experience Levels
        print("EXPERIENCE LEVEL DISTRIBUTION")
        print("-"*80)
        exp_levels = self.analysis.get('experience_levels', {})
        for level, count in exp_levels.items():
            percentage = (count / summary.get('total_jobs', 1)) * 100
            print(f"{level:.<40} {count:>6} ({percentage:>5.1f}%)")
        print()


def main():
    """Main entry point"""
    logger.info("\n" + "="*80)
    logger.info("JOB MARKET ANALYSIS")
    logger.info("="*80)
    
    analyzer = JobAnalyzer(output_dir='./')
    
    # Run analysis
    if analyzer.run_all_analysis():
        # Save results
        analyzer.save_analysis()
        
        # Print to console
        analyzer.print_analysis()
        
        logger.info("\nAnalysis complete!")
    else:
        logger.error("Analysis failed")


if __name__ == '__main__':
    main()
