#!/bin/bash
# Script to initialize git and prepare for GitHub push

echo "Setting up git repository for NC File Processor..."
echo ""

# Initialize git if not already done
if [ ! -d .git ]; then
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: NC File Processor with drag-and-drop support"

echo ""
echo "✓ Repository ready!"
echo ""
echo "Next steps to push to GitHub:"
echo "1. Create a new repository on GitHub (github.com/new)"
echo "   ⚠️  IMPORTANT: Make sure to select 'Public' (not Private)!"
echo "2. Run these commands (replace YOUR_USERNAME and REPO_NAME):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "To verify it's public, check the repository settings on GitHub:"
echo "   Settings → General → Danger Zone → Change repository visibility"
echo ""
