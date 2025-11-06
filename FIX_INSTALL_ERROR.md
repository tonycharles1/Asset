# Fix Installation Error on Streamlit Cloud

## Common Issues and Solutions

### Issue: "installer returned a non-zero exit code"

This usually means one of the packages in `requirements.txt` failed to install.

## Solution 1: Check Streamlit Cloud Logs

1. Go to Streamlit Cloud → Your App
2. Click "Manage app" → "Logs"
3. Look for the specific error message
4. It will tell you which package failed

## Solution 2: Test Installation Locally

Run this to see if requirements install correctly:
```powershell
pip install -r requirements.txt
```

If you see errors, note which package failed.

## Solution 3: Known Problematic Packages

### Pillow Issues
- Problem: Pillow sometimes requires system libraries
- Fix: Try `Pillow==10.4.0` or `Pillow==10.3.0`

### reportlab Issues  
- Problem: reportlab might need system fonts
- Fix: Usually works, but if it fails, we can make it optional

### pandas Version Conflicts
- Problem: pandas 2.0+ might conflict with other packages
- Fix: Try `pandas==1.5.3` if 2.0 fails

## Solution 4: Minimal Requirements Test

If the full requirements fail, try installing one at a time:

1. Start with just Streamlit:
```
streamlit==1.28.0
```

2. Add dependencies one by one and test

## Solution 5: Check Python Version

Make sure `runtime.txt` is correct:
- Streamlit Cloud supports: 3.8, 3.9, 3.10, 3.11
- Current setting: `3.11`

## Solution 6: Alternative - Use Requirements with Specific Versions

If flexible versions (`>=`) fail, use exact versions (`==`).

## Current Requirements

The current `requirements.txt` uses exact versions that are known to work together. If you're still getting errors:

1. **Check the logs** for the specific package that's failing
2. **Share the error message** so we can fix the specific package
3. **Try removing optional packages** (like reportlab) temporarily to test

## Quick Fix Command

If you need to test locally:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Look for any error messages and share them.

