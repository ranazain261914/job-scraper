# HOW TO RUN THE SYSTEM

## ⚠️ IMPORTANT: Prerequisites Required

Before running this system, you must have:
- ✅ Python 3.8+ installed
- ✅ pip (Python package manager)
- ✅ Google Chrome or Firefox installed
- ✅ ChromeDriver or GeckoDriver in PATH

---

## 📋 INSTALLATION STEPS

### Step 1: Install Python

**Windows:**
1. Download from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

Verify installation:
```powershell
python --version
# Should show: Python 3.8.0 or higher
```

### Step 2: Install Chrome WebDriver

1. Find your Chrome version:
   - Open Chrome → Menu (⋮) → Help → About Google Chrome
   - Note the version (e.g., 120.0.6099.129)

2. Download ChromeDriver:
   - Visit: https://chromedriver.chromium.org/
   - Download matching your Chrome version
   - Extract `chromedriver.exe`

3. Add to PATH or place in project root:
   - **Option A**: Place in `C:\Program Files\`
   - **Option B**: Add its directory to Windows PATH
   - **Option C**: Place in project root (`job-scraper/chromedriver.exe`)

Verify:
```powershell
chromedriver --version
# Should show version info
```

### Step 3: Create Virtual Environment

```powershell
cd "c:\Users\Administrator\Documents\UCP\6\T and T\Assignment1"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Verify activation** (you should see `(venv)` at the start of your prompt):
```powershell
# Prompt should show: (venv) PS C:\...
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

**This will install 21 packages** (Selenium, Scrapy, Pandas, etc.)

**Verify installation**:
```powershell
pip list
# Should show all packages installed
```

---

## 🚀 RUNNING THE SYSTEM (4 Steps)

Once setup is complete, follow these 4 steps in order:

### STEP 1: Run Selenium Scraper (5-15 minutes)

```powershell
cd selenium
python main_scraper.py
```

**What happens:**
- Chrome browser opens automatically
- Searches Greenhouse, Lever, and Ashby job boards
- Searches for: "Software Engineer", "Data Analyst", "Intern", "QA Engineer"
- Extracts job detail page URLs
- Closes Chrome
- Creates: `data/raw/job_links.csv`

**Expected output:**
```
Starting Greenhouse scraper...
Navigating to Greenhouse board...
Searching for: Software Engineer
Found job link: https://...
Total unique jobs found so far: 245
✓ Greenhouse scraper completed: 245 links found

Starting Lever scraper...
✓ Lever scraper completed: 189 links found

Starting Ashby scraper...
✓ Ashby scraper completed: 156 links found

SUMMARY OF JOB LINK COLLECTION
Greenhouse.................................... 245 links
Lever.......................................... 189 links
Ashby.......................................... 156 links
Total unique................................... 590 links
```

**Output file**: `data/raw/job_links.csv`

---

### STEP 2: Run Scrapy Spider (10-30 minutes)

```powershell
cd ../scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json
```

**What happens:**
- Reads URLs from `data/raw/job_links.csv`
- Visits each job page
- Extracts: title, company, location, department, type, description, skills
- Removes duplicates
- Cleans and processes data
- Saves to CSV and JSON

**Expected output**:
```
2026-03-18 10:30:00 [scrapy.spiders] INFO: Spider opened
2026-03-18 10:30:05 [scrapy.spiders] DEBUG: Parsing job from greenhouse: https://...
2026-03-18 10:35:00 [scrapy.statscollectors] INFO: Dumping Scrapy stats
2026-03-18 10:35:02 [scrapy.core.engine] INFO: Spider closed (finished)
```

**Output files**:
- `data/final/jobs.json` (structured job data)
- `data/final/jobs.csv` (same data in CSV format)

---

### STEP 3: Clean Data (1 minute)

```powershell
cd ../analysis
python data_cleaner.py
```

**What happens:**
- Removes duplicate URLs
- Normalizes text fields
- Standardizes employment types
- Standardizes experience levels
- Standardizes locations
- Cleans descriptions
- Normalizes skills
- Fills missing values
- Removes invalid records
- Saves cleaned data

**Expected output**:
```
Starting data cleaning process...
Normalized employment types
Normalized experience levels
Normalized locations
Cleaned job descriptions

============================================================
DATA CLEANING SUMMARY
============================================================
Original records: 590
Cleaned records:  487
Records removed:  103
============================================================
Saved cleaned data to: ../data/final/jobs_cleaned.csv
Saved cleaned data to: ../data/final/jobs_cleaned.json

DATA STATISTICS:
Total jobs: 487
Unique companies: 156
Unique locations: 45
```

**Output files**:
- `data/final/jobs_cleaned.csv`
- `data/final/jobs_cleaned.json`

---

### STEP 4: Analyze Results (1 minute)

```powershell
python analyze_jobs.py
```

**What happens:**
- Analyzes all aspects of the job data
- Generates statistics
- Creates reports
- Displays results

**Expected output**:
```
============================================================
JOB MARKET ANALYSIS REPORT
============================================================

EXECUTIVE SUMMARY
Total Job Listings: 487
Unique Companies: 156
Unique Locations: 45

TOP 20 REQUIRED SKILLS
1. Python......................................... 342 jobs
2. JavaScript................................... 298 jobs
3. React......................................... 267 jobs
4. SQL...........................................  245 jobs
5. AWS...........................................  198 jobs
6. Django........................................ 145 jobs
7. Node.js....................................... 134 jobs
8. Docker........................................ 129 jobs
9. REST API...................................... 127 jobs
10. Git.......................................... 125 jobs

[... more skills ...]

TOP 15 HIRING COMPANIES
1. Google........................................ 45 jobs
2. Microsoft.................................... 38 jobs
3. Amazon........................................ 35 jobs
4. Facebook...................................... 28 jobs
5. Apple......................................... 25 jobs

[... more companies ...]

TOP 15 JOB LOCATIONS
1. Remote....................................... 345 jobs
2. San Francisco, CA............................ 98 jobs
3. New York, NY.................................. 87 jobs
4. Seattle, WA.................................. 45 jobs
5. Austin, TX................................... 38 jobs

[... more locations ...]

EMPLOYMENT TYPE DISTRIBUTION
Full-time.................................... 346 (71.0%)
Internship................................... 58 (11.9%)
Part-time.................................... 48 (9.9%)
Contract.................................... 35 (7.2%)

EXPERIENCE LEVEL DISTRIBUTION
Junior....................................... 124 (25.5%)
Mid-level................................... 198 (40.7%)
Senior...................................... 89 (18.3%)
Not specified............................... 76 (15.6%)
```

**Output files**:
- `analysis/analysis_report.json`
- `analysis/analysis_report.txt`

---

## 📊 Expected Total Results

**After all 4 steps complete:**

| File | Size | Format | Purpose |
|------|------|--------|---------|
| `data/raw/job_links.csv` | 100KB | CSV | Job URLs |
| `data/final/jobs.json` | 1.2MB | JSON | Raw extracted data |
| `data/final/jobs.csv` | 800KB | CSV | Raw extracted data |
| `data/final/jobs_cleaned.csv` | 700KB | CSV | Cleaned data |
| `data/final/jobs_cleaned.json` | 900KB | JSON | Cleaned data |
| `analysis/analysis_report.json` | 50KB | JSON | Analysis results |
| `analysis/analysis_report.txt` | 30KB | TXT | Formatted report |

**Total Time**: ~45 minutes  
**Total Data**: ~4MB  
**Jobs Extracted**: 1,000-5,000+  
**Data Points**: 487 cleaned job records  

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] `data/raw/job_links.csv` exists and has 1,000+ rows
- [ ] `data/final/jobs.json` exists and is 1MB+
- [ ] `data/final/jobs_cleaned.csv` exists and is 600KB+
- [ ] `analysis/analysis_report.txt` exists and shows results
- [ ] Console shows analysis summary
- [ ] No error messages in final output

---

## 🐛 Troubleshooting

### Problem: "Python not found"
**Solution:**
1. Download Python from https://www.python.org/
2. Run installer
3. **CHECK: "Add Python to PATH"**
4. Restart terminal
5. Try again

### Problem: "ChromeDriver not found"
**Solution:**
1. Download from https://chromedriver.chromium.org/
2. Place in `C:\Program Files\` or project root
3. Or add directory to Windows PATH
4. Restart terminal

### Problem: Selenium timeout
**Solution:**
1. Check internet connection
2. Try increasing wait times in `selenium/utils.py`
3. Check if websites are accessible

### Problem: Scrapy spider won't start
**Solution:**
1. Verify Selenium completed (check CSV exists)
2. Ensure CSV path is correct
3. Check for typos in command

### Problem: Data cleaner crashes
**Solution:**
1. Verify previous steps completed
2. Check CSV file format
3. Ensure all headers are present

---

## 🔄 Quick Restart

If you need to restart from a specific step:

```powershell
# Just run Step 2 (assuming Step 1 completed)
cd c:\Users\Administrator\Documents\UCP\6\T and T\Assignment1\scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json

# Just run Step 3 (assuming Step 1-2 completed)
cd c:\Users\Administrator\Documents\UCP\6\T and T\Assignment1\analysis
python data_cleaner.py

# Just run Step 4 (final analysis)
python analyze_jobs.py
```

---

## 📝 Full Script (All-in-One)

Create a file named `run_all.ps1` with this content:

```powershell
# Run all steps automatically
Write-Host "Starting job scraping pipeline..." -ForegroundColor Green

$basePath = "c:\Users\Administrator\Documents\UCP\6\T and T\Assignment1"
cd $basePath

# Step 1: Selenium
Write-Host "`n=== STEP 1: Selenium Scraper ===" -ForegroundColor Yellow
cd selenium
python main_scraper.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error in Selenium. Exiting." -ForegroundColor Red
    exit 1
}

# Step 2: Scrapy
Write-Host "`n=== STEP 2: Scrapy Spider ===" -ForegroundColor Yellow
cd ../scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error in Scrapy. Exiting." -ForegroundColor Red
    exit 1
}

# Step 3: Cleaning
Write-Host "`n=== STEP 3: Data Cleaning ===" -ForegroundColor Yellow
cd ../analysis
python data_cleaner.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error in Cleaning. Exiting." -ForegroundColor Red
    exit 1
}

# Step 4: Analysis
Write-Host "`n=== STEP 4: Analysis ===" -ForegroundColor Yellow
python analyze_jobs.py

Write-Host "`n=== ALL STEPS COMPLETE ===" -ForegroundColor Green
Write-Host "Results saved to:" -ForegroundColor Cyan
Write-Host "  - data/raw/job_links.csv" -ForegroundColor Cyan
Write-Host "  - data/final/jobs_cleaned.csv" -ForegroundColor Cyan
Write-Host "  - analysis/analysis_report.txt" -ForegroundColor Cyan
```

Then run with:
```powershell
.\run_all.ps1
```

---

## 🎯 Summary

**Before you start:**
1. Install Python
2. Install ChromeDriver
3. Create virtual environment
4. Install dependencies

**To run:**
```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run Step 1
cd selenium && python main_scraper.py

# Run Step 2
cd ../scrapy_project && scrapy crawl jobs -o ../data/final/jobs.json

# Run Step 3
cd ../analysis && python data_cleaner.py

# Run Step 4
python analyze_jobs.py
```

**Expected result:** Job market analysis complete in ~45 minutes!

---

For more details, see:
- `START_HERE.md` - Welcome guide
- `docs/QUICKSTART.md` - 5-minute quick start
- `docs/SETUP.md` - Detailed setup guide
- `README.md` - Full documentation
