# Quick Start Guide

Get the job scraper running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Chrome or Firefox installed
- [ ] ChromeDriver in PATH or project root
- [ ] Internet connection

## Quick Installation

### 1. Setup Environment (2 minutes)

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run Selenium Scraper (5-15 minutes)

```powershell
cd selenium
python main_scraper.py
```

**What happens:**
- Chrome browser opens automatically
- Searches 4 job sites (Greenhouse, Lever, Ashby)
- Collects job URLs
- Saves to `data/raw/job_links.csv`

### 3. Run Scrapy Spider (10-30 minutes)

```powershell
cd ../scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json
```

**What happens:**
- Visits each job URL
- Extracts structured data
- Removes duplicates automatically
- Saves to CSV and JSON

### 4. Clean Data (1 minute)

```powershell
cd ../analysis
python data_cleaner.py
```

**Output:**
- Cleaned CSV: `data/final/jobs_cleaned.csv`
- JSON: `data/final/jobs_cleaned.json`
- Statistics printed

### 5. Analyze Results (1 minute)

```powershell
python analyze_jobs.py
```

**Output:**
- Console report with insights
- JSON report: `analysis_report.json`
- Text report: `analysis_report.txt`

## Expected Results

After running all steps:

### File Structure
```
data/
├── raw/
│   ├── job_links.csv          (1,000-5,000 URLs)
│   ├── greenhouse_links.csv
│   ├── lever_links.csv
│   └── ashby_links.csv
└── final/
    ├── jobs.csv               (cleaned data)
    ├── jobs.json
    ├── jobs_cleaned.csv
    └── jobs_cleaned.json

analysis/
├── analysis_report.json       (insights)
├── analysis_report.txt
```

### Sample Output

```
TOP REQUIRED SKILLS
1. Python........................................  342 jobs
2. JavaScript...................................  298 jobs
3. React.........................................  267 jobs
4. SQL...........................................  245 jobs
5. AWS...........................................  198 jobs

TOP HIRING COMPANIES
1. Google........................................   45 jobs
2. Microsoft.....................................   38 jobs
3. Amazon........................................   35 jobs

JOB LOCATIONS
1. Remote........................................  345 jobs
2. San Francisco, CA.............................   98 jobs
3. New York, NY..................................   87 jobs
```

## Common Commands

```bash
# Activate environment
.\venv\Scripts\Activate.ps1

# Deactivate environment
deactivate

# Run specific scraper
cd selenium
python greenhouse_scraper.py
python lever_scraper.py
python ashby_scraper.py

# Inspect data
python -c "import pandas as pd; df=pd.read_csv('../data/final/jobs.csv'); print(df.head())"

# Run specific analysis
python -c "from analyze_jobs import JobAnalyzer; JobAnalyzer().run_all_analysis()"
```

## Duration Estimate

| Step | Time | Status |
|------|------|--------|
| Install | 2 min | ✅ Quick |
| Selenium | 5-15 min | ⏳ Depends on speed |
| Scrapy | 10-30 min | ⏳ Depends on Internet |
| Cleaning | 1 min | ✅ Quick |
| Analysis | 1 min | ✅ Quick |
| **Total** | **19-49 min** | 🎯 About 30 min avg |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `chromedriver not found` | Download from https://chromedriver.chromium.org/ |
| `Connection timeout` | Check internet, increase wait times in code |
| `Port already in use` | Kill Chrome process or use different port |
| `No such file` | Ensure Selenium completed before Scrapy |

## Next Steps

1. ✅ Run all 5 steps above
2. 📊 Examine results in `data/final/`
3. 📈 View analysis in `analysis/analysis_report.txt`
4. 🔧 Customize search queries in scrapers
5. 📚 Read full docs in `docs/`

## Full Documentation

- Setup Guide: `docs/SETUP.md`
- Project README: `README.md`
- Code Structure: See inline comments

---

**Questions?** Check README.md for detailed documentation!
