# NexDex Website

This folder contains the GitHub Pages website for NexDex.

## 🌐 Live Demo

Visit: `https://yourusername.github.io/NexDex/website/`

## 📁 Structure

```
website/
├── index.html              # Main landing page
├── style.css               # Styles and responsive design
├── assets/
│   └── screenshots/        # SVG placeholder screenshots
│       ├── ascii-report.svg
│       ├── html-report.svg
│       └── dependency-graph.svg
└── README.md              # This file
```

## 🚀 Deployment to GitHub Pages

### Method 1: Deploy from main branch

1. **Push to GitHub**
   ```bash
   git add website/
   git commit -m "Add NexDex landing page"
   git push origin main
   ```

2. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select `main` branch
   - Set folder to `/ (root)` or `/docs` (if you move website files there)
   - Click **Save**

3. **Access your site**
   - GitHub will build and deploy your site
   - Visit: `https://yourusername.github.io/NexDex/website/`

### Method 2: Deploy to gh-pages branch (Recommended)

1. **Create releases directory** (for free download link)
   ```bash
   mkdir -p releases
   # Create a zip of your project
   zip -r releases/NexDex-free.zip . -x "*.git*" "website/*" "reports/*"
   ```

2. **Install gh-pages** (optional, for automated deployment)
   ```bash
   npm install -g gh-pages
   ```

3. **Deploy to gh-pages branch**
   ```bash
   # From project root
   gh-pages -d website -b gh-pages
   ```

4. **Configure GitHub Pages**
   - Go to **Settings** → **Pages**
   - Select `gh-pages` branch
   - Click **Save**

5. **Your site will be live at:**
   - `https://yourusername.github.io/NexDex/`

### Method 3: Custom Domain (Optional)

1. **Add CNAME file** in `website/` folder:
   ```bash
   echo "nexdex.yourdomain.com" > website/CNAME
   ```

2. **Configure DNS** at your domain provider:
   - Add CNAME record pointing to `yourusername.github.io`

3. **Enable in GitHub Pages settings**
   - Enter custom domain in GitHub Pages settings
   - Enable "Enforce HTTPS"

## 🎨 Customization

### Update Repository Links

Replace all instances of `https://github.com/yourusername/NexDex` with your actual GitHub URL in:
- [index.html](index.html) - Navigation, footer, download instructions
- This README

### Add Actual Screenshots

Replace placeholder SVGs in `assets/screenshots/` with real screenshots:
1. Generate reports using NexDex
2. Take screenshots (or use HTML export)
3. Optimize images (recommended: use WebP format, < 500KB each)
4. Replace SVG files with actual images

### Update Contact Information

Replace email addresses in [index.html](index.html):
- `enterprise@nexdex.io` → your enterprise contact email
- `support@nexdex.io` → your support email

### Customize Colors

Edit CSS variables in [style.css](style.css):
```css
:root {
    --primary-color: #6366f1;    /* Main brand color */
    --secondary-color: #8b5cf6;  /* Accent color */
    /* ... other colors ... */
}
```

## 📦 Creating the Free Download Package

Generate the `releases/NexDex-free.zip` file:

```bash
# From project root
mkdir -p releases
zip -r releases/NexDex-free.zip \
  nexdex.py \
  requirements.txt \
  README.md \
  config/ \
  scenarios/ \
  src/ \
  -x "*.pyc" "__pycache__/*" "*.git*" "website/*" "reports/*"
```

Place this zip file in the `releases/` folder for the download button to work.

## 🧪 Local Testing

Test the website locally before deploying:

### Option 1: Python HTTP Server
```bash
cd website
python3 -m http.server 8000
# Visit: http://localhost:8000
```

### Option 2: VS Code Live Server
1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

### Option 3: Simple File Open
- Open `website/index.html` directly in your browser
- Note: Some features may not work from `file://` protocol

## 📱 Mobile Responsiveness

The website is fully responsive with breakpoints at:
- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

Test on different screen sizes using browser DevTools (F12 → Toggle Device Toolbar).

## 🎯 Features Included

✅ **Hero Section** - Product showcase with terminal preview  
✅ **Features Grid** - 9 key features with icons  
✅ **Download Section** - Free vs Enterprise comparison  
✅ **Installation Guide** - Copy-paste terminal commands  
✅ **Enterprise CTA** - Feature comparison table  
✅ **Documentation Links** - Guides and examples  
✅ **Report Gallery** - Placeholder screenshots  
✅ **Footer** - Links, license info, contact  
✅ **Mobile Menu** - Hamburger navigation for mobile  
✅ **Smooth Scrolling** - Anchor link animations  
✅ **Copy Code Button** - One-click command copying  

## 🔧 Troubleshooting

### Site not loading?
- Check GitHub Pages is enabled in repository settings
- Ensure `index.html` is in the selected folder/branch
- Wait 2-5 minutes after first deployment for DNS propagation

### Download link broken?
- Create `releases/NexDex-free.zip` file (see instructions above)
- Push to GitHub: `git add releases/ && git commit -m "Add release" && git push`

### Custom domain not working?
- Verify CNAME file exists in deployed folder
- Check DNS records at your domain provider
- Enable HTTPS in GitHub Pages settings

## 📄 License

This website is part of NexDex and is released under the same MIT License.

## 🤝 Contributing

To improve the website:
1. Edit files in `website/` folder
2. Test locally
3. Commit and push changes
4. Redeploy to GitHub Pages (automatic with gh-pages branch)

---

**Built with ❤️ for the NexDex project**
