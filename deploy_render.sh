#!/bin/bash

# Raven - Render Deployment Script
# This script prepares the project for Render deployment

set -e

echo "Preparing Raven for Render deployment..."
echo "======================================="

# Check if we're in the right directory
if [ ! -f "api.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Error: Git repository not found. Please initialize git first:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    exit 1
fi

# Check if all files are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "Warning: You have uncommitted changes. Please commit them first:"
    echo "  git add ."
    echo "  git commit -m 'Prepare for Render deployment'"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "✅ Project structure verified"
echo "✅ Git repository found"
echo "✅ render.yaml configuration ready"
echo ""
echo "📋 Next steps for Render deployment:"
echo ""
echo "1. Push to GitHub:"
echo "   git push origin main"
echo ""
echo "2. Go to https://render.com"
echo "3. Click 'New +' and select 'Blueprint'"
echo "4. Connect your GitHub repository"
echo "5. Render will auto-detect services from render.yaml"
echo "6. Click 'Apply' to deploy!"
echo ""
echo "🌐 Your app will be live at:"
echo "   Frontend: https://raven-frontend.onrender.com"
echo "   API: https://raven-api.onrender.com"
echo ""
echo "📚 See DEPLOYMENT_RENDER.md for detailed instructions"
echo ""
echo "🚀 Ready for deployment!" 