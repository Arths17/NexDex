@echo off
REM NexDex Windows Build Script
REM Creates a standalone NexDex.exe for Windows

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║                                                       ║
echo ║    📦 NexDex Windows App Builder                      ║
echo ║                                                       ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Check Python version
python --version
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

REM Check/create virtual environment
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install --quiet --upgrade pip setuptools wheel
pip install --quiet -r requirements.txt
pip install --quiet pyinstaller

REM Create assets directory for icons if it doesn't exist
if not exist "assets" (
    echo 📁 Creating assets directory...
    mkdir assets
)

REM Check for icon file
if not exist "assets/nexdex_icon.ico" (
    echo ⚠️  Icon file not found (assets/nexdex_icon.ico)
    echo    Creating a placeholder. You can replace it with a proper icon later.
    type nul > assets\nexdex_icon.ico
)

REM Clean previous builds
if exist "dist" (
    echo 🗑️  Cleaning previous build...
    rmdir /s /q dist build
)

REM Build the app
echo.
echo 🏗️  Building NexDex.exe...
pyinstaller nexdex_windows.spec --clean --noconfirm

if exist "dist\NexDex.exe" (
    echo.
    echo ✅ Build successful!
    echo.
    echo 📦 Package location: dist\NexDex.exe
    echo.
    echo 📋 Next steps:
    echo    1. Double-click dist\NexDex.exe to launch
    echo    2. The dashboard will open automatically in your browser
    echo.
    
    REM Create a zip for distribution
    echo 📦 Creating distribution zip...
    cd dist
    tar -a -c -f ..\releases\NexDex-Windows.zip NexDex.exe
    cd ..
    
    echo ✅ Distribution zip created: releases\NexDex-Windows.zip
    echo.
) else (
    echo ❌ Build failed. Check the error messages above.
    exit /b 1
)

echo ✨ Done! Your standalone NexDex app is ready.
pause
