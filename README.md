# Fixed Asset Management System

A web-based Fixed Asset Management System built with Python Flask and Google Sheets as the database.

## Features

- User authentication with role-based access (Admin/User)
- Master data management (Location, Category, Subcategory, Type, Brand)
- Asset Entry with auto-generated Asset Code
- Edit and Delete functionality (Admin only for delete)
- Bulk barcode printing (PDF generation)
- Asset Movement tracking
- Responsive design for mobile and desktop

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Sheets API** and **Google Drive API**
4. Go to **Credentials** → **Create Credentials** → **Service Account**
5. Create a service account and download the JSON key file
6. Rename the downloaded file to `credentials.json` and place it in the project root
7. Note the service account email (e.g., `your-service-account@project-id.iam.gserviceaccount.com`)

### 3. Create/Configure Google Sheet

1. Create a new Google Sheet or use an existing one named "Teddybuddies Asset Database"
2. Share the Google Sheet with the service account email (from step 2) and give it **Editor** access
3. Copy the Google Sheet ID from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
   - The `SHEET_ID` is the long string between `/d/` and `/edit`

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here-change-in-production
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEET_ID=your-google-sheet-id-here
```

**Note:** Replace `your-google-sheet-id-here` with the actual Sheet ID from step 3.

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 6. Initial Setup

1. Open your browser and navigate to `http://localhost:5000`
2. Register a new user (the first user will automatically be set as admin)
3. Login with your credentials
4. Set up master data in this order:
   - **Locations** - Add all asset locations
   - **Categories** - Add asset categories
   - **Subcategories** - Add subcategories (linked to categories)
   - **Asset Types** - Add asset types with depreciation values
   - **Brands** - Add asset brands
5. Start adding assets using the **Assets** menu

## Google Sheet Structure

The application will automatically create the following sheets with proper headers:
- **Users** - User accounts and authentication
- **Locations** - Asset locations
- **Categories** - Asset categories
- **Subcategories** - Asset subcategories (linked to categories)
- **AssetTypes** - Asset types with depreciation values
- **Brands** - Asset brands
- **Assets** - Main asset records
- **AssetMovements** - Asset movement history

## Features Guide

### Asset Management
- **Add Asset**: Create new assets with auto-generated Asset Code
- **Edit Asset**: Modify asset details (any user)
- **Delete Asset**: Remove assets (Admin only)
- **Barcode Printing**: Select multiple assets and generate PDF with barcodes

### Asset Movement
- Track when assets move from one location to another
- Automatically updates asset location when movement is recorded
- Maintains complete movement history

### User Roles
- **Admin**: Full access including delete functionality
- **User**: Can add, edit, and view assets but cannot delete

## Troubleshooting

1. **Google Sheets Connection Error**: 
   - Verify `credentials.json` is in the project root
   - Ensure the service account has access to the Google Sheet
   - Check that Google Sheets API is enabled

2. **Barcode Generation Issues**:
   - Ensure `python-barcode` and `Pillow` are installed
   - Check that asset codes are valid for barcode generation

3. **Port Already in Use**:
   - Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

## Mobile Responsiveness

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

All features are accessible from any device size.

