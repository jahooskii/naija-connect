#!/bin/bash

# Naija Connect - Quick Start Script
# Double-click this file to run the application

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║         🇳🇬 NAIJA CONNECT - STARTING APP 🇳🇬      ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Navigate to backend directory
cd "$BACKEND_DIR" || exit

# Check if requirements are installed
echo "📦 Installing dependencies..."
pip3 install -q -r requirements.txt 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Some packages may not have installed. Trying alternative method..."
    pip3 install --user -q -r requirements.txt
fi

echo "✅ Dependencies ready!"
echo ""

# Start the Flask app
echo "🚀 Starting Naija Connect server..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 app.py

# If the app exits
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "❌ Server stopped"
echo ""
