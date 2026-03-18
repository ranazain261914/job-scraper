# QUICK REFERENCE CARD

## 🚀 Start Here (Choose One)

### Option 1: Get Running in 5 Minutes
```bash
Read: docs/QUICKSTART.md
Then: Follow 5 steps to run everything
```

### Option 2: Understand First
```bash
Read: README.md
Then: Read docs/SETUP.md if needed
Finally: Run the system
```

### Option 3: Full Deep Dive
```bash
Read: docs/SETUP.md (installation)
Read: docs/GIT_WORKFLOW.md (workflow)
Read: README.md (project guide)
Explore: Code with comments
```

---

## ⚡ Quick Commands

### Setup (First Time Only)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run All Steps
```powershell
# 1. Selenium Scraper (5-15 min)
cd selenium
python main_scraper.py

# 2. Scrapy Spider (10-30 min)
cd ../scrapy_project
scrapy crawl jobs -o ../data/final/jobs.json

# 3. Data Cleaning (1 min)
cd ../analysis
python data_cleaner.py

# 4. Analysis (1 min)
python analyze_jobs.py
```

### Check Results
```powershell
# View extracted jobs
python -c "import pandas as pd; print(pd.read_csv('../data/final/jobs.csv').head())"

# View analysis
cat analysis_report.txt
```

---

## 📁 Important Files

| File | Purpose | Edit? |
|------|---------|-------|
| `selenium/main_scraper.py` | Run Selenium | No |
| `scrapy_project/spiders/jobs.py` | Extract data | Maybe* |
| `analysis/data_cleaner.py` | Clean data | Maybe* |
| `analysis/analyze_jobs.py` | Analyze results | Maybe* |
| `requirements.txt` | Dependencies | No |
| `README.md` | Guide | No |

*Maybe = Only if you want to customize

---

## 🔍 Expected Output Files

| File | Created After Step | Size |
|------|-------------------|------|
| `data/raw/job_links.csv` | Selenium | 100KB-500KB |
| `data/final/jobs.json` | Scrapy | 500KB-2MB |
| `data/final/jobs.csv` | Scrapy | 200KB-1MB |
| `data/final/jobs_cleaned.csv` | Cleaning | 200KB-1MB |
| `analysis/analysis_report.json` | Analysis | 50KB-200KB |
| `analysis/analysis_report.txt` | Analysis | 20KB-50KB |

---

## 🛠️ Troubleshooting

### Selenium Won't Start
```
ERROR: chromedriver not found
FIX: Download from https://chromedriver.chromium.org/
     or place in project root
```

### Scrapy Can't Find CSV
```
ERROR: FileNotFoundError: data/raw/job_links.csv
FIX: Run selenium/main_scraper.py first
```

### Analysis Shows No Data
```
ERROR: No data to analyze
FIX: Run all previous steps first
     Check file paths
```

### Port Already in Use
```
ERROR: Address already in use
FIX: Kill Chrome process or restart computer
```

---

## 📊 What You'll See

### Selenium Output
```
Starting Greenhouse scraper...
Navigating to Greenhouse board...
Searching for: Software Engineer
Found job link: https://...
Total unique jobs found: 245
✓ Greenhouse scraper completed: 245 links found
```

### Scrapy Output
```
2026-03-18 10:30:00 [scrapy.spiders] INFO: Spider opened
2026-03-18 10:30:05 [scrapy.spiders] DEBUG: Parsing job from greenhouse: https://...
2026-03-18 10:35:00 [scrapy.statscollectors] INFO: Dumping Scrapy stats
```

### Analysis Output
```
EXECUTIVE SUMMARY
Total Job Listings: 1,245
Unique Companies: 324
Unique Locations: 87

TOP 20 REQUIRED SKILLS
1. Python........................................ 342 jobs
2. JavaScript................................... 298 jobs
3. React......................................... 267 jobs
...
```

---

## 🔑 Key Configuration Points

### Customize Search Queries
**File:** `selenium/greenhouse_scraper.py`
```python
SEARCH_QUERIES = [
    "Software Engineer",    # Change these
    "Data Analyst",
    "Intern",
    "QA Engineer"
]
```

### Customize Skill Keywords
**File:** `analysis/analyze_jobs.py` (line ~280)
```python
skills_keywords = {
    'Python': ['python', 'py'],
    'JavaScript': ['javascript', 'js'],
    # Add more skills here
}
```

### Customize Wait Times
**File:** `selenium/utils.py` (line ~42)
```python
timeout=10  # Increase if you get timeouts
```

### Customize Analysis Output
**File:** `analysis/analyze_jobs.py` (line ~180)
```python
.head(20)  # Change number of top results
```

---

## 📚 Documentation Map

```
START HERE
    ↓
README.md (Project overview)
    ↓
Choose your path:
    ├─→ Want to get running? → docs/QUICKSTART.md
    ├─→ Need setup help? → docs/SETUP.md
    ├─→ Want Git info? → docs/GIT_WORKFLOW.md
    └─→ Want full details? → Read all docs
```

---

## ✅ Checklist Before Running

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Chrome installed (or Firefox)
- [ ] ChromeDriver in PATH or project root
- [ ] Virtual environment activated (`.\venv\Scripts\Activate.ps1`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Internet connection working
- [ ] 45 minutes free time

---

## 🎯 Success Criteria

✅ **Selenium Complete When:**
- Chrome opens and closes
- `data/raw/job_links.csv` exists
- Contains 1000+ URLs

✅ **Scrapy Complete When:**
- Spider runs without errors
- `data/final/jobs.csv` exists
- Contains job details

✅ **Cleaning Complete When:**
- No errors in console
- `data/final/jobs_cleaned.csv` exists
- File size is reasonable

✅ **Analysis Complete When:**
- Console shows report
- `analysis_report.txt` exists
- Contains top skills, companies, locations

---

## 🆘 Quick Help

### "I'm stuck!"
1. Check the relevant doc (above map)
2. Search for error in docs/SETUP.md
3. Read code comments in the file
4. Check if requirements.txt packages are installed

### "I want to modify X"
1. Find the file listed above
2. Read the docstring at the top
3. Read inline comments
4. Make your change
5. Test it

### "I want to add feature Y"
1. Read docs/GIT_WORKFLOW.md
2. Create feature branch
3. Make changes
4. Commit with clear message
5. Merge back to develop

---

## 📞 Support Resources

| Need | Resource |
|------|----------|
| Installation help | `docs/SETUP.md` |
| Quick start | `docs/QUICKSTART.md` |
| Error messages | `docs/SETUP.md` → Troubleshooting |
| Code explanation | Read file comments |
| Git commands | `docs/GIT_WORKFLOW.md` |
| Features list | `RELEASE_NOTES.md` |
| Project stats | `PROJECT_COMPLETION.md` |

---

## 🎓 Learning Path

1. **Beginner (30 min)**
   - Read README.md
   - Run QUICKSTART.md
   - Examine output files

2. **Intermediate (2 hours)**
   - Read SETUP.md
   - Read relevant code files
   - Understand architecture
   - Customize search queries

3. **Advanced (4 hours)**
   - Read GIT_WORKFLOW.md
   - Understand Git history
   - Modify scraping logic
   - Add new analyses

4. **Expert (ongoing)**
   - Add new job boards
   - Integrate database
   - Build API/Dashboard
   - Implement ML features

---

## 💾 File Backups

Important: Before running, backup these if you modify:
```
selenium/
  ├─ greenhouse_scraper.py
  ├─ lever_scraper.py
  ├─ ashby_scraper.py
  └─ utils.py

scrapy_project/spiders/
  └─ jobs.py

analysis/
  ├─ data_cleaner.py
  └─ analyze_jobs.py
```

---

## 🚨 Common Mistakes

❌ **Don't:** Run Scrapy before Selenium  
✅ **Do:** Complete Selenium first

❌ **Don't:** Close Chrome until fully done  
✅ **Do:** Let it run completely

❌ **Don't:** Modify .gitignore unless you know Git  
✅ **Do:** Leave configuration files alone

❌ **Don't:** Run multiple instances simultaneously  
✅ **Do:** Complete one run before starting another

❌ **Don't:** Skip reading error messages  
✅ **Do:** Read and understand errors

---

## 🎉 Success!

When everything works:
1. You have clean job data (CSV/JSON)
2. You have analysis reports
3. You understand the job market
4. You can modify and extend the system

**Congratulations! You've built a job scraping system!**

---

## 📖 Next Read

Choose based on your next step:
- **Want to run it?** → `docs/QUICKSTART.md`
- **Having issues?** → `docs/SETUP.md`
- **Want to understand?** → `README.md`
- **Want to contribute?** → `docs/GIT_WORKFLOW.md`

---

**Quick Tip:** Keep this card handy while running!
