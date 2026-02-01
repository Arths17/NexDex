# 🚀 How to Publish NexDex Website to GitHub Pages

## ✅ Step 1: Update Your GitHub Username

Replace `yourusername` in the website with your actual GitHub username:

```bash
# For macOS:
sed -i '' 's/yourusername/YOUR-GITHUB-USERNAME/g' website/index.html

# For Linux:
sed -i 's/yourusername/YOUR-GITHUB-USERNAME/g' website/index.html
```

Or manually edit `website/index.html` and search/replace `yourusername`.

---

## ✅ Step 2: Commit and Push to GitHub

```bash
# Add all website files
git add website/ releases/ deploy.sh DEPLOY.md WEBSITE-COMPLETE.md QUICK-START.txt

# Commit
git commit -m "Add NexDex landing page"

# Push to GitHub
git push origin main
```

---

## ✅ Step 3: Enable GitHub Pages

1. **Go to your repository on GitHub**
   - Navigate to: `https://github.com/YOUR-USERNAME/NexDex`

2. **Open Settings**
   - Click the **"Settings"** tab (top right)

3. **Navigate to Pages**
   - Click **"Pages"** in the left sidebar

4. **Configure Source**
   - Under **"Source"**:
     - Branch: Select **`main`**
     - Folder: Select **`/ (root)`**
   - Click **"Save"**

5. **Wait for Deployment**
   - GitHub will build your site (takes 2-5 minutes)
   - You'll see a blue notification at the top when ready

---

## 🌐 Your Website URL

After deployment, your site will be live at:

```
https://YOUR-GITHUB-USERNAME.github.io/NexDex/website/
```

---

## 🎯 Alternative: Clean URL with gh-pages (Recommended)

For a cleaner URL without `/website/` in the path:

### Option 1: Using gh-pages NPM package
```bash
# Install gh-pages globally (one-time)
npm install -g gh-pages

# Deploy website folder to gh-pages branch
gh-pages -d website -b gh-pages
```

### Option 2: Using git subtree
```bash
# Deploy website folder to gh-pages branch
git subtree push --prefix website origin gh-pages
```

### Then in GitHub Settings → Pages:
- Source: Select **`gh-pages`** branch
- Folder: **`/ (root)`**
- Save

**Your site will now be at:**
```
https://YOUR-GITHUB-USERNAME.github.io/NexDex/
```

---

## 📝 Pre-Deployment Checklist

- [x] Release package created (`releases/NexDex-free.zip`) ✓
- [ ] Updated GitHub username in `website/index.html`
- [ ] Updated email addresses (optional):
  - `enterprise@nexdex.io` → your email
  - `support@nexdex.io` → your email
- [ ] Tested locally (docs links should work now!)
- [ ] Committed and pushed to GitHub
- [ ] Enabled GitHub Pages in Settings

---

## 🧪 Test Locally First

Before deploying, test the site:

```bash
cd website
python3 -m http.server 8000
# Open: http://localhost:8000
```

**Test these:**
- ✓ Navigation menu works
- ✓ All sections scroll smoothly
- ✓ Download button is present (will work after GitHub deploy)
- ✓ Documentation links work (now point to local README)
- ✓ Mobile menu toggles (resize window)
- ✓ Code copy buttons work

---

## 🔧 Troubleshooting

### Site returns 404
- Verify GitHub Pages is enabled (Settings → Pages)
- Check correct branch and folder selected
- Wait 5-10 minutes, clear browser cache

### Documentation links broken
- Links now point to `../README.md` (will work on GitHub Pages)
- Locally they should open the README file

### Download link returns 404
- Ensure `releases/NexDex-free.zip` exists ✓ (Already created!)
- Make sure it's pushed to GitHub

---

## 📊 Quick Deploy Script

Use the automated script:

```bash
./deploy.sh
```

This will:
1. Create release package (already done!)
2. Prompt for GitHub username
3. Update links automatically
4. Commit and push to GitHub
5. Show you next steps

---

## 🎉 After Deployment

Once live:

1. **Share your URL** - Add to your main README
2. **Test thoroughly** - Check all links and features
3. **Monitor** - Check GitHub Pages status in Settings → Pages
4. **Optional**: Add custom domain (CNAME file)
5. **Optional**: Enable HTTPS (automatically enabled by GitHub)

---

## 💡 Pro Tips

- **Custom Domain**: Add a `CNAME` file with your domain
- **Analytics**: Add Google Analytics tracking code
- **Screenshots**: Replace SVG placeholders with real images
- **Social Media**: Add Open Graph meta tags for better sharing

---

**Ready to go live? Run the commands in Step 2 above! 🚀**
