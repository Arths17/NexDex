#!/bin/bash
# Script to fix macOS Gatekeeper warning
# Run this after downloading NexDex

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║    🔓 NexDex - Remove Gatekeeper Quarantine              ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Find NexDex.app in Downloads or current directory
APP_PATH=""

if [ -d "$HOME/Downloads/NexDex.app" ]; then
    APP_PATH="$HOME/Downloads/NexDex.app"
elif [ -d "NexDex.app" ]; then
    APP_PATH="NexDex.app"
elif [ -d "dist/NexDex.app" ]; then
    APP_PATH="dist/NexDex.app"
else
    echo "❌ NexDex.app not found!"
    echo ""
    echo "Please specify the path:"
    echo "  ./remove_quarantine.sh /path/to/NexDex.app"
    echo ""
    exit 1
fi

# Use provided path if given
if [ -n "$1" ]; then
    APP_PATH="$1"
fi

echo "📍 Found app at: $APP_PATH"
echo ""

# Remove quarantine attribute
echo "🔓 Removing quarantine attribute..."
xattr -d com.apple.quarantine "$APP_PATH" 2>/dev/null
xattr -cr "$APP_PATH" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Success! NexDex.app is now trusted."
    echo ""
    echo "🚀 You can now open NexDex.app normally."
    echo ""
else
    echo "⚠️  Could not remove quarantine. Try manually:"
    echo ""
    echo "   1. Right-click NexDex.app"
    echo "   2. Click 'Open'"
    echo "   3. Click 'Open' again in the dialog"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════"
