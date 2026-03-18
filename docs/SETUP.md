# Installation and Setup Guide

## Prerequisites

Before starting, ensure you have the following installed:

1. **Python 3.8+**
   - Check: `python --version`
   - Download from: https://www.python.org/

2. **pip** (Python package manager)
   - Usually comes with Python
   - Check: `pip --version`

3. **Google Chrome or Firefox**
   - Required for Selenium browser automation
   - Download from: https://www.google.com/chrome/ or https://www.mozilla.org/firefox/

4. **ChromeDriver** (if using Chrome)
   - Download: https://chromedriver.chromium.org/
   - Choose version matching your Chrome version
   - Add to PATH or place in project root

## Step 1: Clone/Download Project

```bash
# Navigate to your desired directory
cd path/to/projects

# If cloned from Git
git clone <repository-url>
cd job-scraper

# Or if downloaded as ZIP, extract and navigate
cd job-scraper
```

## Step 2: Create Virtual Environment

Creating a virtual environment isolates project dependencies.

### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### On Windows (Command Prompt):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `selenium` - Web browser automation
- `scrapy` - Web scraping framework
- `pandas` - Data processing
- `requests` - HTTP library
- Other utilities

## Step 4: Setup WebDriver

### For Chrome (Recommended):

1. **Check your Chrome version:**
   - Open Chrome → Menu (⋮) → Help → About Google Chrome
   - Note your version number

2. **Download ChromeDriver:**
   - Visit: https://chromedriver.chromium.org/
   - Download the version matching your Chrome version
   - Extract the `chromedriver.exe` file

3. **Add to PATH (easiest method):**
   - Place `chromedriver.exe` in: `C:\Program Files\`
   - Or add its directory to Windows PATH

4. **Or place in project root:**
   - Put `chromedriver.exe` in the job-scraper project root directory

### For Firefox:

1. **Download GeckoDriver:**
   - Visit: https://github.com/mozilla/geckodriver/releases
   - Download for Windows/Mac/Linux

2. **Add to PATH or project root**

## Step 5: Verify Installation

Test that everything is working:

```bash
# Test Python
python --version

# Test pip
pip list

# Test Selenium (optional)
python -c "from selenium import webdriver; print('Selenium OK')"

# Test Scrapy (optional)
python -c "import scrapy; print('Scrapy OK')"
```

## Step 6: Configure API Keys (If Needed)

If you plan to use any APIs in the future, create a `.env` file:

```bash
# In project root, create .env file
API_KEY=your_api_key_here
PROXY_URL=proxy_if_needed
```

Then load in Python:
```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('API_KEY')
```

## Running the Project

### Option 1: Run Everything (Automated)

Create a `run_all.sh` (macOS/Linux) or `run_all.bat` (Windows) script:

```bash
# Windows (run_all.bat)
cd selenium
python main_scraper.py
cd ..

cd scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json

cd ../analysis
python data_cleaner.py
python analyze_jobs.py
```

### Option 2: Step-by-Step Manual Execution

**Step 1: Run Selenium Scraper**
```bash
cd selenium
python main_scraper.py
# Duration: 5-15 minutes
# Output: /data/raw/job_links.csv
```

**Step 2: Run Scrapy Spider**
```bash
cd ../scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json
# Duration: 10-30 minutes
# Output: /data/final/jobs.json and jobs.csv
```

**Step 3: Clean Data**
```bash
cd ../analysis
python data_cleaner.py
# Output: /data/final/jobs_cleaned.csv
```

**Step 4: Analyze Results**
```bash
python analyze_jobs.py
# Output: analysis_report.json and analysis_report.txt
```

## Troubleshooting

### ChromeDriver Issues

**Error: "chromedriver not in PATH"**
```bash
# Option 1: Add to PATH
setx PATH "%PATH%;C:\Path\To\ChromeDriver"

# Option 2: Download and place in project root
# Then modify selenium/utils.py to specify path:
# driver = webdriver.Chrome('./chromedriver.exe')
```

**Error: "Chrome version mismatch"**
- Download the correct ChromeDriver version matching your Chrome version
- Chrome version must match ChromeDriver version

### Selenium Timeouts

If you get timeout errors:
- Increase wait times in selenium scripts
- Check internet connection
- Ensure websites are accessible
- Check for CAPTCHA blocks

Example in code:
```python
wait = WebDriverWait(driver, 20)  # Increase from 10 to 20 seconds
```

### Scrapy Issues

**"Spider not parsing data"**
- Website HTML structure may have changed
- Inspect page and update CSS selectors
- Check `jobs_spider/spiders/jobs.py`

**"CSV not found"**
- Ensure Selenium scraper completed successfully
- Check `/data/raw/job_links.csv` exists

### Virtual Environment Issues

**"Python: command not found"**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
venv\Scripts\activate.bat    # Windows CMD
source venv/bin/activate     # macOS/Linux
```

**"pip not recognized"**
```bash
# Use Python module method
python -m pip install -r requirements.txt
```

## Performance Tips

1. **Reduce scan scope** - Modify search queries in scraper files
2. **Use headless mode** - Change `headless=True` in main_scraper.py
3. **Increase delays** - Avoid server blocks by using respectful delays
4. **Parallel processing** - For Scrapy, increase CONCURRENT_REQUESTS in settings.py
5. **Cache results** - Use HTTP cache to avoid re-downloading

## Next Steps

1. ✅ Install dependencies
2. ✅ Setup WebDriver
3. ✅ Run Selenium scraper
4. ✅ Run Scrapy spider
5. ✅ Run analysis

See `README.md` for full project documentation.

## Support

For issues:
1. Check logs in terminal output
2. Verify prerequisites are installed
3. Check website accessibility
4. Review code comments for guidance
5. Check HTML structure if selectors fail

## Environment Details

- **Python Version:** 3.8+
- **OS:** Windows, macOS, Linux
- **Browser:** Chrome or Firefox
- **Database:** None (CSV/JSON only)

---

**Last Updated:** March 2026
