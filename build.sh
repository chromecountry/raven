#!/bin/bash

# Build script for Render deployment

echo "Setting up Raven Receipt Processor..."

# Create necessary directories
mkdir -p data/ledger data/attachments data/exports logs

# Create empty ledger file if it doesn't exist
if [ ! -f "data/ledger/ledger.beancount" ]; then
    echo "Creating empty ledger file..."
    touch data/ledger/ledger.beancount
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r cfg/prd/requirements.txt

# Install system dependencies for OCR
echo "Installing system dependencies..."
apt-get update -y
apt-get install -y tesseract-ocr

echo "Build completed successfully!" 