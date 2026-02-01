# 📦 NexDex Packaging Guide

This guide explains how to build standalone NexDex applications for Mac, Windows, and Linux using PyInstaller.

## Overview

NexDex can be packaged into a single-click executable application that:
- Runs entirely locally (no external dependencies)
- Automatically launches the web dashboard on startup
- Hides the Python code (compiled into bytecode)
- Works on Mac (.app), Windows (.exe), and Linux (binary)

## Prerequisites

### For All Platforms
- Python 3.9+ installed
- ~500MB disk space for builds
- All dependencies in `requirements.txt` installed

### Platform-Specific
- **Mac**: macOS 10.13+ (Intel or Apple Silicon)
- **Windows**: Windows 10+ (64-bit recommended)
- **Linux**: Any modern Linux distribution with Python 3.9+

## Quick Start

### Mac Users
```bash
bash build_mac.sh
```

Output: `dist/NexDex.app` and `releases/NexDex-Mac.zip`

To run:
```bash
open dist/NexDex.app
```

### Windows Users
```cmd
build_windows.bat
```

Output: `dist/NexDex.exe` and `releases/NexDex-Windows.zip`

Double-click `dist/NexDex.exe` to launch.

### Linux Users
```bash
bash build_linux.sh
```

Output: `dist/NexDex` and `releases/NexDex-Linux.tar.gz`

To run:
```bash
./dist/NexDex
```

## Build Scripts Explained

### `build_mac.sh`
- Creates a macOS application bundle (.app)
- Includes all dependencies and resources
- Creates a distributable ZIP archive
- Automatically opens the app in Finder

### `build_windows.bat`
- Creates a Windows executable (.exe)
- No console window on startup (GUI mode)
- Creates a distributable ZIP archive
- Adds to system if desired

### `build_linux.sh`
- Creates a single standalone binary
- Works on any Linux system with glibc
- Creates a distributable tar.gz archive
- Executable by default

## Advanced Options

### Custom Icons

#### Mac (`.icns` file)
```bash
# Generate from PNG (requires ImageMagick)
convert nexdex.png -define icon:auto-resize=256,128,96,64,48,32,16 nexdex.icns

# Place in assets/
cp nexdex.icns assets/nexdex_icon.icns

# Rebuild
bash build_mac.sh
```

#### Windows (`.ico` file)
```bash
# Generate from PNG (requires ImageMagick or online tool)
convert nexdex.png -compress none nexdex.ico

# Place in assets/
cp nexdex.ico assets/nexdex_icon.ico

# Rebuild
build_windows.bat
```

#### Linux (`.png` file)
```bash
# Create a 256x256 PNG icon
cp nexdex.png assets/nexdex_icon.png

# Rebuild
bash build_linux.sh
```

### Modifying Build Settings

Edit the `.spec` files to customize:

**`nexdex_mac.spec`** (macOS)
```python
# Change app name
a = Analysis(['launcher.py'], ...)
app = BUNDLE(exe, name='MyApp.app', ...)
```

**`nexdex_windows.spec`** (Windows)
```python
# Change exe name
exe = EXE(..., name='MyApp', ...)
```

### One-File vs One-Dir

Current scripts create:
- **Mac**: One directory (`NexDex.app` folder)
- **Windows**: One file (`NexDex.exe`)
- **Linux**: One file (`NexDex`)

To make Windows create a one-directory bundle, edit `nexdex_windows.spec` and replace the `EXE()` call with a `BUNDLE()` call similar to macOS.

## Distribution

### File Sizes (Approximate)
- macOS .app: ~150-200 MB
- Windows .exe: ~120-180 MB
- Linux binary: ~100-150 MB

### Create Distribution Archives

**Mac**:
```bash
cd dist
zip -r ../releases/NexDex-Mac.zip NexDex.app
cd ..
```

**Windows**:
```cmd
cd dist
tar -a -c -f ..\releases\NexDex-Windows.zip NexDex.exe
cd ..
```

**Linux**:
```bash
cd dist
tar -czf ../releases/NexDex-Linux.tar.gz NexDex
cd ..
```

## Troubleshooting

### "Python not found"
Ensure Python 3.9+ is installed and in your PATH.

### "Module not found" errors
Add the module to `hiddenimports` in the `.spec` file:
```python
hiddenimports=[
    'flask',
    'networkx',
    'module_name_here',  # Add here
    ...
]
```

### App crashes on startup
Check `launcher.py` for errors. Run in debug mode:
```bash
# On Mac
open -a Terminal dist/NexDex.app/Contents/MacOS/NexDex

# On Linux
./dist/NexDex --debug
```

### Dashboard won't open
Ensure port 5000 is available on your system. To change the port:
```bash
export NEXDEX_PORT=8080
./dist/NexDex
```

### Icon not showing
Ensure the icon file exists in `assets/` with the correct format:
- Mac: `.icns` (IcnsForge or online converter)
- Windows: `.ico` (any image editor or online tool)
- Linux: `.png` (256x256 minimum)

## Security & Code Protection

PyInstaller compiles Python to bytecode, which:
- ✅ Prevents casual viewing of source code
- ✅ Keeps your algorithms and logic private
- ✅ Makes reverse-engineering significantly harder
- ⚠️ Is not cryptographically secure (determined reversal engineer could still read bytecode)

For maximum security, consider:
1. Code obfuscation (Cython compilation)
2. License verification
3. Closed-source distribution

## Next Steps

1. **Test the Build**
   ```bash
   # Run the built app
   ./dist/NexDex  # or open dist/NexDex.app
   
   # Check dashboard opens
   # Try running a simulation
   ```

2. **Update Website**
   Add download links to your website:
   ```html
   <a href="releases/NexDex-Mac.zip">Download for Mac</a>
   <a href="releases/NexDex-Windows.zip">Download for Windows</a>
   <a href="releases/NexDex-Linux.tar.gz">Download for Linux</a>
   ```

3. **Create Installation Guide**
   - Mac: Extract → Double-click NexDex.app
   - Windows: Extract → Double-click NexDex.exe
   - Linux: Extract → Run `./NexDex`

4. **Version Control**
   Add to `.gitignore`:
   ```
   dist/
   build/
   *.spec.py
   releases/*.zip
   releases/*.tar.gz
   ```

## Advanced: Custom Launcher

To customize the launcher, edit `launcher.py`:
- Change startup message
- Modify port or host
- Add command-line arguments
- Change browser behavior

Example:
```python
def main():
    port = 8080  # Custom port
    app.run(host='0.0.0.0')  # Allow external access
```

## Support

For issues, check:
- PyInstaller documentation: https://pyinstaller.org
- Flask documentation: https://flask.palletsprojects.com
- GitHub issues: Create an issue in your repository

---

Happy packaging! 🚀
