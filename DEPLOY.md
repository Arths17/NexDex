# 🌐 GitHub Pages Deployment Guide

Quick reference for deploying the NexDex website to GitHub Pages.

## 🚀 Quick Deploy (5 minutes)

### Step 1: Prepare the Release Package
```bash
# Create the free download package
mkdir -p releases
zip -r releases/NexDex-free.zip \
  nexdex.py requirements.txt README.md config/ scenarios/ src/ \
  -x "*.pyc" "__pycache__/*" "*.git*" "website/*" "reports/*"
```

### Step 2: Push to GitHub
```bash
# Add all website files
git add website/ releases/
git commit -m "Add NexDex landing page and release package"
git push origin main
```

### Step 3: Enable GitHub Pages
1. Go to your GitHub repository
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**:
   - Branch: `main`
   - Folder: `/website` (if this option exists)
   - OR use Method 2 below for gh-pages branch
4. Click **Save**
5. Wait 2-5 minutes for deployment

### Step 4: Access Your Site
Your site will be live at:
```
https://yourusername.github.io/NexDex/website/
```

## 🎯 Method 2: Deploy to gh-pages Branch (Recommended)

This method creates a dedicated branch for your website:

```bash
# Option A: Manual deployment
git subtree push --prefix website origin gh-pages

# Option B: Using gh-pages CLI (install first: npm install -g gh-pages)
gh-pages -d website -b gh-pages
```

Then in GitHub:
- **Settings** → **Pages**
- Select `gh-pages` branch
- Your site will be at: `https://yourusername.github.io/NexDex/`

## 📝 Before You Deploy - Checklist

- [ ] Update repository URLs in `website/index.html` (search for `yourusername`)
- [ ] Replace email addresses: `enterprise@nexdex.io`, `support@nexdex.io`
- [ ] Create `releases/NexDex-free.zip` package
- [ ] Test website locally: `cd website && python3 -m http.server 8000`
- [ ] Replace placeholder screenshots in `website/assets/screenshots/` (optional)
- [ ] Review and customize colors in `website/style.css` (optional)

## 🎨 Customization Quick Reference

### Update GitHub URLs
```bash
# Find and replace in website/index.html
# Replace: https://github.com/yourusername/NexDex
# With: https://github.com/YOUR-ACTUAL-USERNAME/NexDex
```

### Update Contact Emails
```bash
# In website/index.html, replace:
enterprise@nexdex.io  → your-enterprise@email.com
support@nexdex.io     → your-support@email.com
```

### Change Brand Colors
Edit `website/style.css`:
```css
:root {
    --primary-color: #6366f1;    /* Your primary color */
    --secondary-color: #8b5cf6;  /* Your secondary color */
}
```

## 🧪 Local Testing

Test before deploying:

```bash
# Method 1: Python
cd website
python3 -m http.server 8000
open http://localhost:8000

# Method 2: PHP
cd website
php -S localhost:8000
```

## 🔧 Troubleshooting

### Site returns 404
- Verify GitHub Pages is enabled
- Check the correct branch and folder are selected
- Ensure `index.html` exists in the selected location
- Wait 5-10 minutes and clear browser cache

### Download link broken
- Ensure `releases/NexDex-free.zip` exists
- Check the file is pushed to GitHub
- Verify the path in `index.html` matches your setup

### CSS not loading
- Check file paths are correct (case-sensitive on GitHub Pages)
- Ensure `style.css` is in the same directory as `index.html`
- Clear browser cache (Cmd+Shift+R / Ctrl+Shift+R)

### Mobile menu not working
- JavaScript is embedded in `index.html`
- Check browser console for errors (F12)
- Test in different browsers

## 📱 Mobile Testing

Test responsiveness before deploying:
1. Open DevTools (F12)
2. Toggle Device Toolbar (Cmd+Shift+M / Ctrl+Shift+M)
3. Test on iPhone, iPad, and Android sizes

## 🌟 Post-Deployment

After successful deployment:

1. **Share your site**: Add the URL to your README.md
2. **Monitor traffic**: Enable GitHub Pages analytics
3. **SEO**: Add meta tags in `index.html` (title, description)
4. **Custom domain** (optional): Add CNAME file and configure DNS

## 📊 Adding Analytics (Optional)

Add Google Analytics to track visitors:

1. Get your GA tracking ID
2. Add before `</head>` in `index.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🔄 Updating the Website

After making changes:

```bash
# Edit files in website/
git add website/
git commit -m "Update website"
git push origin main

# If using gh-pages:
gh-pages -d website -b gh-pages
```

Changes will be live in 1-2 minutes.

## 🎉 Success Checklist

After deployment, verify:
- [ ] Homepage loads correctly
- [ ] Navigation works (all sections scroll smoothly)
- [ ] Download button exists (link to releases/NexDex-free.zip)
- [ ] Enterprise contact link works (mailto)
- [ ] Mobile menu toggles properly
- [ ] All sections are visible and styled correctly
- [ ] Footer links point to correct URLs
- [ ] Site is responsive on mobile/tablet

---

**Need help?** Check the detailed guide in `website/README.md`

**Report issues:** Create an issue on GitHub with:
- Browser and version
- Device (desktop/mobile)
- Screenshot of the problem
- Steps to reproduce
