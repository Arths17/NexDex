# NexDex - Complete User Guide

## Welcome to NexDex! 🎉

NexDex is a professional cross-system business impact simulator that helps you understand how changes cascade through your organization. This guide covers everything you need to get started.

---

## Table of Contents

1. [Quick Start (2 minutes)](#quick-start)
2. [Installation by Platform](#installation)
3. [Getting Started](#getting-started)
4. [Features & How to Use](#features)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)
7. [FAQ](#faq)

---

## Quick Start

### For macOS (Easiest)

1. **Download**: Click "Download for macOS" on [our website](index.html)
2. **Extract**: Double-click the ZIP file to extract
3. **Run**: Double-click `NexDex.app`
4. **Use**: Dashboard opens automatically in your browser

That's it! You're ready to go.

### For Windows (Coming Soon)

```
1. Download NexDex-Windows.zip
2. Right-click → Extract All
3. Double-click NexDex.exe
4. Dashboard appears in your browser
```

### For Linux (Coming Soon)

```bash
# Extract the archive
tar -xzf NexDex-Linux.tar.gz

# Run the app
./NexDex

# Dashboard opens in your browser
```

---

## Installation

### macOS Installation

**Requirements:**
- macOS 10.13 or later
- Intel or Apple Silicon processor
- 500 MB free disk space

**Step-by-Step:**

1. **Download the app**
   - Visit [nexdex.example.com](index.html)
   - Click "Download for macOS"
   - Wait for download to complete (~28 MB)

2. **Extract the ZIP file**
   - Open Downloads folder
   - Double-click `NexDex-Mac.zip`
   - You'll get `NexDex.app`

3. **First time running**
   - Double-click `NexDex.app`
   - You might see "Cannot verify developer" warning
   - Click "Open" to proceed (safe to do)

4. **Dashboard loads**
   - Your browser opens automatically
   - You see NexDex dashboard at `localhost:5000`
   - Ready to use!

**Troubleshooting macOS:**

- **"NexDex can't be opened"** → Right-click, select "Open", then "Open" again
- **Port 5000 already in use** → Close other apps using port 5000
- **Browser won't open** → Manually go to `http://localhost:5000`

---

### Windows Installation

**Requirements:**
- Windows 10 or Windows 11
- 64-bit processor
- 500 MB free disk space

**Step-by-Step:**

1. **Download the app**
   - Visit [nexdex.example.com](index.html)
   - Click "Download for Windows"
   - Wait for download to complete (~25 MB)

2. **Extract the ZIP file**
   - Right-click `NexDex-Windows.zip`
   - Select "Extract All"
   - Choose where to save
   - Click "Extract"

3. **Run the app**
   - Open extracted folder
   - Double-click `NexDex.exe`
   - Windows Defender might ask for permission (safe to allow)

4. **Dashboard loads**
   - Your browser opens automatically
   - You see NexDex dashboard
   - Ready to use!

**Troubleshooting Windows:**

- **Windows Defender warning** → Click "More info" then "Run anyway"
- **Port 5000 already in use** → Close other apps, then try again
- **"Program not found" error** → Extract the ZIP properly first

---

### Linux Installation

**Requirements:**
- glibc 2.17 or later
- Ubuntu 16.04+, CentOS 7+, or Debian 8+
- 500 MB free disk space

**Step-by-Step:**

```bash
# 1. Download (using wget or curl)
wget https://github.com/Arths17/NexDex/releases/download/v1.0.0/NexDex-Linux.tar.gz
# OR
curl -L -O https://github.com/Arths17/NexDex/releases/download/v1.0.0/NexDex-Linux.tar.gz

# 2. Extract
tar -xzf NexDex-Linux.tar.gz

# 3. Make executable (if needed)
chmod +x NexDex

# 4. Run the app
./NexDex

# 5. Dashboard opens in your browser at http://localhost:5000
```

**Troubleshooting Linux:**

- **"command not found"** → Make sure you extracted and use `./NexDex`
- **Permission denied** → Run `chmod +x NexDex` first
- **Port 5000 in use** → Edit launcher.py or change port

---

## Getting Started

### First Time User Checklist

- [ ] App installed and running
- [ ] Dashboard visible in browser
- [ ] Understand the main interface
- [ ] Create your first scenario
- [ ] Run a simulation
- [ ] View the results

### The Dashboard Interface

**Main Sections:**

1. **Home/Dashboard**
   - Overview of all scenarios
   - Quick statistics
   - Recent activity

2. **Scenarios**
   - View all your scenarios
   - Create new scenarios
   - Edit existing ones

3. **Simulation**
   - Run what-if analysis
   - Compare scenarios
   - Generate reports

4. **Settings**
   - Configure application
   - Manage data
   - Export/Import scenarios

---

## Features & How to Use

### 1. Create a Scenario

**What it does:** Define your system and relationships

**How to use:**

1. Go to "Scenarios" section
2. Click "Create New Scenario"
3. Give it a name (e.g., "Q1 2026 Rollout")
4. Define your systems:
   - System A (e.g., Database)
   - System B (e.g., API)
   - System C (e.g., Frontend)
5. Click "Save"

### 2. Define Dependencies

**What it does:** Show how systems affect each other

**How to use:**

1. In your scenario, click "Add Dependency"
2. Select: System A → System B
3. Set impact percentage (0-100%)
4. Optional: Add description
5. Repeat for all relationships
6. Click "Save"

### 3. Run Simulations

**What it does:** Analyze impact of changes

**How to use:**

1. Click "Run Simulation"
2. Choose which system changes
3. Set change intensity (low/medium/high)
4. Choose time period to analyze
5. Click "Run"
6. View results in dashboard

### 4. Compare Scenarios

**What it does:** See differences between scenarios

**How to use:**

1. Go to "Compare"
2. Select 2 scenarios to compare
3. Choose what to compare:
   - Systems & dependencies
   - Simulation results
   - Impact patterns
4. View comparison report

### 5. Generate Reports

**What it does:** Export results for documentation

**How to use:**

1. In scenario, click "Generate Report"
2. Choose format:
   - ASCII (text)
   - HTML (viewable in browser)
3. Click "Generate"
4. Download or view report

---

## Understanding Results

### Impact Score

**What it means:**
- 0-20%: Low impact
- 20-50%: Medium impact
- 50-80%: High impact
- 80-100%: Critical impact

**How to interpret:** Higher score means the change affects more of your organization.

### Time-Based Multipliers

**What it means:** Impact changes over time

**Example:**
- Day 1: 50% impact
- Day 3: 75% impact (increases)
- Day 7: 100% impact (fully realized)

**Why it matters:** Shows how effects compound or fade over time.

---

## Troubleshooting

### General Issues

**App won't start:**
- Check if port 5000 is free: `lsof -i :5000` (macOS/Linux)
- Close other apps
- Try restarting app

**Dashboard won't load:**
- Wait 5 seconds after starting app
- Try opening browser manually: `http://localhost:5000`
- Check internet is working (for display assets)

**App closes immediately:**
- Check system requirements are met
- Try opening terminal and running directly
- Check error messages

### Platform-Specific

**macOS:**
- Right-click app → Get Info → Check for blocking
- Remove from quarantine: `xattr -d com.apple.quarantine NexDex.app`

**Windows:**
- Check Windows Defender isn't blocking
- Try running in compatibility mode
- Try Administrator mode

**Linux:**
- Check execute permissions: `chmod +x NexDex`
- Check libc version: `ldd ./NexDex | grep libc`
- Try: `export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH`

---

## Advanced Usage

### Data Management

**Export your scenarios:**
1. In scenario list, click "Export"
2. Choose format (JSON recommended)
3. Save to desired location

**Import scenarios:**
1. Click "Import Scenario"
2. Select JSON file
3. Review and confirm
4. Click "Import"

### Customization

**Change port (if 5000 is busy):**

macOS/Linux:
```bash
NEXDEX_PORT=8000 ./NexDex.app/Contents/MacOS/NexDex
```

Windows:
```cmd
set NEXDEX_PORT=8000
NexDex.exe
```

**Disable auto-launch:**

Set environment variable:
```bash
NEXDEX_NO_BROWSER=1
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+S` / `Ctrl+S` | Save scenario |
| `Cmd+N` / `Ctrl+N` | New scenario |
| `Cmd+,` / `Ctrl+,` | Open settings |
| `?` | Help menu |

---

## FAQ

### General Questions

**Q: Is it really free?**
A: Yes! NexDex is free and open-source forever.

**Q: Do I need to install Python?**
A: No! Everything is bundled into the app.

**Q: Can I use it offline?**
A: Yes! Everything runs locally. No internet required.

**Q: Is my data private?**
A: Completely! Your data never leaves your computer.

**Q: Can I use it at work?**
A: Yes! It's free for personal and commercial use.

### Technical Questions

**Q: What's the maximum scenario size?**
A: Up to 500+ systems per scenario (depends on your hardware).

**Q: Can I export my data?**
A: Yes! Export to JSON format anytime.

**Q: What about data backup?**
A: Manually export and save your scenarios regularly.

**Q: Can multiple people use one installation?**
A: Yes! Just share the downloaded app.

### Support Questions

**Q: I found a bug, what do I do?**
A: Report it on [GitHub Issues](https://github.com/Arths17/NexDex/issues)

**Q: Can I request a feature?**
A: Yes! Open a [GitHub Discussion](https://github.com/Arths17/NexDex/discussions)

**Q: Where do I get help?**
A: Check GitHub issues, discussions, or this documentation.

**Q: Can I contribute?**
A: Yes! NexDex is open-source. Fork it on GitHub!

---

## Getting Help

### Documentation

- [Main README](../README.md)
- [Release Notes](../RELEASE-NOTES.md)
- [Technical Guide](../PACKAGING.md)
- [Publication Info](../PUBLISHED.md)

### Community

- [GitHub Repository](https://github.com/Arths17/NexDex)
- [GitHub Issues](https://github.com/Arths17/NexDex/issues) - Report bugs
- [GitHub Discussions](https://github.com/Arths17/NexDex/discussions) - Ask questions

### Quick Help

**Check this first:**
1. Is your system supported?
2. Did you extract the ZIP correctly?
3. Is port 5000 available?
4. Try restarting the app?

---

## Tips & Tricks

### Best Practices

1. **Start simple:** Create small scenarios first
2. **Document your systems:** Use clear naming
3. **Export regularly:** Don't lose your work
4. **Test assumptions:** Run multiple simulations
5. **Share results:** Export reports for stakeholders

### Advanced Tips

1. **Batch analysis:** Run multiple scenarios together
2. **Templates:** Reuse common scenario patterns
3. **What-if analysis:** Try different impact percentages
4. **Time analysis:** Compare day 1 vs day 30 impacts
5. **Cross-reference:** Use import/export for merging

---

## System Information

**Version:** 1.0.0
**Release Date:** February 1, 2026
**Type:** Standalone Desktop Application
**License:** Open Source
**Platform Support:** macOS, Windows, Linux

---

## Next Steps

1. ✅ Download and install NexDex
2. ✅ Create your first scenario
3. ✅ Define some systems and relationships
4. ✅ Run a simulation
5. ✅ Generate a report
6. ✅ Share with your team!

---

## Feedback & Questions

Have ideas? Found a bug? Have questions?

Visit: [https://github.com/Arths17/NexDex](https://github.com/Arths17/NexDex)

We'd love to hear from you!

---

*Created: February 1, 2026*
*Last Updated: February 1, 2026*
*Status: Complete & Ready to Use*
