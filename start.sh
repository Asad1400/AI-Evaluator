#!/bin/bash

# Quick Start Script for Automated Evaluation System
# This script helps you start both backend and frontend servers

echo "🎓 Automated Evaluation System - Quick Start"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Expected: /Users/asad/Desktop/Data Science Project/"
    exit 1
fi

echo "📋 Starting Backend Server..."
echo "   Location: http://localhost:8000"
echo "   Note: Models will download on first run (~1GB)"
echo ""

# Start backend in background
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Starting FastAPI server..."
uvicorn app.main:app --reload &
BACKEND_PID=$!

cd ..

echo ""
echo "⏳ Waiting for backend to start..."
sleep 5

echo ""
echo "🎨 Starting Frontend Server..."
echo "   Location: http://localhost:5173"
echo ""

cd frontend
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Both servers are starting!"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

wait
