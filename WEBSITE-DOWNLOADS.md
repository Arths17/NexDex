# 🌐 Website Update Guide: Adding NexDex Downloads

This guide shows how to update your website to offer downloadable NexDex standalone applications for Mac, Windows, and Linux.

## Step 1: Build the Apps

First, build the standalone applications on each platform (or at least the ones you want to support):

```bash
# On Mac
bash build_mac.sh

# On Windows
bash build_windows.bat

# On Linux
bash build_linux.sh
```

These create distribution archives in the `releases/` folder:
- `NexDex-Mac.zip` (~150MB)
- `NexDex-Windows.zip` (~150MB)
- `NexDex-Linux.tar.gz` (~100MB)

## Step 2: Upload to Your Website

Place the `.zip` and `.tar.gz` files in a `releases/` directory on your web server:

```
yourserver.com/
├── releases/
│   ├── NexDex-Mac.zip
│   ├── NexDex-Windows.zip
│   └── NexDex-Linux.tar.gz
└── index.html
```

## Step 3: Update Download Page HTML

### Simple Download Section

Add this to your website's HTML (e.g., `index.html` or `downloads.html`):

```html
<section class="downloads">
  <h2>📥 Download NexDex</h2>
  <p>Download the standalone application for your platform. No installation required—just download, extract, and run!</p>
  
  <div class="download-grid">
    <!-- Mac Download -->
    <div class="download-card">
      <h3>🍎 macOS</h3>
      <p>Intel & Apple Silicon</p>
      <p class="size">~150 MB</p>
      <a href="releases/NexDex-Mac.zip" download class="btn btn-primary">
        Download for Mac
      </a>
      <p class="instructions">
        1. Download & extract<br>
        2. Double-click NexDex.app<br>
        3. Dashboard opens automatically
      </p>
    </div>
    
    <!-- Windows Download -->
    <div class="download-card">
      <h3>🪟 Windows</h3>
      <p>Windows 10 & 11 (64-bit)</p>
      <p class="size">~150 MB</p>
      <a href="releases/NexDex-Windows.zip" download class="btn btn-primary">
        Download for Windows
      </a>
      <p class="instructions">
        1. Download & extract<br>
        2. Double-click NexDex.exe<br>
        3. Dashboard opens automatically
      </p>
    </div>
    
    <!-- Linux Download -->
    <div class="download-card">
      <h3>🐧 Linux</h3>
      <p>Glibc 2.17+ (Ubuntu 16.04+, CentOS 7+)</p>
      <p class="size">~100 MB</p>
      <a href="releases/NexDex-Linux.tar.gz" download class="btn btn-primary">
        Download for Linux
      </a>
      <p class="instructions">
        1. Download & extract<br>
        2. chmod +x NexDex<br>
        3. ./NexDex
      </p>
    </div>
  </div>
</section>
```

### Styled CSS (Bootstrap example)

```html
<style>
  .downloads {
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin: 2rem 0;
  }

  .downloads h2 {
    text-align: center;
    margin-bottom: 1rem;
    font-size: 2.5rem;
  }

  .downloads > p {
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.9;
  }

  .download-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

  .download-card {
    background: rgba(255, 255, 255, 0.95);
    color: #333;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .download-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  }

  .download-card h3 {
    font-size: 1.8rem;
    margin: 0 0 0.5rem 0;
  }

  .download-card p {
    margin: 0.5rem 0;
  }

  .download-card .size {
    font-size: 0.9rem;
    color: #666;
    margin: 1rem 0;
  }

  .download-card .btn {
    display: inline-block;
    padding: 0.8rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    margin: 1rem 0;
    font-weight: bold;
    transition: all 0.3s ease;
  }

  .download-card .btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  .download-card .instructions {
    font-size: 0.85rem;
    color: #666;
    line-height: 1.6;
    margin-top: 1rem;
    text-align: left;
  }
</style>
```

## Step 4: Add System Requirements & Features

### Full Download Section Template

```html
<section class="features-downloads">
  <div class="container">
    <!-- Features List -->
    <div class="features">
      <h3>✨ What's Included</h3>
      <ul>
        <li>✅ Interactive Web Dashboard</li>
        <li>✅ Scenario Management & Comparison</li>
        <li>✅ Impact Analysis Reports</li>
        <li>✅ Service Dependency Mapping</li>
        <li>✅ Peak Hours Impact Modeling</li>
        <li>✅ HTML & Markdown Reports</li>
        <li>✅ 100% Local - No Cloud Required</li>
      </ul>
    </div>

    <!-- System Requirements -->
    <div class="requirements">
      <h3>📋 System Requirements</h3>
      
      <h4>macOS</h4>
      <ul>
        <li>macOS 10.13 or later</li>
        <li>Intel or Apple Silicon</li>
        <li>150 MB free disk space</li>
      </ul>

      <h4>Windows</h4>
      <ul>
        <li>Windows 10 or Windows 11 (64-bit)</li>
        <li>150 MB free disk space</li>
      </ul>

      <h4>Linux</h4>
      <ul>
        <li>glibc 2.17+ (Ubuntu 16.04+, CentOS 7+, etc.)</li>
        <li>100 MB free disk space</li>
      </ul>
    </div>

    <!-- Quick Start -->
    <div class="quickstart">
      <h3>🚀 Quick Start</h3>
      <ol>
        <li>Download the app for your platform</li>
        <li>Extract the archive</li>
        <li>Double-click the app (or run from terminal)</li>
        <li>Dashboard opens automatically in your browser</li>
        <li>Start running simulations!</li>
      </ol>
    </div>
  </div>
</section>
```

## Step 5: Update Navigation

Add a prominent download link in your navigation bar:

```html
<nav class="navbar">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/features">Features</a></li>
    <li><a href="/downloads" class="btn-download">📥 Download</a></li>
    <li><a href="/docs">Documentation</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

## Step 6: Create a Dedicated Downloads Page

Create a new page (e.g., `/downloads.html` or `/downloads/index.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Download NexDex - Business Impact Simulator</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <!-- Header -->
  <header>
    <h1>📥 Download NexDex</h1>
    <p>Get the standalone application running on your computer in minutes</p>
  </header>

  <!-- Downloads Section -->
  <main>
    <section class="downloads">
      <!-- Download cards here (from Step 3) -->
    </section>

    <!-- FAQ Section -->
    <section class="faq">
      <h2>❓ Frequently Asked Questions</h2>
      
      <div class="faq-item">
        <h4>Do I need to install anything?</h4>
        <p>No! Just download, extract, and run. No installation required.</p>
      </div>

      <div class="faq-item">
        <h4>Does it require internet?</h4>
        <p>No, NexDex runs completely locally. Your data never leaves your computer.</p>
      </div>

      <div class="faq-item">
        <h4>Can I see the source code?</h4>
        <p>Yes! Visit our <a href="https://github.com/yourrepo/nexdex">GitHub repository</a> to explore the code.</p>
      </div>

      <div class="faq-item">
        <h4>What if I have issues?</h4>
        <p>Check the <a href="/docs/INSTALL.md">installation guide</a> or <a href="https://github.com/yourrepo/nexdex/issues">create an issue</a>.</p>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer>
    <p>© 2026 NexDex. Built with ❤️ for engineers.</p>
  </footer>
</body>
</html>
```

## Step 7: Update Documentation Links

Add links in your documentation to the installation guide:

```markdown
# Getting Started with NexDex

## Option 1: Standalone Application (Recommended)
Download the pre-built app for your platform:
- [macOS](../releases/NexDex-Mac.zip)
- [Windows](../releases/NexDex-Windows.zip)
- [Linux](../releases/NexDex-Linux.tar.gz)

See [Installation Guide](INSTALL.md) for detailed instructions.

## Option 2: Run from Source
```

## Step 8: Add Analytics & Tracking (Optional)

Track downloads with Google Analytics:

```html
<a href="releases/NexDex-Mac.zip" 
   onclick="gtag('event', 'file_download', {'file_name': 'NexDex-Mac.zip'})"
   download>
  Download for Mac
</a>
```

## Step 9: Create Release Notes

Add version information to your downloads page:

```html
<div class="release-info">
  <h3>Latest Release: v1.0.0</h3>
  <p><strong>Released:</strong> February 1, 2026</p>
  <h4>What's New:</h4>
  <ul>
    <li>✨ Web dashboard with scenario management</li>
    <li>🔄 Scenario comparison with visual indicators</li>
    <li>📊 Peak hours impact multipliers (1.2x)</li>
    <li>📄 HTML & Markdown report generation</li>
    <li>🎨 Responsive design for desktop & tablet</li>
  </ul>
  <a href="CHANGELOG.md">View full changelog →</a>
</div>
```

## Step 10: Test Everything

Before deploying:

1. **Test all download links** - Ensure files download correctly
2. **Test on all platforms** - Download and run on Mac, Windows, Linux
3. **Test file integrity** - Verify ZIP/TAR.GZ checksums
4. **Test page performance** - Check load times and responsiveness
5. **Test mobile view** - Ensure responsive design works

### Add Checksums for Security

```html
<details>
  <summary>🔒 Verify Download Integrity</summary>
  <pre>
macOS:
SHA-256: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

Windows:
SHA-256: q1r2s3t4u5v6w7x8y9z0a1b2c3d4e5f6

Linux:
SHA-256: g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2
  </pre>
</details>
```

## Example: Complete Downloads Page

See `website/downloads.html` for a complete working example with all styling and functionality.

## Deployment Checklist

- [ ] Apps built for all platforms
- [ ] Files uploaded to server
- [ ] Download links updated
- [ ] Navigation updated
- [ ] System requirements documented
- [ ] Installation guide linked
- [ ] FAQ section added
- [ ] Release notes added
- [ ] All links tested
- [ ] Page responsive on mobile
- [ ] Analytics set up

## Monitoring Downloads

Track popular platforms:

```javascript
// Example: Log download events
document.querySelectorAll('[data-platform]').forEach(link => {
  link.addEventListener('click', () => {
    const platform = link.dataset.platform;
    console.log(`Download started: ${platform}`);
    // Send to analytics
  });
});
```

---

## Next Steps

1. ✅ Build apps on each platform
2. ✅ Upload to web server
3. ✅ Update HTML with download links
4. ✅ Test all downloads
5. ✅ Monitor user feedback
6. ✅ Update with bug fixes as needed

Your NexDex downloads are now live! 🚀
