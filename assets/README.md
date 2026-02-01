# 🎨 NexDex Assets

Icons and branding assets for NexDex standalone applications.

## Icon Files

### macOS (`nexdex_icon.icns`)
- Format: `.icns` (Apple Icon format)
- Size: 256x256 pixels minimum
- Used for app icon in macOS app bundle

### Windows (`nexdex_icon.ico`)
- Format: `.ico` (Windows Icon format)
- Size: 256x256 pixels minimum
- Used for executable icon in Windows .exe

### Linux (`nexdex_icon.png`)
- Format: `.png`
- Size: 256x256 pixels minimum
- Used for app icon in Linux file managers

## How to Generate Icons

### From PNG to macOS `.icns`

Using ImageMagick:
```bash
convert nexdex.png -define icon:auto-resize=256,128,96,64,48,32,16 nexdex.icns
```

Or use online tools:
- https://icoconvert.com/
- https://cloudconvert.com/

### From PNG to Windows `.ico`

Using ImageMagick:
```bash
convert nexdex.png -compress none nexdex.ico
```

Or use online tools:
- https://icoconvert.com/
- https://favicon-generator.org/

### PNG for Linux

Simply save a 256x256 PNG file:
```bash
# Create from any image
convert input.png -resize 256x256 nexdex_icon.png
```

## Source Design

Here's a simple SVG design for NexDex that you can export to PNG:

```html
<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <!-- Purple gradient background -->
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="256" height="256" fill="url(#grad)" rx="50"/>
  
  <!-- Network nodes -->
  <circle cx="80" cy="80" r="20" fill="white" opacity="0.9"/>
  <circle cx="176" cy="80" r="20" fill="white" opacity="0.7"/>
  <circle cx="128" cy="140" r="20" fill="white" opacity="0.9"/>
  <circle cx="80" cy="200" r="20" fill="white" opacity="0.7"/>
  <circle cx="176" cy="200" r="20" fill="white" opacity="0.7"/>
  
  <!-- Connection lines -->
  <line x1="80" y1="80" x2="128" y2="140" stroke="white" stroke-width="3" opacity="0.6"/>
  <line x1="176" y1="80" x2="128" y2="140" stroke="white" stroke-width="3" opacity="0.6"/>
  <line x1="128" y1="140" x2="80" y2="200" stroke="white" stroke-width="3" opacity="0.6"/>
  <line x1="128" y1="140" x2="176" y2="200" stroke="white" stroke-width="3" opacity="0.6"/>
  
  <!-- Center text/logo -->
  <text x="128" y="245" font-size="14" font-weight="bold" fill="white" 
        text-anchor="middle" font-family="Arial">NexDex</text>
</svg>
```

Steps to convert SVG to icons:
1. Save as `nexdex.svg`
2. Export to PNG (256x256) in your design tool
3. Convert to `.icns` and `.ico` using ImageMagick

## Placeholder Generation

If you don't have icons yet, PyInstaller will use system defaults. The build scripts create placeholder files automatically:

```bash
touch assets/nexdex_icon.icns
touch assets/nexdex_icon.ico
touch assets/nexdex_icon.png
```

Replace these with proper icon files when ready.

## Icon Guidelines

### Design Principles
- **Simple** - Recognizable at small sizes (16x16)
- **Distinctive** - Unique from other app icons
- **Professional** - Appropriate for business context
- **Transparent** - PNG and ICO should have transparent backgrounds
- **Consistent** - Same design across platforms

### Color Scheme
Recommended colors (matching NexDex branding):
- Primary: #667eea (blue-purple)
- Secondary: #764ba2 (purple)
- Accent: #ff6b6b (red for alerts)
- Background: Transparent

### Size Guidelines
- Save at multiple sizes:
  - 512x512 (largest)
  - 256x256 (standard)
  - 128x128 (medium)
  - 64x64 (small)
  - 32x32 (icon)
  - 16x16 (favicon)

## Using Custom Icons in Builds

1. Generate icon files in required formats
2. Place in `assets/` folder:
   - `nexdex_icon.icns` (macOS)
   - `nexdex_icon.ico` (Windows)
   - `nexdex_icon.png` (Linux)
3. Rebuild using respective build script
4. Icons automatically included in output

## Branding Assets (Optional)

You can also add:
- `logo.png` - Horizontal logo for website
- `logo-square.png` - Square logo for social media
- `banner.png` - Website banner/hero image
- `screenshot.png` - App screenshot for website

These are not required for the app to function, but helpful for marketing.

## More Resources

- **Flaticon** - Free icons: https://www.flaticon.com
- **Noun Project** - Icon library: https://thenounproject.com
- **Figma** - Design tool: https://www.figma.com
- **Canva** - Icon maker: https://www.canva.com

---

**Next Steps:**
1. Generate proper icon files
2. Place in `assets/` folder
3. Rebuild NexDex app with `build_mac.sh`, `build_windows.bat`, or `build_linux.sh`
4. Your icons will appear in the app!
