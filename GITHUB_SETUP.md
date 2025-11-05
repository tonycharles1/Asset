# GitHub Setup & Deployment Guide

## ⚠️ Security Checklist Before Pushing

Before pushing to GitHub, make sure:

- [ ] `credentials.json` is in `.gitignore` ✅
- [ ] `.env` file is in `.gitignore` ✅
- [ ] No sensitive data in code
- [ ] `uploads/` folder is ignored ✅

## Step-by-Step GitHub Setup

### 1. Initialize Git (if not done)
```bash
git init
```

### 2. Add All Files
```bash
git add .
```

### 3. Make Initial Commit
```bash
git commit -m "Initial commit: Asset Management System"
```

### 4. Add GitHub Remote
```bash
git remote add origin https://github.com/tonycharles1/Asset.git
```

### 5. Rename Branch to Main
```bash
git branch -M main
```

### 6. Push to GitHub
```bash
git push -u origin main
```

## After Pushing to GitHub

### Deploy to Render (Recommended)

1. **Go to https://render.com**
   - Sign up or log in
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Click "Connect GitHub"
   - Authorize Render
   - Select repository: `tonycharles1/Asset`

3. **Configure Service**
   - **Name:** `asset-management-system` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   
   - **Name:** `SECRET_KEY`
     **Value:** Generate with:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```
   
   - **Name:** `GOOGLE_SHEET_ID`
     **Value:** `1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec`
   
   - **Name:** `GOOGLE_SHEETS_CREDENTIALS`
     **Value:** `credentials.json`
   
   - **Name:** `FLASK_DEBUG`
     **Value:** `False`

5. **Upload credentials.json**
   - In Render dashboard, go to "Environment" tab
   - Scroll to "Secret Files"
   - Click "Add Secret File"
   - **Name:** `credentials.json`
   - **Contents:** Paste your entire credentials.json file content
   - OR use environment variable (see below)

6. **Alternative: Use Environment Variable for Credentials**
   Instead of uploading file, you can:
   - **Name:** `GOOGLE_SHEETS_CREDENTIALS_JSON`
   - **Value:** Paste entire JSON content from credentials.json
   - Then update `config.py` to read from this variable

7. **Deploy!**
   - Click "Create Web Service"
   - Wait for build (3-5 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

## Deploy to Railway (Alternative)

1. **Go to https://railway.app**
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `tonycharles1/Asset`

2. **Railway auto-detects Flask**
   - It will automatically detect and configure
   - Add environment variables in "Variables" tab
   - Upload credentials.json in "Files" tab

3. **Deploy**
   - Railway automatically deploys on push
   - Your app will be live immediately

## Environment Variables Summary

You'll need these on your hosting platform:

```
SECRET_KEY=<generate-with-secrets-token-hex>
GOOGLE_SHEET_ID=1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec
GOOGLE_SHEETS_CREDENTIALS=credentials.json
FLASK_DEBUG=False
PORT=5000 (auto-set by platform)
```

## Troubleshooting

### If credentials.json is missing on deployment:
- Upload it as a "Secret File" in Render
- Or convert to environment variable
- Make sure service account has access to Google Sheet

### If app crashes on startup:
- Check logs in Render/Railway dashboard
- Verify all environment variables are set
- Check Google Sheets API is enabled

### If database connection fails:
- Verify credentials.json is correct
- Check service account email has access to sheet
- Ensure Google Sheets API is enabled in Google Cloud Console

## Next Steps After Deployment

1. ✅ Test all features on live site
2. ✅ Verify Google Sheets connection works
3. ✅ Test user registration/login
4. ✅ Test asset CRUD operations
5. ✅ Test reports and exports
6. ✅ Set up custom domain (optional)

## Support

If you encounter issues:
1. Check Render/Railway logs
2. Verify environment variables
3. Test credentials.json locally first
4. Check Google Sheets API quotas

Good luck with your deployment! 🚀

