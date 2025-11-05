# Quick Fix: Invalid JWT Signature Error

## The Problem
The credentials file exists but is still giving "Invalid JWT Signature" error. This means you need to download a **FRESH** credentials file from Google Cloud Console.

## Solution (5 Steps)

### Step 1: Download New Credentials
1. Open: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316
2. Click on: `asset-database@asset-database-477316.iam.gserviceaccount.com`
3. Go to "Keys" tab
4. Click "Add Key" → "Create new key" → Select "JSON"
5. Click "Create" - file downloads automatically

### Step 2: Replace credentials.json
1. Find the downloaded file (check Downloads folder)
2. Copy it to: `C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System`
3. **Rename it to:** `credentials.json`
4. **Overwrite** the existing file when prompted

### Step 3: Share Google Sheet
1. Open: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit
2. Click "Share" button
3. Add: `asset-database@asset-database-477316.iam.gserviceaccount.com`
4. Set to "Editor"
5. Click "Share"

### Step 4: Test Connection
Run this command:
```powershell
python test_connection.py
```

If you see `[SUCCESS]`, you're good!

### Step 5: Restart Flask
```powershell
python app.py
```

---

**Note:** Make sure the file is named exactly `credentials.json` (not `.txt` or anything else)


