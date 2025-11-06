# 🚀 Quick Start - Run on Localhost

## Easiest Method: Double-Click Batch File

1. **Double-click:** `start_local.bat`
2. **Wait 5-10 seconds** for Streamlit to start
3. **Browser opens automatically** at http://localhost:8501

---

## Manual Method: PowerShell/Command Prompt

1. **Open PowerShell** in project folder (right-click → "Open in Terminal")

2. **Run this command:**
   ```powershell
   python -m streamlit run app_streamlit.py
   ```

3. **Wait for output:**
   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   ```

4. **Browser opens automatically** OR manually go to: http://localhost:8501

---

## Important: Use `python -m streamlit`

**NOT:** `streamlit run app_streamlit.py` ❌  
**USE:** `python -m streamlit run app_streamlit.py` ✅

---

## If Browser Doesn't Open Automatically

1. Wait 10 seconds for Streamlit to fully start
2. Manually open browser
3. Go to: **http://localhost:8501**

---

## First Time Setup

If dependencies aren't installed:
```powershell
pip install -r requirements.txt
```

---

## Troubleshooting

### "streamlit: command not found"
**Solution:** Use `python -m streamlit` instead

### "Port already in use"
**Solution:** Use different port:
```powershell
python -m streamlit run app_streamlit.py --server.port 8502
```

### "Module not found"
**Solution:** Install dependencies:
```powershell
pip install -r requirements.txt
```

---

## Login

- **First time:** Register a new admin account
- **Or use:** `admin` / `admin123` (if exists)

---

**That's it! Your app should be running on http://localhost:8501** 🎉

