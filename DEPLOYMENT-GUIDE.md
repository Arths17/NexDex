# NexDex - Complete Deployment & Setup Guide

## Overview

This guide helps you deploy NexDex to your website and ensure users can download and run it successfully.

---

## Table of Contents

1. [Website Deployment](#website-deployment)
2. [File Structure](#file-structure)
3. [Setting Up Downloads](#setting-up-downloads)
4. [Hosting Options](#hosting-options)
5. [User Support](#user-support)
6. [Analytics & Tracking](#analytics)
7. [Troubleshooting](#troubleshooting)

---

## Website Deployment

### Quick Setup (5 minutes)

**Step 1: Prepare Files**
```bash
# From NexDex repository
cp website/index.html /var/www/your-domain/
cp -r website/assets /var/www/your-domain/
cp releases/NexDex-Mac.zip /var/www/your-domain/downloads/
```

**Step 2: Create Downloads Directory**
```bash
mkdir -p /var/www/your-domain/downloads
chmod 755 /var/www/your-domain/downloads
```

**Step 3: Upload Files**
- Upload `index.html` to your web root
- Upload `NexDex-Mac.zip` to `/downloads/` folder
- Create download links in HTML

**Step 4: Test**
- Visit your website
- Test all download buttons work
- Verify file downloads correctly

### Full Setup (30 minutes)

**Step 1: Create Directory Structure**
```bash
/your-domain/
├── index.html              (main download page)
├── downloads/              (download files)
│   ├── NexDex-Mac.zip
│   ├── NexDex-Windows.zip  (when ready)
│   └── NexDex-Linux.tar.gz (when ready)
├── docs/                   (documentation)
│   ├── USER-GUIDE.md
│   ├── INSTALL.md
│   └── FAQ.md
├── assets/                 (website assets)
│   ├── logo.png
│   ├── icon.png
│   └── style.css
└── js/                     (JavaScript)
    └── analytics.js        (optional)
```

**Step 2: Copy Website Files**
```bash
# Copy main page
cp website/index.html /var/www/your-domain/

# Copy documentation
cp USER-GUIDE.md /var/www/your-domain/docs/
cp RELEASE-NOTES.md /var/www/your-domain/docs/
cp INSTALL.md /var/www/your-domain/docs/

# Copy release files
mkdir -p /var/www/your-domain/downloads
cp releases/NexDex-Mac.zip /var/www/your-domain/downloads/
```

**Step 3: Update Links in HTML**

Edit `index.html` and update download links:

```html
<!-- Change from -->
<a href="../releases/NexDex-Mac.zip" class="download-btn">Download for macOS</a>

<!-- To -->
<a href="/downloads/NexDex-Mac.zip" class="download-btn">Download for macOS</a>
```

**Step 4: Set Permissions**
```bash
chmod 644 /var/www/your-domain/index.html
chmod 644 /var/www/your-domain/downloads/*.zip
chmod 755 /var/www/your-domain/downloads/
```

**Step 5: Test All Links**
- Visit website homepage
- Click each download button
- Verify file downloads
- Verify file integrity

---

## File Structure

### Local Repository Structure
```
NexDex/
├── website/
│   ├── index.html          ← Main download page
│   └── downloads.html      ← Alternative download page
├── releases/
│   ├── NexDex-Mac.zip      ← macOS app (28 MB)
│   ├── NexDex-Windows.zip  ← Windows app (coming soon)
│   └── NexDex-Linux.tar.gz ← Linux app (coming soon)
├── docs/
│   ├── USER-GUIDE.md       ← User documentation
│   ├── INSTALL.md          ← Installation guide
│   └── RELEASE-NOTES.md    ← Version history
├── dashboard/              ← Flask app code
├── src/                    ← Simulation engine
└── config/                 ← Configuration files
```

### Web Server Structure
```
/var/www/your-domain/
├── index.html              ← Main page (published)
├── downloads/              ← Download folder
│   ├── NexDex-Mac.zip
│   ├── NexDex-Windows.zip
│   └── NexDex-Linux.tar.gz
├── docs/                   ← Documentation
│   ├── user-guide.html
│   ├── install.html
│   └── faq.html
├── assets/                 ← Static assets
│   ├── logo.png
│   ├── styles.css
│   └── favicon.ico
└── api/                    ← Optional API
    ├── version.json
    └── stats.json
```

---

## Setting Up Downloads

### Option 1: Direct File Serving (Recommended)

**Using Nginx:**
```nginx
server {
    listen 80;
    server_name nexdex.yoursite.com;

    root /var/www/nexdex;

    location /downloads/ {
        # Allow downloads
        autoindex on;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        # Serve web pages
        try_files $uri $uri/ =404;
    }
}
```

**Using Apache:**
```apache
<VirtualHost *:80>
    ServerName nexdex.yoursite.com
    DocumentRoot /var/www/nexdex

    <Directory /var/www/nexdex/downloads>
        Options Indexes FollowSymLinks
        AllowOverride None
        Allow from all
    </Directory>

    <Directory /var/www/nexdex>
        Options -Indexes FollowSymLinks
        AllowOverride None
        Allow from all
    </Directory>
</VirtualHost>
```

### Option 2: GitHub Releases

**Use GitHub to host files:**
```html
<a href="https://github.com/Arths17/NexDex/releases/download/v1.0.0/NexDex-Mac.zip" 
   class="download-btn">Download for macOS</a>
```

**Advantages:**
- No server space needed
- Built-in version control
- Automatic CDN
- Easy release management

**Disadvantages:**
- Depends on GitHub availability
- Rate limiting possible

### Option 3: Hybrid Approach

**Host index.html on your site, files on GitHub:**
```
Your Website → index.html (showing all download options)
                    ↓
              GitHub Releases (serves actual files)
                    ↓
              Users download files
```

---

## Hosting Options

### Self-Hosted (Full Control)

**Pros:**
- Complete control
- No dependency on third parties
- Custom analytics
- Branding flexibility

**Cons:**
- Maintenance required
- Bandwidth costs
- Infrastructure needed

**Setup:**
```bash
# 1. Get web server (Nginx, Apache, etc.)
# 2. Create directories
mkdir -p /var/www/nexdex/downloads

# 3. Copy files
cp website/index.html /var/www/nexdex/
cp releases/NexDex-Mac.zip /var/www/nexdex/downloads/

# 4. Set permissions
chmod 755 /var/www/nexdex/downloads
chmod 644 /var/www/nexdex/index.html

# 5. Configure web server (see above)
```

### GitHub Pages (Free)

**Pros:**
- Free hosting
- Git integration
- Automatic HTTPS
- Good for static content

**Cons:**
- File size limits
- No dynamic content
- Limited customization

**Setup:**
```bash
# 1. Create gh-pages branch
git checkout -b gh-pages

# 2. Create site folder
mkdir site
cp website/index.html site/
cp USER-GUIDE.md site/guide.md

# 3. Push to GitHub
git add site/
git commit -m "Deploy website"
git push origin gh-pages

# 4. Enable in GitHub settings
# → Settings → Pages → Select gh-pages branch
```

### Netlify (Easy & Free)

**Pros:**
- Free tier
- Easy deployment
- Automatic HTTPS
- Good performance

**Cons:**
- File size limits (50MB free tier)
- Limited storage
- Third-party dependency

**Setup:**
```bash
# 1. Create netlify.toml
cat > netlify.toml << 'EOF'
[build]
  publish = "website"

[[redirects]]
  from = "/downloads/*"
  to = "https://github.com/Arths17/NexDex/releases/download/v1.0.0/:splat"
  status = 302
EOF

# 2. Push to GitHub
# 3. Connect repo to Netlify
# 4. Deploy automatically
```

### AWS S3 + CloudFront

**Pros:**
- Scalable
- Pay-as-you-go
- CDN included
- Very fast

**Cons:**
- Costs money
- More complex setup
- AWS account needed

**Setup:**
```bash
# 1. Create S3 bucket
aws s3 mb s3://nexdex-downloads

# 2. Upload files
aws s3 cp website/index.html s3://nexdex-downloads/
aws s3 cp releases/NexDex-Mac.zip s3://nexdex-downloads/downloads/

# 3. Enable CloudFront
# (via AWS console)

# 4. Point domain
# (DNS CNAME record)
```

---

## User Support

### Download Assistance

**Help users who can't download:**

1. **Check browser**
   - Recommend: Chrome, Firefox, Safari, Edge
   - Disable ad blockers

2. **Check connection**
   - Ask: Can you open other websites?
   - Try different network

3. **Check file**
   - Verify download size (should be ~28 MB for macOS)
   - Check MD5 hash if provided

**MD5 Hashes:**
```
NexDex-Mac.zip:     (get with `md5 NexDex-Mac.zip`)
NexDex-Windows.zip: (coming soon)
NexDex-Linux.tar.gz: (coming soon)
```

### Installation Support

**Common Issues:**

1. **"Cannot open" on macOS**
   ```bash
   # Solution: Right-click → Open
   # Or: xattr -d com.apple.quarantine /path/to/NexDex.app
   ```

2. **Windows Defender warning**
   - Click "More info"
   - Click "Run anyway"
   - This is normal for unsigned apps

3. **Port 5000 in use**
   - Close other apps using port 5000
   - Or set: `NEXDEX_PORT=8000`

---

## Analytics & Tracking

### Optional: Track Downloads

**Add to index.html:**
```html
<script>
// Track download clicks
document.querySelectorAll('.download-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        // Send to analytics
        if (window.gtag) {
            gtag('event', 'download', {
                'platform': this.dataset.platform,
                'version': '1.0.0'
            });
        }
    });
});
</script>
```

### Version Check API (Optional)

**Create `/api/version.json`:**
```json
{
  "version": "1.0.0",
  "released": "2026-02-01",
  "latest": "1.0.0",
  "downloads": {
    "macos": {
      "version": "1.0.0",
      "url": "/downloads/NexDex-Mac.zip",
      "size": "28 MB",
      "released": "2026-02-01"
    },
    "windows": {
      "version": "coming-soon",
      "url": null,
      "size": null
    },
    "linux": {
      "version": "coming-soon",
      "url": null,
      "size": null
    }
  }
}
```

---

## Troubleshooting

### Website Won't Load

**Problem:** 404 error or blank page

**Solutions:**
1. Check file exists: `ls -la /var/www/nexdex/index.html`
2. Check permissions: `chmod 644 /var/www/nexdex/index.html`
3. Check web server: `nginx -t` or `apache2ctl configtest`
4. Check DNS: `nslookup nexdex.yoursite.com`

### Downloads Won't Start

**Problem:** Click button, nothing happens

**Solutions:**
1. Check file exists: `ls -la /var/www/nexdex/downloads/`
2. Check MIME type: `file NexDex-Mac.zip`
3. Test direct link in browser
4. Check server logs: `tail -f /var/log/nginx/error.log`

### Files Too Large

**Problem:** Only some files download

**Solutions:**
1. Check disk space: `df -h`
2. Check upload limits in web server
3. Check file size: `ls -lh releases/`
4. Consider using GitHub releases instead

### Slow Downloads

**Problem:** Downloads take too long

**Solutions:**
1. Enable gzip compression
2. Use CDN (CloudFront, CloudFlare, etc.)
3. Check server bandwidth
4. Host files closer to users

**Nginx gzip example:**
```nginx
gzip on;
gzip_types text/html text/plain application/json;
gzip_min_length 1000;
gzip_comp_level 6;
```

---

## Checklist for Launch

- [ ] Website files uploaded
- [ ] Download files in correct location
- [ ] All links tested and working
- [ ] File permissions set correctly
- [ ] MIME types configured
- [ ] Web server restarted
- [ ] DNS pointing correctly
- [ ] SSL/HTTPS enabled
- [ ] Analytics configured (optional)
- [ ] Documentation accessible
- [ ] User support plan ready
- [ ] Backup system in place

---

## Maintenance

### Regular Tasks

**Weekly:**
- Check website load times
- Verify all links work
- Monitor error logs

**Monthly:**
- Review download statistics
- Check server health
- Update documentation

**Quarterly:**
- Security updates
- Performance optimization
- Backup verification

---

## Support & Updates

**For issues:**
- Check: [GitHub Issues](https://github.com/Arths17/NexDex/issues)
- Ask: [GitHub Discussions](https://github.com/Arths17/NexDex/discussions)

**For updates:**
- Subscribe to: [GitHub Releases](https://github.com/Arths17/NexDex/releases)
- Watch: [NexDex Repository](https://github.com/Arths17/NexDex)

---

## Need Help?

1. **Website issues?** → See "Troubleshooting" section
2. **User questions?** → Share [USER-GUIDE.md](USER-GUIDE.md)
3. **Tech questions?** → Check [PACKAGING.md](../PACKAGING.md)
4. **Bugs?** → Report on [GitHub Issues](https://github.com/Arths17/NexDex/issues)

---

*Version: 1.0*
*Last Updated: February 1, 2026*
*Status: Complete & Production-Ready*
