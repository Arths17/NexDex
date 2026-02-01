# 🎯 NexDex Packaging & Distribution

Complete guide for building, packaging, and distributing NexDex as standalone applications.

## 📋 Overview

This directory contains everything needed to turn NexDex into production-ready standalone apps for:
- 🍎 **macOS** (`.app` bundle)
- 🪟 **Windows** (`.exe` executable)
- 🐧 **Linux** (standalone binary)

Users can download these apps and run them with **zero installation required**.

## 📁 Project Structure

```
NexDex/
├── launcher.py                  # Entry point for standalone app
├── nexdex_mac.spec              # PyInstaller config for macOS
├── nexdex_windows.spec          # PyInstaller config for Windows
├── build_mac.sh                 # Build script for macOS
├── build_windows.bat            # Build script for Windows
├── build_linux.sh               # Build script for Linux
├── PACKAGING.md                 # Detailed packaging guide
├── INSTALL.md                   # User installation guide
├── WEBSITE-DOWNLOADS.md         # Website integration guide
│
├── dashboard/                   # Flask web dashboard
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   └── static/                  # CSS & JavaScript
│
├── releases/                    # Built apps (output directory)
│   ├── NexDex-Mac.zip           # macOS app bundle
│   ├── NexDex-Windows.zip       # Windows executable
│   └── NexDex-Linux.tar.gz      # Linux binary
│
└── ...other NexDex files
```

## 🚀 Quick Start

### Build for Your Platform

**macOS:**
```bash
bash build_mac.sh
# Output: dist/NexDex.app + releases/NexDex-Mac.zip
```

**Windows:**
```cmd
build_windows.bat
:: Output: dist\NexDex.exe + releases\NexDex-Windows.zip
```

**Linux:**
```bash
bash build_linux.sh
# Output: dist/NexDex + releases/NexDex-Linux.tar.gz
```

### Run the Built App

**macOS:**
```bash
open dist/NexDex.app
```

**Windows:**
```cmd
dist\NexDex.exe
```

**Linux:**
```bash
./dist/NexDex
```

## 📦 Components

### `launcher.py`
The entry point for standalone applications. When the user runs the app:
1. Detects configuration and scenario files
2. Creates Flask application
3. Launches web dashboard in default browser
4. Runs Flask server on localhost:5000

### Build Scripts (`build_*.sh`, `build_*.bat`)
Automated build scripts that:
- Create/activate virtual environment
- Install dependencies
- Run PyInstaller
- Create distribution archives
- Output ready-to-distribute files

### PyInstaller Specs (`*.spec` files)
Configuration files for PyInstaller that:
- Define what files to include
- Specify hidden imports
- Set app metadata
- Configure icons and branding

## 🔧 Configuration

### Changing App Name

Edit `.spec` files:

**macOS** (`nexdex_mac.spec`):
```python
app = BUNDLE(exe, name='MyApp.app', ...)
```

**Windows** (`nexdex_windows.spec`):
```python
exe = EXE(..., name='MyApp', ...)
```

### Custom Icons

1. Create icon files:
   - macOS: `.icns` file (256x256)
   - Windows: `.ico` file (256x256)
   - Linux: `.png` file (256x256)

2. Place in `assets/` folder

3. Rebuild using respective build script

### Custom Port

Edit `launcher.py`:
```python
port = int(os.environ.get('NEXDEX_PORT', 8080))  # Change 5000 to 8080
```

## 📊 Build Output

### macOS
```
dist/
└── NexDex.app/
    ├── Contents/
    │   ├── MacOS/
    │   │   └── NexDex          # Executable
    │   ├── Resources/
    │   │   └── [all dependencies]
    │   └── Info.plist           # App metadata
```
**Size:** ~150-200 MB
**Distribution:** `NexDex-Mac.zip`

### Windows
```
dist/
└── NexDex.exe                   # Single executable
```
**Size:** ~120-180 MB
**Distribution:** `NexDex-Windows.zip`

### Linux
```
dist/
└── NexDex                       # Single executable
```
**Size:** ~100-150 MB
**Distribution:** `NexDex-Linux.tar.gz`

## 🧪 Testing

### Pre-Build Testing
```bash
# Test Flask app locally
python3 launcher.py
# Should open http://localhost:5000

# Test CLI
python3 nexdex.py --list
python3 nexdex.py --load peak_hours_db_outage
```

### Post-Build Testing
1. Extract the distribution file
2. Run the app (double-click or terminal)
3. Test all dashboard features
4. Verify reports generate correctly
5. Check performance and startup time

### Common Test Cases
- [ ] App launches without errors
- [ ] Dashboard opens automatically
- [ ] Can run a simulation
- [ ] Can compare scenarios
- [ ] Can download reports
- [ ] App closes cleanly
- [ ] No error dialogs appear

## 📈 Distribution

### Upload to Web Server
```bash
# Upload releases to your web server
scp releases/NexDex-*.zip user@server:/var/www/downloads/
scp releases/NexDex-*.tar.gz user@server:/var/www/downloads/
```

### Create Download Page
See `WEBSITE-DOWNLOADS.md` for detailed HTML/CSS templates for your website's download page.

### Add to GitHub Releases
```bash
# Tag release
git tag v1.0.0

# Push tag
git push origin v1.0.0

# Create release on GitHub with these files:
# - NexDex-Mac.zip
# - NexDex-Windows.zip
# - NexDex-Linux.tar.gz
```

## 🔐 Security Considerations

### Code Protection
PyInstaller compiles Python to bytecode, which:
- ✅ Prevents casual code viewing
- ✅ Protects your algorithms
- ✅ Makes reverse-engineering harder
- ⚠️ Is not cryptographically secure

### User Privacy
- All data stays local (no cloud upload)
- No telemetry or tracking
- No internet required
- Reports saved to user's computer

### Code Signing (Optional)

**macOS:**
```bash
codesign --deep --force --verify --verbose \
  --sign "-" dist/NexDex.app
```

**Windows:**
(Requires certificate - Signtool.exe)

## 🐛 Troubleshooting

### Build Fails
1. Check Python version: `python3 --version`
2. Ensure all dependencies: `pip install -r requirements.txt`
3. Check virtual environment is activated
4. Clear build cache: `rm -rf dist build`

### App Won't Start
1. Check port 5000 is available
2. Try different port: `export NEXDEX_PORT=8080`
3. Check browser console for errors
4. Try in different browser

### Icon Not Showing
1. Verify icon file exists in `assets/`
2. Correct format (`.icns`, `.ico`, `.png`)
3. Minimum size 256x256
4. Rebuild after adding icon

### Dashboard Blank
1. Check browser console (F12)
2. Verify templates exist in `dashboard/templates/`
3. Check static files load (network tab)
4. Try different browser

## 📚 Documentation

- **PACKAGING.md** - Detailed packaging guide with advanced options
- **INSTALL.md** - User installation and getting started guide
- **WEBSITE-DOWNLOADS.md** - Website integration and download page setup

## 🔄 Version Updates

### Building New Version

1. Update version in `launcher.py` or code
2. Test thoroughly
3. Create git tag: `git tag v1.1.0`
4. Build on all platforms:
   ```bash
   bash build_mac.sh
   bash build_linux.sh
   # On Windows machine: build_windows.bat
   ```
5. Upload releases
6. Update website download links
7. Create GitHub release

### Incremental Releases

For bug fixes or patches:
1. Fix the bug in source code
2. Rebuild using respective script
3. Upload new `.zip`/`.tar.gz`
4. Update website version number

## 📊 Performance Notes

### Startup Time
- First run: 3-5 seconds (Flask initialization)
- Subsequent runs: ~1-2 seconds
- Dashboard load: <1 second

### Memory Usage
- Idle: 80-120 MB
- Running simulation: 150-250 MB
- Generating reports: 200-300 MB

### Disk Space Required
- macOS app: ~150 MB installed
- Windows exe: ~120 MB installed
- Linux binary: ~100 MB installed

All include all dependencies bundled.

## 🎯 Next Steps

1. **Build** - Run the appropriate build script
2. **Test** - Verify app works on target platform
3. **Package** - Distribution files created in `releases/`
4. **Host** - Upload to web server or GitHub
5. **Promote** - Add download links to website
6. **Support** - Help users install and use

## 📞 Support

For issues with packaging:
1. Check troubleshooting section above
2. Review PACKAGING.md for advanced options
3. Check PyInstaller documentation: https://pyinstaller.org
4. Create GitHub issue with build logs

## 🎉 You're Ready!

Your NexDex applications are ready for production distribution. Users can now download and run NexDex with a single click!

Happy packaging! 🚀
