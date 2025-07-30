#!/bin/bash

# Raven - Simple Startup Script
# This script starts both the backend API and React frontend

set -e

echo "Starting Raven - Intelligent Receipt Processing System"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "api.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo "Shutting down services..."
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Handle virtual environment
if [ -d ".venv" ]; then
    echo "Using existing virtual environment"
else
    echo "Creating new virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install backend dependencies (skip if already installed)
echo "Checking backend dependencies..."
pip install -r cfg/dev/requirements.txt --quiet

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install --silent
    cd ..
else
    echo "Frontend dependencies already installed"
fi

# Start backend API
echo "Starting backend API server..."
python api.py &
API_PID=$!

# Wait a moment for API to start
sleep 3

# Check if API is running
if ! curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "Backend API failed to start"
    echo "Try running: python api.py"
    cleanup
fi

echo "Backend API started successfully on http://localhost:5000"

# Start React frontend
echo "Starting React frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "React frontend starting on http://localhost:3000"
echo ""
echo "🌐 Application URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   API Health: http://localhost:5000/api/health"
echo ""
echo "📋 Available Features:"
echo "   • Email receipt processing with time window filtering"
echo "   • PDF receipt parsing and storage"
echo "   • Bank statement upload and comparison"
echo "   • Transaction matching and reconciliation"
echo "   • Real-time dashboard with charts"
echo "   • Professional ledger view with data grid"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait 