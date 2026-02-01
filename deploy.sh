#!/bin/bash
# NexDex Website Deployment Script
# This script deploys the website to GitHub Pages

echo "🚀 NexDex GitHub Pages Deployment"
echo "=================================="
echo ""

# Step 1: Create release package
echo "📦 Step 1: Creating release package..."
mkdir -p releases
if [ -f "releases/NexDex-free.zip" ]; then
    echo "   ✓ Release package already exists"
else
    echo "   Creating NexDex-free.zip..."
    zip -r releases/NexDex-free.zip \
        nexdex.py requirements.txt README.md config/ scenarios/ src/ \
        -x "*.pyc" "__pycache__/*" "*.git*" "website/*" "reports/*" "*.DS_Store" > /dev/null 2>&1
    echo "   ✓ Created releases/NexDex-free.zip"
fi
echo ""

# Step 2: Update GitHub username
echo "📝 Step 2: Update GitHub username..."
read -p "   Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "   ⚠️  Skipping username update"
else
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/yourusername/$github_username/g" website/index.html
    else
        sed -i "s/yourusername/$github_username/g" website/index.html
    fi
    echo "   ✓ Updated username to: $github_username"
fi
echo ""

# Step 3: Git operations
echo "📤 Step 3: Commit and push to GitHub..."
git add website/ releases/ DEPLOY.md WEBSITE-COMPLETE.md QUICK-START.txt
git commit -m "Add NexDex landing page and website assets"
git push origin main
echo "   ✓ Pushed to GitHub"
echo ""

# Step 4: Instructions
echo "✅ Files pushed to GitHub!"
echo ""
echo "📋 NEXT STEPS:"
echo "   1. Go to your GitHub repository"
echo "   2. Click: Settings → Pages"
echo "   3. Under 'Source':"
echo "      - Branch: main"
echo "      - Folder: /website (or / if using gh-pages)"
echo "   4. Click 'Save'"
echo "   5. Wait 2-5 minutes"
echo ""
echo "🌐 Your site will be live at:"
echo "   https://$github_username.github.io/NexDex/website/"
echo ""
echo "💡 TIP: For cleaner URL (without /website/):"
echo "   Run: gh-pages -d website -b gh-pages"
echo "   Then in Settings → Pages, select 'gh-pages' branch"
echo "   Site will be: https://$github_username.github.io/NexDex/"
echo ""
echo "Done! 🎉"
