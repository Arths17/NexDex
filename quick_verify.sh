#!/bin/bash
echo "Verifying NexDex Packaging Files..."
echo ""

FILES=(
    "launcher.py"
    "nexdex.py"
    "build_mac.sh"
    "build_windows.bat"
    "build_linux.sh"
    "nexdex_mac.spec"
    "nexdex_windows.spec"
    "PACKAGING.md"
    "INSTALL.md"
    "WEBSITE-DOWNLOADS.md"
    "BUILD.md"
)

DIRS=(
    "dashboard"
    "dashboard/templates"
    "dashboard/static"
    "src"
    "config"
    "scenarios"
    "assets"
    "website"
)

MISSING=0

for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        echo "✓ $f"
    else
        echo "✗ MISSING: $f"
        ((MISSING++))
    fi
done

echo ""
for d in "${DIRS[@]}"; do
    if [ -d "$d" ]; then
        echo "✓ $d/"
    else
        echo "✗ MISSING: $d/"
        ((MISSING++))
    fi
done

echo ""
if [ $MISSING -eq 0 ]; then
    echo "=========================================="
    echo "SUCCESS: All packaging files ready!"
    echo "=========================================="
    echo ""
    echo "Next: Build the standalone apps"
    echo "  bash build_mac.sh         (for macOS)"
    echo "  bash build_linux.sh       (for Linux)"
    echo "  build_windows.bat         (for Windows)"
else
    echo "Missing $MISSING files/directories"
    exit 1
fi
