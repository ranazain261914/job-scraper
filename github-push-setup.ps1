# GitHub Push Setup Script for PowerShell
# This script configures and prepares your project for GitHub

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "  GIT GITHUB PUSH SETUP SCRIPT" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Green

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "[OK] Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if in a Git repository
if (-not (Test-Path .git)) {
    Write-Host "[ERROR] Not in a Git repository" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Git repository found" -ForegroundColor Green

# Show current directory
Write-Host "`nCurrent Directory: $(Get-Location)" -ForegroundColor Yellow

# Show current Git configuration
Write-Host "`nCurrent Git Configuration:" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
$userName = git config --global user.name
$userEmail = git config --global user.email
Write-Host "Username: $userName"
Write-Host "Email: $userEmail"

# Rename branch to main
Write-Host "`nRenaming branch to main (if needed)..." -ForegroundColor Yellow
git branch -m master main 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Branch renamed to main" -ForegroundColor Green
} else {
    Write-Host "[INFO] Branch is already main" -ForegroundColor Cyan
}

# Show current state
Write-Host "`nCurrent Repository State:" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

Write-Host "`nBranches:" -ForegroundColor Yellow
git branch -a

Write-Host "`nRemote:" -ForegroundColor Yellow
$remotes = git remote -v
if ($remotes) {
    Write-Host $remotes
} else {
    Write-Host "[INFO] No remote configured yet" -ForegroundColor Cyan
}

Write-Host "`nRecent Commits:" -ForegroundColor Yellow
git log --oneline -5

# Main instructions
Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "NEXT STEPS TO PUSH TO GITHUB:" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Green

$steps = @"
STEP 1: Create a GitHub Account (if you don't have one)
   → Go to https://github.com
   → Sign up for free
   → Verify your email

STEP 2: Create Personal Access Token
   → Go to https://github.com/settings/tokens
   → Click "Generate new token (classic)"
   → Fill in:
      Name: job-scraper-token
      Scopes: ✓ repo, ✓ workflow
   → Click "Generate token"
   → COPY AND SAVE THE TOKEN (you won't see it again!)
   
STEP 3: Create New Repository on GitHub
   → Go to https://github.com/new
   → Fill in:
      Repository name: job-scraper
      Description: Job listing web scraper with Selenium, Scrapy, and analysis
      Visibility: Public (recommended)
   → Click "Create repository"
   → Do NOT initialize with README, gitignore, or license

STEP 4: Add Remote and Push to GitHub
   Run the following commands:

   `$github_username = Read-Host 'Enter your GitHub username'
   git remote add origin "https://github.com/`$github_username/job-scraper.git"
   git branch -m main master 2>$null
   git branch -m master main
   git push -u origin main

   When prompted:
   → Username: git (or your GitHub username)
   → Password: Paste your Personal Access Token (NOT your password!)

STEP 5: Verify Your Repository
   → Go to https://github.com/[your-username]/job-scraper
   → You should see all 21 commits and files

OPTIONAL - NEXT ACTIONS:
   • Enable GitHub Pages for documentation
   • Add repository description and topics
   • Invite collaborators
   • Set up GitHub Actions for CI/CD
"@

Write-Host $steps

Write-Host "============================================================`n" -ForegroundColor Green

# Offer to proceed
$proceed = Read-Host "Do you want to add GitHub remote now? (yes/no)"

if ($proceed -eq "yes" -or $proceed -eq "y") {
    $username = Read-Host "Enter your GitHub username"
    $repoUrl = "https://github.com/$username/job-scraper.git"
    
    Write-Host "`nAdding remote: $repoUrl" -ForegroundColor Yellow
    git remote add origin $repoUrl
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Remote added successfully" -ForegroundColor Green
        Write-Host "`nVerifying remote:" -ForegroundColor Yellow
        git remote -v
        
        Write-Host "`nReady to push! Run:" -ForegroundColor Green
        Write-Host "   git push -u origin main" -ForegroundColor Cyan
    } else {
        Write-Host "[ERROR] Failed to add remote" -ForegroundColor Red
        Write-Host "This might mean the remote already exists. Check with: git remote -v" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nSkipped. Run this script again when ready!" -ForegroundColor Cyan
}

Write-Host "`n"
