#!/bin/bash

# MARGDARSHAN Platform GitHub Repository Creation and Push Script
# This script helps you create a GitHub repository and push the MARGDARSHAN Career Guidance Platform

echo "=== MARGDARSHAN Platform GitHub Repository Creation Script ==="
echo ""

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo "Error: This script must be run from the Git repository root directory"
    exit 1
fi

# Get repository name
echo "Enter the name for your GitHub repository (e.g., margdarshan-career-platform):"
read REPO_NAME

if [ -z "$REPO_NAME" ]; then
    REPO_NAME="margdarshan-career-platform"
    echo "Using default repository name: $REPO_NAME"
fi

# Get repository description
echo "Enter a description for your repository (or press Enter to skip):"
read REPO_DESCRIPTION

# Get repository visibility
echo "Should the repository be public or private? (public/private) [public]:"
read REPO_VISIBILITY

if [ "$REPO_VISIBILITY" != "private" ]; then
    REPO_VISIBILITY="public"
fi

echo ""
echo "=== Repository Details ==="
echo "Name: $REPO_NAME"
echo "Description: $REPO_DESCRIPTION"
echo "Visibility: $REPO_VISIBILITY"
echo ""

# Get GitHub personal access token
echo "To create a repository on GitHub, you need a personal access token."
echo "1. Go to https://github.com/settings/tokens"
echo "2. Click 'Generate new token'"
echo "3. Give it a name (e.g., 'margdarshan-repo-creator')"
echo "4. Select scopes: 'repo' (and 'delete_repo' if you want to allow deletion)"
echo "5. Click 'Generate token'"
echo "6. Copy the token (you won't see it again)"
echo ""
echo "Enter your GitHub personal access token:"
read -s GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "No token provided. You'll need to create the repository manually."
    echo "Run this script again with a valid token, or follow the manual steps:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named '$REPO_NAME'"
    echo "3. Run the following commands:"
    echo "   cd /Users/raheedpasha/Mini_Project/Generative"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    exit 1
fi

echo ""
echo "Creating repository on GitHub..."

# Create the repository using GitHub API
curl -f -u "$GITHUB_TOKEN:x-oauth-basic" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$REPO_NAME\",\"description\":\"$REPO_DESCRIPTION\",\"private\":$(if [ "$REPO_VISIBILITY" = "private" ]; then echo "true"; else echo "false"; fi)}" \
  https://api.github.com/user/repos

if [ $? -eq 0 ]; then
    echo "Repository created successfully!"
    
    # Get the username from the token
    USERNAME=$(curl -s -u "$GITHUB_TOKEN:x-oauth-basic" https://api.github.com/user | grep "\"login\":" | cut -d '"' -f 4)
    
    if [ -z "$USERNAME" ]; then
        echo "Could not determine GitHub username. Please enter it manually:"
        read USERNAME
    fi
    
    echo "Setting up remote repository..."
    git remote add origin https://github.com/$USERNAME/$REPO_NAME.git
    
    echo "Pushing code to GitHub..."
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=== SUCCESS ==="
        echo "Your MARGDARSHAN Career Guidance Platform has been pushed to GitHub!"
        echo "Repository URL: https://github.com/$USERNAME/$REPO_NAME"
        echo ""
        echo "Next steps:"
        echo "1. Visit your repository at https://github.com/$USERNAME/$REPO_NAME"
        echo "2. For deployment:"
        echo "   - Frontend: Connect to Vercel or Netlify"
        echo "   - Backend: Deploy to Heroku or Render"
        echo ""
        echo "The repository contains all documentation and code for your platform."
    else
        echo "Failed to push code. You may need to push manually:"
        echo "git push -u origin main"
    fi
else
    echo "Failed to create repository. You may need to create it manually:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named '$REPO_NAME'"
    echo "3. Run the following commands:"
    echo "   cd /Users/raheedpasha/Mini_Project/Generative"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
fi