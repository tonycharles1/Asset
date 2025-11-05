# Fix: "Database not configured" Error

## Current Status
✅ Credentials file exists and has valid structure  
❌ Connection failing with "Invalid JWT Signature" error

## What This Means
The credentials file structure is correct, but the **private key is invalid**. This happens when:
- The key was rotated or revoked in Google Cloud Console
- The key expired
- The service account was disabled/recreated

## Solution: Generate a NEW Key

### Step 1: Delete Old Keys (Optional but Recommended)
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316
2. Click on: `asset-database@asset-database-477316.iam.gserviceaccount.com`
3. Go to "Keys" tab
4. Delete any old keys (you can keep them, but it's better to clean up)

### Step 2: Create New Key
1. In the same "Keys" tab, click **"Add Key"** → **"Create new key"**
2. Select **"JSON"** format
3. Click **"Create"**
4. The file will download automatically (usually to Downloads folder)

### Step 3: Replace credentials.json
1. **Find the downloaded file** (check your Downloads folder)
   - It will be named something like: `asset-database-477316-xxxxxxxxxxxx.json`
   
2. **Copy to project folder:**
   - Navigate to: `C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System`
   
3. **Rename the file:**
   - Right-click → Rename
   - Change it to exactly: `credentials.json`
   - **Important:** Make sure it's NOT `credentials.json.txt`
   - If Windows shows file extensions, ensure it ends with `.json` only

4. **Replace the old file:**
   - If `credentials.json` already exists, choose "Replace" when prompted

### Step 4: Verify Sheet Sharing
1. Open: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit
2. Click **"Share"** button (top right)
3. Add this email: `asset-database@asset-database-477316.iam.gserviceaccount.com`
4. Set permission to **"Editor"**
5. Click **"Share"**
6. Make sure it shows as "Editor" in the sharing list

### Step 5: Test Connection
Run this command:
```powershell
python validate_credentials.py
```
You should see: `[SUCCESS] Credentials file structure is valid!`

Then run:
```powershell
python test_connection.py
```
You should see: `[SUCCESS] Google Sheets connection established successfully!`

### Step 6: Restart Flask Server
If test passes, restart the server:
```powershell
python app.py
```

---

## Quick Checklist
- [ ] Downloaded NEW key from Google Cloud Console
- [ ] Renamed file to exactly `credentials.json` (not .txt)
- [ ] Replaced old credentials.json file
- [ ] Verified sheet is shared with service account email
- [ ] Service account has "Editor" permission
- [ ] Test connection shows [SUCCESS]
- [ ] Flask server restarted

---

## Still Having Issues?

If you still get errors after following these steps:

1. **Check the service account email matches:**
   - Run: `python validate_credentials.py`
   - Note the "Service Account Email" shown
   - Make sure this EXACT email is shared with the Google Sheet

2. **Verify Google Sheets API is enabled:**
   - Go to: https://console.cloud.google.com/apis/library?project=asset-database-477316
   - Search for "Google Sheets API"
   - Make sure it's enabled (should show "API enabled")

3. **Check service account is active:**
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316
   - Make sure the service account shows as "Active" (not disabled)

