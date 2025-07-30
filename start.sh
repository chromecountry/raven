#!/bin/bash

# Startup script for Render deployment

echo "Starting Raven Receipt Processor..."

# Ensure directories exist
mkdir -p data/ledger data/attachments data/exports logs

# Create empty ledger file if it doesn't exist
if [ ! -f "data/ledger/ledger.beancount" ]; then
    echo "Creating empty ledger file..."
    touch data/ledger/ledger.beancount
fi

# Set environment variables
export FAVA_HOST=0.0.0.0
export FAVA_PORT=$PORT

echo "Starting Fava on port $PORT..."
echo "Ledger file: data/ledger/ledger.beancount"

# Start Fava
exec fava --host 0.0.0.0 --port $PORT data/ledger/ledger.beancount 