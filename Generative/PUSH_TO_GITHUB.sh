#!/bin/bash

# MARGDARSHAN Platform GitHub Push Script
# This script helps you push the MARGDARSHAN Career Guidance Platform to GitHub

echo "=== MARGDARSHAN Platform GitHub Push Script ==="
echo ""

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo "Error: This script must be run from the Git repository root directory"
    exit 1
fi

# Check current status
echo "Checking repository status..."
git status

echo ""
echo "=== Instructions ==="
echo "To push this repository to GitHub, follow these steps:"
echo ""
echo "1. Go to https://github.com/new and create a new repository"
echo "   - Name it something like 'margdarshan-career-platform'"
echo "   - Make it Public or Private as you prefer"
echo "   - DO NOT initialize with a README"
echo "   - Click 'Create repository'"
echo ""
echo "2. Copy the repository URL (it will look like: https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)"
echo ""
echo "3. Run the following commands in your terminal:"
echo ""
echo "   cd /Users/raheedpasha/Mini_Project/Generative"
echo "   git remote add origin YOUR_REPOSITORY_URL"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "=== Alternative: Using GitHub CLI (if installed) ==="
echo "If you have GitHub CLI installed, you can run:"
echo ""
echo "   gh repo create margdarshan-career-platform --public --source=. --push"
echo ""
echo "=== Deployment Options ==="
echo "After pushing to GitHub, you can deploy using:"
echo ""
echo "Frontend (React):"
echo "  - Vercel: https://vercel.com"
echo "  - Netlify: https://netlify.com"
echo ""
echo "Backend (FastAPI):"
echo "  - Heroku: https://heroku.com"
echo "  - Render: https://render.com"
echo ""
echo "The repository is ready with all documentation and code."
echo "Enjoy your professional MARGDARSHAN Career Guidance Platform!"