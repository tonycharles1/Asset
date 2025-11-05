# Running Your Streamlit App

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Secrets (for local testing)

Create a `.streamlit/secrets.toml` file:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CERT_URL"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

**OR** use `credentials.json` file (fallback option)

### 3. Run the App
```bash
streamlit run app_streamlit.py
```

The app will open in your browser at http://localhost:8501

## Deploy to Streamlit Cloud

### 1. Push to GitHub
Make sure your code is pushed to GitHub (already done)

### 2. Go to Streamlit Cloud
1. Visit https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"

### 3. Configure App
- **Repository:** Select `tonycharles1/Asset`
- **Branch:** `main`
- **Main file path:** `app_streamlit.py`
- **App URL:** (optional custom subdomain)

### 4. Add Secrets
Click "Advanced settings" → "Secrets"

Paste your credentials in TOML format (see `streamlit_secrets_example.toml`)

### 5. Deploy!
Click "Deploy" and wait for the app to build and deploy.

## Default Login

After first deployment, you'll need to register a user or use the default admin:
- **Username:** admin
- **Password:** admin123

(If no users exist, the system may create a default admin)

## Troubleshooting

### Database Connection Error
- Check that secrets are correctly formatted
- Verify service account has access to Google Sheet
- Check Google Sheets API is enabled

### Import Errors
- Make sure all dependencies are in `requirements.txt`
- Check that all page files exist in `pages/` directory

### Authentication Issues
- Make sure Users sheet has at least one user
- Default admin credentials: admin/admin123

## Features Converted

✅ All pages converted to Streamlit
✅ Dashboard with charts
✅ Asset management (add, edit, delete)
✅ Master data management
✅ Reports and exports
✅ Depreciation calculations
✅ Activity logs
✅ Asset movements

## Next Steps

1. Test locally first
2. Fix any issues
3. Deploy to Streamlit Cloud
4. Configure secrets
5. Test on live app

