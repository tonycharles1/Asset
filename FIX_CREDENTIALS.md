# Fix "Invalid JWT Signature" Error

## Problem
The error "Invalid JWT Signature" means the service account credentials are invalid or have been revoked.

## Solution: Regenerate Service Account Key

### Option 1: Download New Credentials (Recommended)

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Select project: `asset-database-477316`

2. **Navigate to Service Accounts:**
   - Go to: IAM & Admin → Service Accounts
   - Or direct link: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316

3. **Find the Service Account:**
   - Look for: `asset-database@asset-database-477316.iam.gserviceaccount.com`
   - Click on it

4. **Create New Key:**
   - Click the "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON" format
   - Click "Create"

5. **Replace credentials.json:**
   - The JSON file will download automatically
   - Replace your current `credentials.json` with the downloaded file
   - Make sure it's named exactly `credentials.json`

6. **Restart the Flask application**

### Option 2: Check System Clock

The JWT signature is time-sensitive. Make sure your system clock is correct:

1. Check Windows time settings
2. Ensure timezone is correct
3. Sync with internet time if needed

### Option 3: Verify Service Account Still Exists

1. Go to Google Cloud Console
2. Check if the service account still exists
3. If it was deleted, you'll need to create a new one

## After Fixing Credentials

1. **Share the Google Sheet:**
   - Open: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit
   - Click "Share"
   - Add: `asset-database@asset-database-477316.iam.gserviceaccount.com`
   - Set permission to "Editor"
   - Click "Share"

2. **Restart Flask app:**
   ```bash
   python app.py
   ```

3. **Check for success message:**
   - You should see: `[SUCCESS] Google Sheets connection established successfully`


