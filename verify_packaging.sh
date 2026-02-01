#!/bin/bash
# NexDex Packaging Verification Script
# Checks that all packaging files are in place and ready to build

set -e

echo ""
echo "=========================================="
echo "NexDex Packaging Setup Verification"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} Missing: $1"
        ((CHECKS_FAILED++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} Missing directory: $1"
        ((CHECKS_FAILED++))
    fi
}

echo ""
echo "Checking Core Files..."
check_file "launcher.py"
check_file "nexdex.py"

echo ""
echo ""
echo "Checking Build Scripts..."
check_file "build_mac.sh"
check_file "build_windows.bat"
check_file "build_linux.sh"

echo ""
echo "Checking PyInstaller Configs..."
check_file "nexdex_mac.spec"
check_file "nexdex_windows.spec"

echo ""
echo "Checking Documentation..."
check_file "PACKAGING.md"
check_file "INSTALL.md"
check_file "WEBSITE-DOWNLOADS.md"
check_file "BUILD.md"

echo ""
echo "Checking Directories..."
check_dir "dashboard"
check_dir "dashboard/templates"
check_dir "dashboard/static"
check_dir "src"
check_dir "config"
check_dir "scenarios"
check_dir "assets"
check_dir "website"

echo ""
echo "Checking Key Dashboard Files..."
check_file "dashboard/app.py"
check_file "dashboard/templates/base.html"
check_file "dashboard/templates/index.html"
check_file "dashboard/static/style.css"
check_file "dashboard/static/scripts.js"

echo ""
echo "Checking Website Files..."
check_file "website/downloads.html"

echo ""
echo "=========================================="
echo "Results"
echo "=========================================="
echo ""
echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"

if [ $CHECKS_FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $CHECKS_FAILED${NC}"
    echo ""
    echo "ERROR: Some files are missing."
    echo "Make sure you:"
    echo "  1. Created the dashboard/ folder with Flask app"
    echo "  2. Have all required build scripts"
    echo "  3. Run from the NexDex project root"
    exit 1
else
    echo ""
    echo "=========================================="
    echo "SUCCESS: All packaging files ready!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Build standalone apps:"
    echo "   macOS:   bash build_mac.sh"
    echo "   Windows: build_windows.bat"
    echo "   Linux:   bash build_linux.sh"
    echo ""
    echo "2. Read the guides:"
    echo "   - PACKAGING.md      (detailed packaging)"
    echo "   - INSTALL.md        (user guide)"
    echo "   - BUILD.md          (build infrastructure)"
    echo ""
    echo "3. Update your website:"
    echo "   - website/downloads.html (template)"
    echo "   - See WEBSITE-DOWNLOADS.md"
    echo ""
    echo "4. After building, upload to:"
    echo "   - releases/NexDex-Mac.zip"
    echo "   - releases/NexDex-Windows.zip"
    echo "   - releases/NexDex-Linux.tar.gz"
    echo ""
fi
