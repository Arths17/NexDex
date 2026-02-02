#!/bin/bash
# NexDex macOS Build Script
# Creates a standalone NexDex.app for macOS

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║    📦 NexDex macOS App Builder                        ║"
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
if [ ! -f "assets/nexdex_icon.icns" ]; then
    echo "⚠️  Icon file not found (assets/nexdex_icon.icns)"
    echo "   Creating a placeholder. You can replace it with a proper icon later."
    touch assets/nexdex_icon.icns
fi

# Clean previous builds
if [ -d "dist" ]; then
    echo "🗑️  Cleaning previous build..."
    rm -rf dist build *.egg-info
fi

# Build the app
echo ""
echo "🏗️  Building NexDex.app..."
pyinstaller nexdex_mac.spec --clean --noconfirm

if [ -d "dist/NexDex.app" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📦 Package location: dist/NexDex.app"
    echo ""
    
    # Sign the app with ad-hoc signature
    echo "🔐 Code signing app..."
    codesign --force --deep --sign - dist/NexDex.app 2>/dev/null || echo "⚠️  Code signing skipped (optional)"
    
    # Remove quarantine attribute for local testing
    echo "🔓 Removing quarantine attribute for local testing..."
    xattr -d com.apple.quarantine dist/NexDex.app 2>/dev/null || true
    xattr -cr dist/NexDex.app 2>/dev/null || true
    
    echo ""
    echo "📋 Next steps:"
    echo "   1. Open Finder and navigate to dist/"
    echo "   2. Right-click NexDex.app → Open (to allow on first run)"
    echo "   3. Or: open dist/NexDex.app"
    echo ""
    echo "🚀 The app will automatically open the dashboard in your browser"
    echo ""
    
    # Create a zip for distribution
    echo "📦 Creating distribution zip..."
    cd dist
    
    # Sign before zipping
    codesign --force --deep --sign - NexDex.app 2>/dev/null || true
    
    zip -r -q ../releases/NexDex-Mac.zip NexDex.app
    cd ..
    
    echo "✅ Distribution zip created: releases/NexDex-Mac.zip"
    echo ""
    echo "📝 Note: Users will need to right-click → Open on first launch"
    echo "   See MACOS-GATEKEEPER.md for detailed instructions"
    echo ""
else
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi

echo "✨ Done! Your standalone NexDex app is ready."
