# Quick Start Guide

## Your Google Sheet is Configured!

Your Google Sheet ID has been set: `1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec`

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google Sheets API Credentials

1. Go to https://console.cloud.google.com/
2. Create a project or select existing
3. Enable **Google Sheets API** and **Google Drive API**
4. Create Service Account:
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Create the service account
   - Click on it → "Keys" tab → "Add Key" → "Create new key" → JSON
   - Download and save as `credentials.json` in project folder
5. **IMPORTANT**: Share your Google Sheet with the service account:
   - Open the JSON file and find `client_email` (looks like: `xxx@xxx.iam.gserviceaccount.com`)
   - Open your Google Sheet: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit
   - Click "Share" button
   - Paste the service account email
   - Give it "Editor" access
   - Click "Share"

### 3. Create .env File (Optional)

Create a `.env` file if you want to customize:
```env
SECRET_KEY=your-secret-key-here
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEET_ID=1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec
```

**Note**: The Sheet ID is already configured in `config.py`, so you can skip this if you're using the default credentials path.

### 4. Run the Application

```bash
python app.py
```

### 5. Access the Application

Open your browser: http://localhost:5000

### 6. First Time Setup

1. **Register** your first user (will automatically be admin)
2. **Login** with your credentials
3. Set up master data:
   - Go to **Locations** → Add locations
   - Go to **Categories** → Add categories
   - Go to **Subcategories** → Add subcategories
   - Go to **Asset Types** → Add asset types with depreciation values
   - Go to **Brands** → Add brands
4. Start adding assets!

## Troubleshooting

**"Could not initialize Google Sheets connection"**
- Make sure `credentials.json` is in the project folder
- Verify you shared the Google Sheet with the service account email
- Check that the service account has "Editor" access

**"Permission denied"**
- Double-check that the Google Sheet is shared with the service account email
- The email should end with `@xxx.iam.gserviceaccount.com`

## Your Google Sheet

The application will automatically create these sheets if they don't exist:
- Users
- Locations  
- Categories
- Subcategories
- AssetTypes
- Brands
- Assets
- AssetMovements

You can view your sheet here: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit


