# Verify Your Credentials File

## Current Issue
The error "Invalid JWT Signature" means the credentials file is either:
1. Not properly downloaded/updated
2. Corrupted during copy
3. From a revoked/disabled service account

## Steps to Fix

### 1. Download Fresh Credentials from Google Cloud Console

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316

2. Click on the service account: `asset-database@asset-database-477316.iam.gserviceaccount.com`

3. Go to the "Keys" tab

4. Click "Add Key" → "Create new key"

5. Select "JSON" format

6. Click "Create" - this will download a JSON file

### 2. Replace credentials.json

1. **Find the downloaded file** (usually in your Downloads folder)
   - It will have a name like: `asset-database-477316-xxxxx.json`

2. **Copy it to your project folder:**
   - Navigate to: `C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System`

3. **Rename it to exactly:** `credentials.json`
   - Make sure it's NOT `credentials.json.txt` or anything else
   - It must be exactly `credentials.json`

4. **Replace the old file** - overwrite the existing `credentials.json`

### 3. Verify the File

Run this command to verify:
```powershell
python test_connection.py
```

You should see: `[SUCCESS] Google Sheets connection established successfully!`

### 4. Share the Google Sheet

1. Open: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit

2. Click "Share" (top right)

3. Add this email: `asset-database@asset-database-477316.iam.gserviceaccount.com`

4. Set permission to "Editor"

5. Click "Share"

### 5. Restart the Flask App

After updating credentials and sharing the sheet, restart the app.

---

## Important Notes

- The credentials file MUST be named exactly `credentials.json` (not .txt or anything else)
- Make sure you're downloading a NEW key from Google Cloud Console
- The file should be about 2-3 KB in size
- If you see "Invalid JWT Signature" after updating, the file might be corrupted - download it again


