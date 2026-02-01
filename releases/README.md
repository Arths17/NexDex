# NexDex Free Release Package

This directory contains the free downloadable version of NexDex.

## Creating the Release Package

Run this command from the project root to create the free download:

```bash
zip -r releases/NexDex-free.zip \
  nexdex.py \
  requirements.txt \
  README.md \
  config/ \
  scenarios/ \
  src/ \
  -x "*.pyc" "__pycache__/*" "*.git*" "website/*" "reports/*" "*.DS_Store"
```

This will create a clean package with:
- ✅ Main CLI tool (nexdex.py)
- ✅ Dependencies (requirements.txt)
- ✅ Documentation (README.md)
- ✅ Configuration examples (config/)
- ✅ Scenario examples (scenarios/)
- ✅ Source code (src/)

Excluded from package:
- ❌ Website files
- ❌ Generated reports
- ❌ Git history
- ❌ Python cache files

## Version Tracking

Update this file with each release:

### v1.0.0 (Current)
- Initial public release
- CLI + Interactive mode
- ASCII & HTML reports
- Scenario tagging
- Dependency mapping
- Business impact scoring

---

Place `NexDex-free.zip` in this directory for the website download link to work.
