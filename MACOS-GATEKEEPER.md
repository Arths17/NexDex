# macOS Gatekeeper Warning

If you see a warning that says "Apple could not verify NexDex is free of malware", follow these steps:

## Quick Fix (Recommended)

### Method 1: Right-Click Open
1. Open **Finder**
2. Navigate to where you downloaded **NexDex.app**
3. **Right-click** (or Control+click) on `NexDex.app`
4. Click **"Open"** from the menu
5. Click **"Open"** again in the security dialog

The app will now open and won't show the warning again.

### Method 2: Terminal Command (Fastest)
Open Terminal and run:

```bash
xattr -cr ~/Downloads/NexDex.app
open ~/Downloads/NexDex.app
```

### Method 3: Use Our Script
If you downloaded the full repository:

```bash
chmod +x remove_quarantine.sh
./remove_quarantine.sh ~/Downloads/NexDex.app
```

## Alternative: System Preferences

If the above don't work:

1. Go to **System Preferences** → **Security & Privacy**
2. Click the **General** tab
3. Look for a message about NexDex being blocked
4. Click **"Open Anyway"**
5. Enter your password if prompted

## Why This Happens

NexDex is an open-source app built locally and not signed with an Apple Developer certificate. macOS Gatekeeper protects you from potentially malicious software by warning you about unsigned apps.

## Is It Safe?

Yes! NexDex is:
- ✅ **Open source** - Source code visible on [GitHub](https://github.com/Arths17/NexDex)
- ✅ **No malware** - Built from trusted Python packages
- ✅ **No internet required** - Runs completely offline
- ✅ **No data collection** - Doesn't send any data anywhere

## Getting a Proper Code Signature (For Developers)

If you want to distribute a code-signed version:

```bash
# Self-sign (for development/distribution)
codesign -s - --deep --force dist/NexDex.app

# Or rebuild with signing enabled:
./build_mac.sh
```

## If You Still See the Warning

1. Go to **System Preferences** → **Security & Privacy**
2. Click **"Open Anyway"** next to NexDex
3. The warning won't appear again

---

**Questions?** Check the main [README.md](README.md) or open an issue on [GitHub Issues](https://github.com/Arths17/NexDex/issues).
