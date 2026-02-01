# 🚀 NexDex App Installation Guide

Thank you for downloading NexDex! This guide will help you get started in just a few clicks.

## What is NexDex?

NexDex is a **Cross-System Business Impact Simulator** that helps you understand how failures in one service cascade through your entire system. The app comes with an interactive web dashboard and requires zero installation beyond extracting the files.

## Installation & Launch

### macOS (Intel & Apple Silicon)

1. **Download & Extract**
   - Download `NexDex-Mac.zip`
   - Double-click to extract → folder `NexDex.app` appears

2. **First Launch**
   - Double-click `NexDex.app`
   - If macOS shows "Cannot open" → Right-click → "Open"
   - Approve security prompt (first time only)

3. **Dashboard Opens**
   - Your default browser opens to `http://localhost:5000`
   - Dashboard is ready to use!

4. **Stop the App**
   - Close the browser tab or application window

### Windows

1. **Download & Extract**
   - Download `NexDex-Windows.zip`
   - Right-click → Extract All → Select folder

2. **First Launch**
   - Double-click `NexDex.exe`
   - Windows SmartScreen may appear → Click "Run anyway"
   - Firewall may ask → Click "Allow"

3. **Dashboard Opens**
   - Your default browser opens to `http://localhost:5000`
   - Dashboard is ready to use!

4. **Stop the App**
   - Close the application window
   - Or press Ctrl+C in any terminal window it opened

### Linux

1. **Download & Extract**
   ```bash
   tar -xzf NexDex-Linux.tar.gz
   cd NexDex
   ```

2. **First Launch**
   ```bash
   chmod +x NexDex
   ./NexDex
   ```
   Or double-click `NexDex` in your file manager.

3. **Dashboard Opens**
   - Your default browser opens to `http://localhost:5000`
   - Dashboard is ready to use!

4. **Stop the App**
   ```bash
   Ctrl+C
   ```

## Features

### 📊 Scenario Management
- **View All Scenarios** - See pre-built failure scenarios
- **Search & Filter** - Find scenarios by name or tags
- **Run Simulations** - Execute a scenario to see impact analysis
- **View Reports** - Get detailed impact breakdown

### 🔄 Scenario Comparison
- **Compare Two Scenarios** - Side-by-side impact analysis
- **Identify Differences** - See which services are uniquely affected
- **Visual Indicators** - Red (worse) and green (better) comparisons

### 📈 Impact Analysis
- **Total Impact Score** - Combined impact of all failures
- **Services Affected** - Direct and cascade failures
- **Business Processes** - Which processes are most impacted
- **Cascade Depth** - How far failures propagate

### 📄 Reports
- **Markdown Reports** - Machine-readable format
- **HTML Reports** - Beautiful interactive reports
- **Downloadable** - Save reports for documentation

### 🕐 Peak Hours
- **Time-Based Multipliers** - 1.2x impact during peak hours
- **Realistic Modeling** - Account for business hours in simulations

## Dashboard Walkthrough

### 1. Scenario List (Home)
- All pre-configured failure scenarios
- Search bar for quick filtering
- Run any scenario with one click

### 2. Simulation Results
After running a scenario, you'll see:
- **Impact Summary** - Quick metrics
- **Affected Services** - Table of all impacted services
- **Business Processes** - Highest-impact processes
- **Top Services** - Most critical failures
- **Generate Reports** - Download HTML/Markdown

### 3. Comparison View
- Select two scenarios to compare
- Side-by-side impact metrics
- Unique and common affected services
- Visual severity indicators
- Download comparison report

## Example Usage

### Scenario: "Database Outage (Peak Hours)"
1. Click "Run Simulation" next to the scenario
2. View results:
   - 11 services affected
   - 1584.94 impact score (with 1.2x peak multiplier)
   - Payment & Order services most impacted
3. Download HTML report for stakeholders

### Compare Scenarios
1. Go to "Compare Scenarios"
2. Select "peak_hours_db_outage" vs "api_gateway_failure"
3. See how database failure (1584.94) vs API failure (852.18) compare
4. Identify unique risks for each scenario

## System Requirements

- **Disk Space** - ~200MB (app + data)
- **Memory** - 512MB minimum, 1GB+ recommended
- **Network** - Local network only (no internet required)
- **Browser** - Modern browser (Chrome, Firefox, Safari, Edge)

### Supported Operating Systems
- macOS 10.13+ (Intel & Apple Silicon)
- Windows 10 (64-bit)
- Linux with glibc 2.17+

## Port Information

The dashboard runs on **localhost:5000** by default.

To use a different port:

**macOS/Linux:**
```bash
export NEXDEX_PORT=8080
./NexDex
```

**Windows:**
```cmd
set NEXDEX_PORT=8080
NexDex.exe
```

## Troubleshooting

### Dashboard won't open
1. Check if another app is using port 5000
2. Wait 10 seconds after app launches
3. Manually navigate to `http://localhost:5000` in your browser

### "Port already in use" error
Use a different port:
```bash
export NEXDEX_PORT=8080
./NexDex
```

### App crashes immediately
1. Ensure you have Python 3.9+ (if building from source)
2. Check for antivirus or firewall blocking
3. Try the web version at [nexdex.dev](https://nexdex.dev)

### Dashboard looks broken
- Refresh your browser (Ctrl+R or Cmd+R)
- Clear browser cache
- Try a different browser

### Performance issues
- Close other applications to free up RAM
- Close unused browser tabs
- Restart the app

## FAQ

**Q: Does NexDex require internet?**
A: No, everything runs locally. No data leaves your computer.

**Q: Can I modify scenarios?**
A: Yes, edit JSON files in the `scenarios/` folder and restart the app.

**Q: Can I run multiple simulations?**
A: Yes, each simulation is independent. Results are saved as reports.

**Q: Where are reports saved?**
A: In the `reports/` folder (created on first run).

**Q: How do I update NexDex?**
A: Download the latest release and replace your .app/.exe file.

**Q: Is my data safe?**
A: Yes, all data stays on your computer. Nothing is uploaded or tracked.

**Q: Can I run this on a server?**
A: Yes, edit `launcher.py` to change host from `127.0.0.1` to `0.0.0.0`

## Advanced: Command Line

If you extracted the source code, you can use the CLI:

```bash
# List all services
python3 nexdex.py --list

# Run a scenario via CLI
python3 nexdex.py --load peak_hours_db_outage

# Interactive mode
python3 nexdex.py --interactive

# Compare two scenarios
python3 nexdex.py --compare scenario1 scenario2

# Get help
python3 nexdex.py --help
```

## Getting Help

- **Documentation** - See QUICK-START.txt in the app folder
- **Issues** - Create an issue on GitHub
- **Questions** - Check the FAQ above

## What's Included

```
NexDex.app/
├── Dashboard/          # Web interface
│   ├── Templates/      # HTML pages
│   ├── Static/         # CSS & JavaScript
│   └── App.py          # Flask backend
├── Config/             # Service definitions
├── Scenarios/          # Pre-built scenarios
├── Reports/            # Generated reports
└── Src/                # Simulation engine
```

## Next Steps

1. ✅ Launch the app and open the dashboard
2. 📊 Run your first simulation
3. 📈 Compare different failure scenarios
4. 📄 Generate reports for your team
5. 🔧 Customize scenarios with your own services (advanced)

---

Enjoy using NexDex! Questions? Check our documentation or create an issue on GitHub. 🚀
