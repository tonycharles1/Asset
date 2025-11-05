# Deployment Guide for Asset Management System

## Important Note: Streamlit vs Flask

⚠️ **This is a Flask application, not a Streamlit application.**

- **Streamlit Cloud** only hosts Streamlit apps (not Flask apps)
- To use Streamlit Cloud, you would need to completely rewrite the application
- For Flask apps, use platforms like Render, Railway, Heroku, etc.

## Recommended Hosting Platforms for Flask

### Option 1: Render (Recommended - Free Tier Available)

**Pros:**
- Free tier available
- Easy deployment from GitHub
- Automatic SSL certificates
- Good for small to medium applications

**Steps:**
1. Push your code to GitHub
2. Go to https://render.com and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment Variables:**
     - `SECRET_KEY` - Generate a secure key
     - `GOOGLE_SHEETS_CREDENTIALS` - Upload credentials.json content or use environment variable
     - `GOOGLE_SHEET_ID` - Your Google Sheet ID

6. Upload `credentials.json` securely or use environment variables

### Option 2: Railway

**Pros:**
- Very easy setup
- Free credits monthly
- Auto-deploy from GitHub

**Steps:**
1. Push code to GitHub
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub repo"
4. Add environment variables in Railway dashboard
5. Railway auto-detects Flask and deploys

### Option 3: PythonAnywhere

**Pros:**
- Free tier available
- Good for beginners
- Easy file upload

**Steps:**
1. Sign up at https://www.pythonanywhere.com
2. Upload your files via web interface
3. Configure web app in "Web" tab
4. Set environment variables in "Files" tab

### Option 4: Heroku

**Pros:**
- Well-established platform
- Good documentation

**Steps:**
1. Install Heroku CLI
2. Create `Procfile` (see below)
3. Deploy: `git push heroku main`

## Required Files for Deployment

### 1. Procfile (for Heroku/Railway)
```
web: gunicorn app:app
```

### 2. runtime.txt (optional, for Heroku)
```
python-3.11.0
```

### 3. .env File (DO NOT commit to Git!)

Add to `.gitignore`:
```
.env
credentials.json
```

### 4. Environment Variables Needed

```bash
SECRET_KEY=your-secret-key-here
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEET_ID=your-sheet-id
```

## Important Security Considerations

1. **Never commit `credentials.json` to Git**
   - Use environment variables or secure file storage
   - Render/Railway allow secure file uploads

2. **Generate a strong SECRET_KEY**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

3. **Update Google Sheets API settings**
   - Ensure service account has access
   - Check API quotas

## Updating app.py for Production

You may need to update the app.py to handle production environment:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

## Deployment Checklist

- [ ] Push code to GitHub (excluding credentials.json)
- [ ] Create account on hosting platform
- [ ] Set environment variables
- [ ] Upload credentials.json securely
- [ ] Configure build/start commands
- [ ] Test deployment
- [ ] Verify Google Sheets connection
- [ ] Test all features

## Alternative: Converting to Streamlit (Not Recommended)

If you really want to use Streamlit Cloud, you would need to:
1. Rewrite the entire application in Streamlit
2. Use Streamlit's components instead of Flask routes
3. Redesign forms and UI
4. This is a massive undertaking (weeks of work)

**Better option:** Use Render or Railway for Flask deployment.

## Support

If you need help with deployment, please specify which platform you'd like to use, and I can provide detailed platform-specific instructions.

