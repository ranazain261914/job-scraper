@echo off
REM Git Configuration and GitHub Push Script
REM This script prepares your project for GitHub and pushes it

echo.
echo ============================================================
echo     GIT GITHUB PUSH SETUP SCRIPT
echo ============================================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    exit /b 1
)
echo [OK] Git is installed

REM Show current directory
echo Current Directory: %cd%

REM Check if .git directory exists
if not exist .git (
    echo ERROR: Not in a Git repository
    exit /b 1
)
echo [OK] Git repository found

REM Check current user config
echo.
echo Current Git Configuration:
echo ========================
git config --global user.name
git config --global user.email
echo.

REM Rename master to main
echo Renaming master branch to main...
git branch -m master main 2>nul
if errorlevel 0 (
    echo [OK] Branch renamed to main
) else (
    echo [INFO] Branch is already main
)

REM Show current state
echo.
echo Current Repository State:
echo =========================
echo.
echo Branches:
git branch -a
echo.
echo Remote:
git remote -v
if errorlevel 1 (
    echo [INFO] No remote configured yet
)
echo.
echo Recent Commits:
git log --oneline -5
echo.

REM Instructions
echo.
echo ============================================================
echo NEXT STEPS TO PUSH TO GITHUB:
echo ============================================================
echo.
echo 1. Create a GitHub account (free): https://github.com
echo.
echo 2. Create Personal Access Token:
echo    - Go to https://github.com/settings/tokens
echo    - Click "Generate new token (classic)"
echo    - Name: job-scraper-token
echo    - Check: repo, workflow
echo    - Click "Generate token"
echo    - SAVE IT SOMEWHERE SAFE!
echo.
echo 3. Create new repository on GitHub:
echo    - Go to https://github.com/new
echo    - Name: job-scraper
echo    - Description: "Job listing web scraper with analysis"
echo    - Click "Create repository"
echo.
echo 4. Add remote and push (run in PowerShell):
echo    
echo    $username = Read-Host 'Enter your GitHub username'
echo    git remote add origin "https://github.com/$username/job-scraper.git"
echo    git push -u origin main
echo    (Paste your token when asked for password)
echo.
echo 5. Verify at:
echo    https://github.com/[your-username]/job-scraper
echo.
echo ============================================================

pause
