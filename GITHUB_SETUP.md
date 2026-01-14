# GitHub Setup - Make Sure It's Public!

## Step-by-Step Instructions

### 1. Create Repository on GitHub

1. Go to https://github.com/new
2. **Repository name:** `nc-file-processor` (or whatever you prefer)
3. **Description:** "Simple Windows GUI for processing NC/G-code files"
4. **⚠️ IMPORTANT: Select "Public" (not Private)!**
5. **DO NOT** check "Initialize with README" (we already have files)
6. Click "Create repository"

### 2. Push Your Code

```bash
cd /Users/jorml/nc_file_processor

# If you haven't committed yet:
git add .
git commit -m "Initial commit: NC File Processor with drag-and-drop support"

# Add your GitHub remote (replace YOUR_USERNAME and REPO_NAME):
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub:
git branch -M main
git push -u origin main
```

### 3. Verify It's Public

After pushing:
- Go to your repository on GitHub
- Look for a **"Public"** badge next to the repository name
- If you see "Private", go to: **Settings → General → Danger Zone → Change repository visibility → Make public**

### Quick Check

You can also check by visiting your repo URL - if it's public, anyone can view it without logging in!
