# Quick Setup Guide

## Step-by-Step Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google Sheets API Credentials

1. Visit https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable these APIs:
   - Google Sheets API
   - Google Drive API
4. Create Service Account:
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Fill in details and create
   - Click on the created service account
   - Go to "Keys" tab → "Add Key" → "Create new key" → Choose JSON
   - Download the JSON file
   - Rename it to `credentials.json` and place in project root

### 3. Create/Configure Google Sheet

1. Create a new Google Sheet or open existing "Teddybuddies Asset Database"
2. Get the Sheet ID from URL:
   - URL: `https://docs.google.com/spreadsheets/d/XXXXX/edit`
   - `XXXXX` is your Sheet ID
3. Share the sheet with the service account email:
   - Find service account email in the JSON file (field: `client_email`)
   - Share the Google Sheet with this email
   - Give it "Editor" access

### 4. Configure Environment

Create a `.env` file in project root:
```env
SECRET_KEY=change-this-to-a-random-secret-key
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEET_ID=your-sheet-id-from-step-3
```

### 5. Run the Application

```bash
python app.py
```

Open browser: http://localhost:5000

### 6. First Time Setup

1. Register your first user (will automatically be admin)
2. Login with your credentials
3. Set up master data:
   - Locations
   - Categories
   - Subcategories
   - Asset Types
   - Brands
4. Start adding assets!

## Troubleshooting

**Error: "Could not initialize Google Sheets connection"**
- Check that `credentials.json` exists in project root
- Verify the file path in `.env` is correct
- Ensure the service account has access to the Google Sheet

**Error: "Permission denied"**
- Make sure you shared the Google Sheet with the service account email
- Verify the service account has "Editor" access

**Barcode not generating**
- Install: `pip install python-barcode[images]`
- Ensure Pillow is installed: `pip install Pillow`


