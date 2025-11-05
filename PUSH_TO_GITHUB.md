# Push to GitHub - Quick Guide

## ✅ Git Repository Ready!

Your repository has been initialized and committed. Now push to GitHub:

## Commands to Run (Copy & Paste)

```bash
# 1. Add GitHub remote (if not already added)
git remote add origin https://github.com/tonycharles1/Asset.git

# 2. Rename branch to main
git branch -M main

# 3. Push to GitHub
git push -u origin main
```

## If You Get Authentication Errors

If GitHub asks for authentication, you have two options:

### Option 1: Use Personal Access Token (Recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Use token as password when prompted

### Option 2: Use GitHub CLI
```bash
gh auth login
```

## After Pushing to GitHub

### Deploy to Render (Recommended)

1. **Go to https://render.com**
   - Sign up/login
   - Click "New +" → "Web Service"

2. **Connect GitHub**
   - Click "Connect GitHub"
   - Authorize Render
   - Select: `tonycharles1/Asset`

3. **Configure:**
   - **Name:** `asset-management-system`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. **Environment Variables:**
   - `SECRET_KEY` - Generate: `python -c "import secrets; print(secrets.token_hex(32))"`
   - `GOOGLE_SHEET_ID` - `1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec`
   - `GOOGLE_SHEETS_CREDENTIALS` - `credentials.json`
   - `FLASK_DEBUG` - `False`

5. **Upload credentials.json:**
   - In Render → Environment → Secret Files
   - Add Secret File: `credentials.json`
   - Paste your credentials.json content

6. **Deploy!**
   - Click "Create Web Service"
   - Wait 3-5 minutes
   - Your app will be live!

## Security Checklist ✅

- ✅ `credentials.json` is in `.gitignore`
- ✅ `.env` is in `.gitignore`
- ✅ `uploads/` folder is ignored
- ✅ No sensitive data in code

## Need Help?

See `GITHUB_SETUP.md` for detailed deployment instructions.

