# NexDex - Comprehensive FAQ

## General Questions

### What is NexDex?

**NexDex** is a professional cross-system business impact simulator that helps organizations understand how changes cascade through their systems.

**Key features:**
- Interactive web dashboard
- Dependency mapping
- Impact analysis with time-based multipliers
- Scenario comparison
- Professional report generation
- 100% offline - works completely locally

**Who uses it?**
- Business analysts
- System architects
- Operations teams
- Change managers
- Decision makers

---

## Download & Installation

### Where can I download NexDex?

**Official sources:**
1. **This website** (primary)
   - Visit the download page
   - Choose your platform
   - Click download button

2. **GitHub** (alternative)
   - Visit: https://github.com/Arths17/NexDex
   - Releases tab
   - Download any version

**All sources have the same files - choose whatever is easiest for you.**

### Do I need to install anything?

**Short answer: No!**

NexDex is completely self-contained. Just download, extract, and run.

**Nothing else needed:**
- ❌ No Python installation
- ❌ No Node.js installation
- ❌ No dependencies to install
- ❌ No configuration needed
- ✅ Just download and run!

### What are the system requirements?

**macOS:**
- macOS 10.13 or later
- Intel or Apple Silicon processor
- 500 MB free disk space
- 4 GB RAM (recommended)

**Windows:**
- Windows 10 or Windows 11
- 64-bit processor
- 500 MB free disk space
- 4 GB RAM (recommended)

**Linux:**
- glibc 2.17 or later
- Ubuntu 16.04+, CentOS 7+, or Debian 8+
- 500 MB free disk space
- 4 GB RAM (recommended)

### How do I install it?

**macOS:**
1. Download `NexDex-Mac.zip`
2. Double-click to extract
3. Double-click `NexDex.app`
4. Done!

**Windows:**
1. Download `NexDex-Windows.zip`
2. Right-click → Extract All
3. Double-click `NexDex.exe`
4. Done!

**Linux:**
```bash
tar -xzf NexDex-Linux.tar.gz
./NexDex
```

### How big is the download?

**File sizes:**
- macOS: ~28 MB
- Windows: ~25 MB
- Linux: ~22 MB

**Why so big?**
The app bundles Python, Flask, all dependencies, and the simulation engine. You're getting a complete, standalone application.

---

## Usage & Features

### How do I use NexDex?

**Basic workflow:**

1. **Create a scenario**
   - Define your systems
   - Name them clearly

2. **Map dependencies**
   - Show how systems affect each other
   - Set impact percentages

3. **Run simulations**
   - Choose what changes
   - See impact cascade

4. **Compare results**
   - Try different scenarios
   - Make better decisions

5. **Generate reports**
   - Document your analysis
   - Share with stakeholders

### What can I do with NexDex?

**Capabilities:**

- ✅ Model your entire organization
- ✅ Understand cascade effects
- ✅ Test "what-if" scenarios
- ✅ Compare different approaches
- ✅ Visualize complex dependencies
- ✅ Generate professional reports
- ✅ Export data for further analysis
- ✅ Run unlimited scenarios

### Can I import my data?

**Yes!** NexDex supports importing scenarios:

1. **JSON format**
   - Export from other tools
   - Import into NexDex
   - Format documented in repo

2. **CSV format**
   - System list CSV
   - Dependency list CSV
   - Bulk import available

3. **Manual entry**
   - Web interface
   - Quick and easy
   - Recommended for learning

### Can I export results?

**Yes!** Multiple formats:

1. **JSON**
   - Complete scenario data
   - For backup
   - Import into other tools

2. **HTML**
   - Beautiful formatted reports
   - Share with anyone
   - No special software needed

3. **ASCII**
   - Text-based reports
   - Email friendly
   - Terminal friendly

4. **CSV**
   - Impact data
   - Use in Excel/Sheets
   - For further analysis

---

## Technical Questions

### Does NexDex need internet?

**No!** Everything runs locally on your computer.

**What this means:**
- No cloud services
- No external API calls
- No data transmitted
- Works offline completely
- Works on airplane mode

**Internet might be needed for:**
- Downloading the app (first time)
- Website assets (fonts, icons) - minimal
- But core functionality works offline

### Is my data private?

**Yes, completely!**

**Your data:**
- Stays on your computer
- Never uploaded to cloud
- Never shared with anyone
- Never sent to our servers
- You have full control

**We don't:**
- Collect any data
- Track your usage
- Store your scenarios
- Monitor your activities
- Access your files

### What happens if I uninstall?

**Simple:**
1. Delete the app
2. All data is gone
3. Make sure to export first!

**To keep your data:**
1. Export all scenarios (JSON)
2. Save files somewhere safe
3. You can import them back anytime
4. Then uninstall

### Can I move the app to a different folder?

**Yes!** The app is portable.

Just move the entire folder and it still works.

### Can I run multiple instances?

**Recommended: No**

Running multiple instances might:
- Cause port conflicts
- Lead to data issues
- Create confusion

**Better approach:**
- Use different ports for each
- Or use different machines

### Can I run it from a USB drive?

**Yes!** NexDex is portable.

Just copy to USB and run from there.

**Works on:**
- USB flash drives
- External hard drives
- Network drives (might be slow)
- Anything accessible as a folder

---

## Performance & Limitations

### How many systems can I have?

**Practical limits:**
- Small scenarios: 10-50 systems (easy)
- Medium scenarios: 50-200 systems (normal)
- Large scenarios: 200-500 systems (possible)
- Very large: 500+ systems (depends on hardware)

**Performance factors:**
- Your computer's RAM
- CPU speed
- Number of dependencies
- Complexity of simulations

### How fast is it?

**Typical performance:**
- Load scenario: <1 second
- Run simulation: <5 seconds
- Generate report: <10 seconds
- Compare scenarios: <3 seconds

**Variables:**
- Computer specs
- Scenario complexity
- Number of dependencies
- Report size

### Will it work on old computers?

**Maybe!** Check these:**

1. **OS Support**
   - Windows 7? Probably not
   - Windows 10+? Yes
   - Old macOS? Depends on version

2. **RAM**
   - 2 GB? Barely
   - 4 GB? Good
   - 8 GB+? Perfect

3. **Disk space**
   - 500 MB? Minimum
   - 1 GB? Comfortable
   - 2 GB+? Ideal

**Recommendation:** Update your OS if possible.

### Can I use it on multiple computers?

**Yes, absolutely!**

**You can:**
- Download on multiple machines
- Install on unlimited computers
- Use simultaneously
- No license keys needed
- It's free!

**Tip:** Export and import scenarios between computers.

---

## Troubleshooting

### The app won't start

**Try these steps:**

1. **Make sure you extracted correctly**
   - Should have NexDex.app (or .exe)
   - Not nested in extra folders

2. **Check system requirements**
   - Right OS version?
   - 64-bit processor?
   - Enough RAM?

3. **Try running from terminal**
   - macOS: `./NexDex.app/Contents/MacOS/NexDex`
   - Linux: `./NexDex`
   - This shows error messages

4. **Restart your computer**
   - Simple but effective

5. **Download again**
   - File might be corrupted

**Still stuck?** Check [User Guide](USER-GUIDE.md#troubleshooting)

### Dashboard won't load

**Solutions:**

1. **Wait a few seconds**
   - App needs time to start
   - Browser needs to load

2. **Try manual URL**
   - Open browser
   - Go to: `http://localhost:5000`
   - Press Enter

3. **Check port 5000**
   - Another app might be using it
   - Try: `NEXDEX_PORT=8000` (then go to :8000)

4. **Check browser**
   - Try different browser
   - Clear browser cache
   - Disable extensions

5. **Restart the app**
   - Close completely
   - Wait 5 seconds
   - Open again

### App keeps crashing

**Debug steps:**

1. **Check system requirements** again
2. **Look for error messages**
   - Run from terminal
   - Watch for error text
   - Screenshot if found

3. **Check logs**
   - Look in app folder for logs/
   - Check home folder/.nexdex/ for logs
   - Share error logs when reporting

4. **Report the bug**
   - Go to [GitHub Issues](https://github.com/Arths17/NexDex/issues)
   - Describe what happened
   - Include error messages
   - Describe your system

### File won't download

**Checklist:**

1. **Check internet**
   - Can you access other websites?
   - Is connection stable?
   - Try different network?

2. **Try different browser**
   - Chrome, Firefox, Safari, Edge
   - Disable ad blockers

3. **Check disk space**
   - Need ~500 MB minimum
   - Check with: `df -h` (macOS/Linux)
   - Check with: Properties (Windows)

4. **Try manual download**
   - Right-click download link
   - Select "Save As"
   - Choose location
   - Try again

5. **GitHub alternative**
   - Download from: https://github.com/Arths17/NexDex/releases
   - Same files, different server

---

## Data & Backup

### How do I backup my scenarios?

**Simple process:**

1. **In NexDex dashboard**
   - Go to Scenarios
   - Click Export button
   - Choose JSON format

2. **Save the file**
   - Choose location (Google Drive, Dropbox, USB, etc.)
   - Remember where you put it
   - Consider multiple copies

3. **Back up regularly**
   - After big changes
   - Before major updates
   - Monthly minimum

### How do I restore a backup?

**Simple process:**

1. **In NexDex dashboard**
   - Go to Scenarios
   - Click Import button
   - Choose your JSON file
   - Click Import

2. **Verify import**
   - Check data looks right
   - Run test simulation
   - Confirm everything is there

### What if I lose my data?

**Unfortunately:**
- If not exported, it's gone
- We can't recover deleted data
- This is why backups matter

**Future prevention:**
1. Export scenarios regularly
2. Save multiple copies
3. Use cloud storage backup
4. Schedule regular exports

---

## Licensing & Legal

### Is NexDex really free?

**Yes, 100% free!**

**What free means:**
- ✅ No cost
- ✅ No premium features
- ✅ No payment ever
- ✅ Open source code
- ✅ Forever free

### Can I use it for work?

**Yes, absolutely!**

**Use for:**
- Personal projects
- Business analysis
- Commercial work
- Enterprise use
- Any purpose

**No restrictions on:**
- Personal use
- Commercial use
- Team use
- Large teams
- Any industry

### What's the license?

**Open Source License** (usually MIT or similar)

**You can:**
- Use commercially
- Modify the code
- Distribute it
- Use in closed-source products
- Use without restrictions

**Requirements:**
- Include original license
- Acknowledge original creator
- That's it!

See [LICENSE](../LICENSE) file for details.

### Can I redistribute it?

**Yes!**

**You can:**
- Give it to friends
- Distribute at work
- Post on your site
- Include in your product
- Sell it (with attribution)

**Just remember:**
- Include license file
- Credit the creator
- That's all!

---

## Contributing & Community

### Can I contribute?

**Yes, please!**

**How to contribute:**

1. **Report bugs**
   - Open issue on GitHub
   - Describe the problem
   - Include system info

2. **Suggest features**
   - Open discussion on GitHub
   - Describe what you need
   - Explain why it would help

3. **Fix bugs**
   - Fork repository
   - Fix the issue
   - Send pull request

4. **Improve docs**
   - Found an error?
   - Have better explanation?
   - Submit a fix!

5. **Create plugins**
   - Extend functionality
   - Share with community
   - Help others!

### Where's the community?

**Connect with us:**

- **GitHub Issues**: Report bugs, request features
- **GitHub Discussions**: Ask questions, share ideas
- **GitHub Releases**: Stay updated on new versions
- **Issues/PRs**: Join development discussions

### How often is it updated?

**Current schedule:**
- v1.0.0: Initial release (Feb 2026)
- Future: Regular updates planned

**Stay updated:**
- Watch GitHub repository
- Subscribe to releases
- Check here for announcements

---

## Comparison & Alternatives

### How is NexDex different?

**Unique features:**
- ✅ Completely free
- ✅ Open source
- ✅ No installation needed
- ✅ Runs offline completely
- ✅ Beautiful interface
- ✅ Time-based multipliers
- ✅ Scenario comparison
- ✅ Private (no data collection)

**Other tools might have:**
- More features
- Prettier UI
- Larger teams
- Enterprise support

**But only NexDex has:**
- Everything bundled
- Zero installation
- Complete offline
- Completely free
- Open source code

### Should I switch from [other tool]?

**Consider if you:**
- Want to avoid installation
- Need offline capability
- Want completely free
- Value privacy
- Like open source
- Want simplicity

**Stick with [other tool] if:**
- You need advanced features
- You need team collaboration
- You need enterprise support
- You need integrations
- You want professional support

### Can I use both?

**Yes!**

**NexDex can:**
- Export data
- Import from other tools
- Work alongside other tools
- Complement other solutions

**Many users:**
- Use NexDex for analysis
- Export to Excel for reporting
- Use with other tools
- Combine approaches

---

## Support & Help

### Where do I get help?

**Free help available:**

1. **[User Guide](USER-GUIDE.md)**
   - Complete usage guide
   - Step-by-step instructions
   - Tips and tricks

2. **[Installation Guide](INSTALL.md)**
   - Platform-specific help
   - Troubleshooting steps
   - Common issues

3. **[GitHub Issues](https://github.com/Arths17/NexDex/issues)**
   - Bug reports
   - Feature requests
   - Technical issues

4. **[GitHub Discussions](https://github.com/Arths17/NexDex/discussions)**
   - Questions
   - Ideas
   - Community help

### How do I report a bug?

**Steps:**

1. Check if it's already reported
   - Search GitHub Issues
   - Look for similar problems

2. Gather information
   - What OS? Version?
   - What were you doing?
   - What happened?
   - What did you expect?
   - Error messages?

3. Create new issue
   - Go to GitHub Issues
   - Click "New Issue"
   - Describe problem clearly
   - Include all info
   - Share system details

4. Be patient
   - Maintainers are volunteers
   - Takes time to investigate
   - Updates when progress made

### How do I request a feature?

**Steps:**

1. Check if requested
   - Search discussions
   - Look at issues
   - See what's planned

2. Start discussion
   - Open GitHub Discussion
   - Describe what you need
   - Explain why it would help
   - Suggest implementation

3. Wait for feedback
   - Creator might comment
   - Community might engage
   - Others might want it too

4. Consider contributing
   - If you're technical
   - You could build it
   - And submit it!

---

## Getting More Help

### Need more detailed help?

**Check these resources:**

- [User Guide](USER-GUIDE.md) - Complete usage guide
- [Installation Guide](INSTALL.md) - Platform-specific install
- [Deployment Guide](DEPLOYMENT-GUIDE.md) - Website setup
- [Technical Guide](PACKAGING.md) - For developers
- [GitHub Issues](https://github.com/Arths17/NexDex/issues) - Bug reports
- [GitHub Discussions](https://github.com/Arths17/NexDex/discussions) - Questions

### Still have questions?

**Please:**
1. Check User Guide first
2. Search GitHub Issues
3. Ask in GitHub Discussions
4. Include system information
5. Describe problem clearly

We're here to help!

---

## Quick Links

- **Website**: [nexdex.yoursite.com](index.html)
- **GitHub**: [github.com/Arths17/NexDex](https://github.com/Arths17/NexDex)
- **Issues**: [github.com/Arths17/NexDex/issues](https://github.com/Arths17/NexDex/issues)
- **Discussions**: [github.com/Arths17/NexDex/discussions](https://github.com/Arths17/NexDex/discussions)
- **Download**: [nexdex.yoursite.com](index.html)
- **User Guide**: [USER-GUIDE.md](USER-GUIDE.md)
- **Install Guide**: [INSTALL.md](INSTALL.md)

---

**Last Updated:** February 1, 2026  
**Version:** 1.0.0  
**Status:** Complete & Ready to Help!

*Have a great question we missed? Open an issue or discussion on GitHub!*
