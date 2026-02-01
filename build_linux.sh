#!/bin/bash
# NexDex Linux Build Script
# Creates a standalone NexDex executable for Linux

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║    📦 NexDex Linux App Builder                        ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python Version: $PYTHON_VERSION"

# Check/create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --quiet --upgrade pip setuptools wheel
pip install --quiet -r requirements.txt
pip install --quiet pyinstaller

# Create assets directory for icons if it doesn't exist
if [ ! -d "assets" ]; then
    echo "📁 Creating assets directory..."
    mkdir -p assets
fi

# Check for icon file
if [ ! -f "assets/nexdex_icon.png" ]; then
    echo "⚠️  Icon file not found (assets/nexdex_icon.png)"
    echo "   Creating a placeholder. You can replace it with a proper icon later."
    touch assets/nexdex_icon.png
fi

# Clean previous builds
if [ -d "dist" ]; then
    echo "🗑️  Cleaning previous build..."
    rm -rf dist build *.egg-info
fi

# Build the executable
echo ""
echo "🏗️  Building NexDex..."

pyinstaller \
    --onefile \
    --windowed \
    --name NexDex \
    --icon assets/nexdex_icon.png \
    --hidden-import=flask \
    --hidden-import=networkx \
    --hidden-import=matplotlib \
    --hidden-import=jinja2 \
    --hidden-import=colorama \
    --hidden-import=tabulate \
    --add-data "dashboard/templates:dashboard/templates" \
    --add-data "dashboard/static:dashboard/static" \
    --add-data "config:config" \
    --add-data "scenarios:scenarios" \
    --add-data "src:src" \
    launcher.py

if [ -f "dist/NexDex" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📦 Package location: dist/NexDex"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Make executable: chmod +x dist/NexDex"
    echo "   2. Run: ./dist/NexDex"
    echo "   3. Or double-click the executable in your file manager"
    echo ""
    echo "🚀 The app will automatically open the dashboard in your browser"
    echo ""
    
    # Make executable
    chmod +x dist/NexDex
    
    # Create a tar.gz for distribution
    echo "📦 Creating distribution archive..."
    cd dist
    tar -czf ../releases/NexDex-Linux.tar.gz NexDex
    cd ..
    
    echo "✅ Distribution archive created: releases/NexDex-Linux.tar.gz"
    echo ""
else
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi

echo "✨ Done! Your standalone NexDex app is ready."
