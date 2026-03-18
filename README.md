# Job Listings Scraper & Analysis System

A complete end-to-end job scraping and analysis system using Selenium and Scrapy. This project collects job listings from multiple public job boards, extracts structured data, and performs insightful analysis.

## 📊 Project Overview

This project scrapes job listings from the following sources:
- **Greenhouse** (boards.greenhouse.io)
- **Lever** (jobs.lever.co)
- **Ashby** (ashbyhq.com/careers)

### Features
✅ Multi-site job board scraping with Selenium
✅ Structured data extraction using Scrapy
✅ CSV/JSON output formats
✅ Data cleaning and normalization
✅ Job market analysis with visualizations
✅ Proper Git workflow with feature branches

## 📁 Project Structure

```
job-scraper/
├── selenium/              # Selenium web scraping scripts
│   ├── greenhouse_scraper.py
│   ├── lever_scraper.py
│   ├── ashby_scraper.py
│   └── utils.py
├── scrapy_project/        # Scrapy spider project
│   ├── scrapy.cfg
│   └── jobs_spider/
├── data/
│   ├── raw/              # Raw extracted job URLs (CSV)
│   └── final/            # Cleaned and structured job data (CSV/JSON)
├── analysis/             # Data analysis scripts
│   ├── analyze_jobs.py
│   └── visualizations.py
├── docs/                 # Project documentation
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Google Chrome or Firefox browser (for Selenium)

### Installation

1. **Clone or navigate to the project**
   ```bash
   cd job-scraper
   ```

2. **Create a virtual environment** (Recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 How to Run

### Step 1: Run Selenium Scraper (Extract Job Links)
```bash
cd selenium
python main_scraper.py
```

Output: `/data/raw/job_links.csv`

**What it does:**
- Opens each job board in browser
- Searches for: "Software Engineer", "Data Analyst", "Intern", "QA Engineer"
- Applies filters if available
- Extracts job detail page URLs
- Saves to CSV

**Duration:** 5-15 minutes (depends on internet speed)

### Step 2: Run Scrapy Spider (Extract Job Details)
```bash
cd scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json
```

Output: `/data/final/jobs.json` and `/data/final/jobs.csv`

**What it does:**
- Reads URLs from `/data/raw/job_links.csv`
- Visits each job page
- Extracts structured job data
- Saves to JSON and CSV

**Duration:** 10-30 minutes

### Step 3: Run Data Analysis
```bash
cd analysis
python analyze_jobs.py
```

**What it shows:**
- Top 10 most required skills
- Top hiring locations
- Top hiring companies
- Job type distribution (Intern, Junior, Senior, etc.)
- Most common job titles

## 📊 Extracted Data Fields

Each job record contains:
- `job_title` - Job title/position
- `company_name` - Hiring company name
- `location` - Job location (city, country, or "Remote")
- `department` - Department (Engineering, Sales, etc.)
- `employment_type` - Full-time, Part-time, Intern, Contract
- `posted_date` - When job was posted
- `job_url` - Full URL to job listing
- `job_description` - Complete job description text
- `required_skills` - Extracted technical skills
- `experience_level` - Junior, Mid, Senior, or Not specified

## 🌳 Git Workflow

This project follows a structured Git branching strategy:

### Main Branches
- `main` - Production-ready code (stable releases)
- `develop` - Development branch (integration point)

### Feature Branches
- `feature/selenium-scraper` - Selenium implementation
- `feature/scrapy-parser` - Scrapy spiders
- `feature/data-analysis` - Analysis scripts

### Bug Fix Branches
- `bugfix/issue-name` - Bug fixes

### Workflow Example
```bash
# 1. Start a feature
git checkout -b feature/new-feature develop

# 2. Make changes and commit
git add .
git commit -m "Add new feature"

# 3. Merge back to develop
git checkout develop
git merge --no-ff feature/new-feature

# 4. Create release when ready
git checkout main
git merge --no-ff develop
git tag -a v1.0 -m "Release version 1.0"
```

## 📝 Best Practices

✅ **Selenium:**
- Uses WebDriverWait for proper synchronization
- Implements respectful delays between requests
- Handles dynamic content loading
- Never bypasses CAPTCHAs or requires login

✅ **Scrapy:**
- Modular spider design
- Proper error handling for missing fields
- Respects robots.txt
- Uses item pipelines for data cleaning

✅ **General:**
- Clean, modular code with comments
- Comprehensive error handling
- Meaningful git commit messages
- Proper logging and debugging

## ⚠️ Important Notes

1. **Rate Limiting:** The scrapers include delays to avoid overloading servers
2. **Browser:** Ensure you have Chrome or Firefox installed
3. **Data Privacy:** Respect website terms of service
4. **Updates:** Job board HTML structure may change - update selectors accordingly

## 🐛 Troubleshooting

### Selenium Issues
- **Chrome driver not found:** Install chromedriver: https://chromedriver.chromium.org/
- **Timeout errors:** Increase wait times in code
- **Element not found:** HTML structure may have changed - inspect and update selectors

### Scrapy Issues
- **Spider not parsing:** Check CSS selectors against actual HTML
- **Missing fields:** Add fallback values in item pipeline

### General
- Check browser console for JavaScript errors
- Verify internet connection
- Ensure website is accessible from your location

## 📈 Analysis Output

The analysis script generates:
- Summary statistics (total jobs, unique companies, etc.)
- Top skills frequency chart
- Location distribution
- Company hiring patterns
- HTML report in `analysis/report.html`

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

1. Create a feature branch from `develop`
2. Make your changes
3. Commit with clear messages
4. Push and merge back to `develop`

---

**Last Updated:** March 2026
**Version:** 1.0
