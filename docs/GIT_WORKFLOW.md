# Git Workflow Guide

## Overview

This project follows a professional Git branching strategy with:
- `main` - Production-ready code (stable releases)
- `develop` - Development integration branch
- Feature branches - Individual feature development
- Bugfix branches - Bug fixes
- Release branches - Release preparation

## Branch Structure

```
main
└── release/v1.0
    └── develop
        ├── feature/selenium-scraper ✓ (merged)
        ├── feature/scrapy-parser ✓ (merged)
        ├── feature/data-cleaning ✓ (merged)
        ├── bugfix/issue-name (if needed)
        └── [future features...]
```

## Current Status

✅ **Merged Features:**
- feature/selenium-scraper - Selenium web scrapers
- feature/scrapy-parser - Scrapy spiders and pipelines
- feature/data-cleaning - Data cleaning and analysis

⏳ **In Progress:**
- Preparing v1.0 release

## How to Work with Branches

### 1. View All Branches

```bash
git branch -a
```

Output:
```
* develop
  feature/selenium-scraper
  feature/scrapy-parser
  feature/data-cleaning
  master
```

### 2. Check Current Branch

```bash
git branch --show-current
# or
git status
```

### 3. Create a New Feature Branch

```bash
# From develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/new-feature develop

# Make changes...
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature
```

### 4. Merge Feature into Develop

```bash
# Switch to develop
git checkout develop

# Merge with --no-ff flag (keeps history)
git merge --no-ff feature/new-feature -m "Merge feature/new-feature into develop"

# Delete feature branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### 5. Create a Bugfix Branch

```bash
git checkout -b bugfix/issue-name develop

# Fix the bug...
git add .
git commit -m "Fix: Describe the fix"

# Merge back
git checkout develop
git merge --no-ff bugfix/issue-name -m "Merge bugfix/issue-name into develop"
git branch -d bugfix/issue-name
```

## Commit Messages

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add Selenium scraper for Greenhouse job boards"
git commit -m "Fix: Handle missing job descriptions in parser"
git commit -m "Refactor: Improve data cleaning pipeline"
git commit -m "Docs: Update installation guide"

# Message format
git commit -m "TYPE: Description"

# Types:
# - Add: New feature
# - Fix: Bug fix
# - Refactor: Code refactoring
# - Docs: Documentation
# - Test: Test additions
# - Chore: Build, dependencies, etc.
```

## Merge Strategies

### Using --no-ff (Recommended)

```bash
git merge --no-ff feature/name
```

**Advantages:**
- Preserves branch history
- Easy to revert entire features
- Clear project timeline

**Result:**
```
* commit (merge commit)
|\ 
| * feature commits
|/
* previous commits
```

### Without --no-ff (Fast-forward)

```bash
git merge feature/name
```

**Result:**
```
* feature commits
* previous commits
```

## Git Log Viewing

```bash
# View all commits
git log --oneline

# View with branch graph
git log --oneline --graph --all

# View commits for a file
git log --oneline src/file.py

# View detailed info
git log -p

# View last 5 commits
git log -n 5
```

## Reverting Changes

### Undo Last Commit (Not Pushed)

```bash
git reset --soft HEAD~1
```

### Undo Changes in a File

```bash
git checkout -- path/to/file.py
```

### Revert a Merged Feature

```bash
git revert -m 1 <merge-commit-hash>
```

## Stashing Changes

Save work without committing:

```bash
# Stash current changes
git stash

# List stashed changes
git stash list

# Apply stashed changes
git stash apply

# Apply and remove stash
git stash pop

# Discard stash
git stash drop
```

## Release Process

### Creating a Release (v1.0)

```bash
# Ensure develop is up to date
git checkout develop
git pull origin develop

# Switch to main
git checkout main
git pull origin main

# Merge develop into main
git merge --no-ff develop -m "Release v1.0"

# Tag the release
git tag -a v1.0 -m "Release version 1.0"

# Push to remote
git push origin main
git push origin v1.0
```

### Release Tags

View tags:
```bash
git tag -l
```

View tag details:
```bash
git show v1.0
```

Checkout specific version:
```bash
git checkout v1.0
```

## Remote Repository

### Setup Remote

```bash
# Add remote
git remote add origin https://github.com/user/job-scraper.git

# View remotes
git remote -v

# Change remote URL
git remote set-url origin https://new-url.git
```

### Push and Pull

```bash
# Push branch
git push origin feature/name

# Pull latest
git pull origin main

# Fetch without merging
git fetch origin
```

## GitHub Pull Request Workflow

If using GitHub:

```bash
# 1. Push feature branch
git push origin feature/name

# 2. Go to GitHub
# - Click "Compare & pull request"
# - Add description
# - Request reviewers

# 3. After approval, merge on GitHub
# (Use "Create a merge commit" option)

# 4. Sync local repo
git checkout develop
git pull origin develop
```

## Best Practices

✅ **DO:**
- Use feature branches for all work
- Write clear commit messages
- Pull before pushing
- Use `--no-ff` for merges
- Tag releases
- Review code before merging
- Keep branches up to date

❌ **DON'T:**
- Commit directly to main
- Use vague commit messages ("fixed stuff")
- Ignore merge conflicts
- Force push to shared branches
- Leave stale branches

## Git Configuration

### Setup (First Time)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Useful Aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'
```

## Troubleshooting

### Merge Conflicts

```bash
# View conflicts
git status

# Edit conflicted files manually
# Look for <<<<<<, ======, >>>>>>

# After fixing
git add .
git commit -m "Resolve merge conflicts"
```

### Accidentally Committed to Wrong Branch

```bash
# Create new branch from current
git branch recovery-branch

# Reset main branch to before commit
git reset --hard HEAD~1

# Switch to recovery branch
git checkout recovery-branch
```

### Need to Update Feature Branch

```bash
git checkout feature/name
git fetch origin
git rebase origin/develop
# or
git merge develop
```

## Current Project Status

### Merged Branches
```bash
git branch --merged develop
```

**Output:**
```
develop
feature/selenium-scraper
feature/scrapy-parser
feature/data-cleaning
```

### Ready for Release
- ✅ All features merged to develop
- ✅ Tests passing
- ✅ Documentation complete
- ⏳ Ready to merge to main and tag v1.0

---

For more info: https://git-scm.com/book/
