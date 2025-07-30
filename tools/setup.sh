#!/bin/bash

# Receipt Processing System Setup Script

set -e

echo "Setting up Receipt Processing System..."
echo "======================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r cfg/prd/requirements.txt

# Create credentials file if it doesn't exist
if [ ! -f "src/core/credentials.py" ]; then
    echo "Creating credentials file from template..."
    cp src/core/credentials.py.skel src/core/credentials.py
    echo "Please edit src/core/credentials.py with your actual credentials"
fi

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/ledger data/attachments data/exports logs

# Create empty ledger file if it doesn't exist
if [ ! -f "data/ledger/ledger.beancount" ]; then
    echo "Creating empty ledger file..."
    touch data/ledger/ledger.beancount
fi

echo ""
echo "Setup complete!"
echo "Next steps:"
echo "1. Edit src/core/credentials.py with your email credentials"
echo "2. Run: python src/ui/main.py help"
echo "3. Run: python src/ui/main.py process-emails"
echo "4. Run: python src/ui/main.py launch-fava" 