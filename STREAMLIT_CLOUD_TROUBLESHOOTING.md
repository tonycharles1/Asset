# Streamlit Cloud Installation Error - Troubleshooting

## Step 1: Get the Exact Error Message

**This is the most important step!**

1. Go to: https://share.streamlit.io
2. Sign in and find your app
3. Click on your app → **"Manage app"**
4. Click **"Logs"** tab
5. Scroll down to find the **installation error**
6. Look for lines that say:
   - `ERROR: Could not install packages`
   - `ERROR: Failed building wheel`
   - `ERROR: pip install failed`
   - Or any package name with an error

**Copy the exact error message** and share it.

## Step 2: Common Errors and Fixes

### Error: "Failed building wheel for Pillow"
**Fix:** Pillow needs system libraries. Try:
```txt
Pillow==10.3.0
```

### Error: "Could not find a version that satisfies the requirement"
**Fix:** The version might not exist. Check the package version on PyPI.

### Error: "ERROR: pip's dependency resolver"
**Fix:** There's a conflict between packages. We may need to adjust versions.

### Error: "No module named 'X'"
**Fix:** Missing dependency. Add it to requirements.txt.

## Step 3: Test Locally First

Before deploying, test locally:

```powershell
# Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

If installation fails locally, note the error and we can fix it.

## Step 4: Minimal Test

If full installation fails, try a minimal requirements.txt:

```txt
streamlit==1.28.0
gspread==5.12.0
google-auth==2.23.4
pandas==2.0.3
```

Then add packages one by one until you find the problematic one.

## Step 5: Check Python Version

Make sure `runtime.txt` contains:
```
3.11
```

Not:
```
python-3.11.0
```

## Current Status

✅ Updated requirements.txt with conservative versions
✅ Fixed runtime.txt format
✅ Removed python-barcode (optional dependency)

## What to Do Next

1. **Check Streamlit Cloud logs** for the specific error
2. **Share the error message** with me
3. **Or test locally** with `pip install -r requirements.txt` and share the error

The error message will tell us exactly which package is failing and why!

