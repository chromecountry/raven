#!/bin/bash

# Raven - Vercel Deployment Script
# This script prepares the project for Vercel deployment

set -e

echo "Preparing Raven for Vercel deployment..."
echo "========================================"

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
    echo "  git commit -m 'Prepare for Vercel deployment'"
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
echo ""
echo "📋 Next steps for Vercel deployment:"
echo ""
echo "1. Push to GitHub:"
echo "   git push origin main"
echo ""
echo "2. Go to https://vercel.com"
echo "3. Click 'New Project'"
echo "4. Import your GitHub repository"
echo "5. Deploy!"
echo ""
echo "🌐 Your app will be live at: https://your-project-name.vercel.app"
echo ""
echo "📚 See DEPLOYMENT_VERCEL.md for detailed instructions"
echo ""
echo "🚀 Ready for deployment!" 