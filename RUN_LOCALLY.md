# 🚀 How to Run the Project on Localhost

## Quick Start (Easiest Method)

### Option 1: Double-Click Batch File
1. Find `start_local.bat` in your project folder
2. **Double-click it**
3. Wait for Streamlit to start
4. Browser will open automatically at http://localhost:8501

---

## Option 2: Using PowerShell/Command Prompt

### Step 1: Open Terminal
1. **Right-click** in your project folder
2. Select **"Open in Terminal"** or **"Open PowerShell window here"**

**OR**

1. Open PowerShell/Command Prompt
2. Navigate to your project:
   ```powershell
   cd "C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System"
   ```

### Step 2: Run Streamlit
```powershell
streamlit run app_streamlit.py
```

### Step 3: Open Browser
- Streamlit will automatically open: **http://localhost:8501**
- Or manually go to: **http://localhost:8501**

---

## Option 3: Using Python Module

```powershell
python -m streamlit run app_streamlit.py
```

---

## What You'll See

When Streamlit starts successfully, you'll see:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

The browser should open automatically.

---

## First Time Setup (If Needed)

### 1. Install Dependencies
If you haven't installed dependencies yet:
```powershell
pip install -r requirements.txt
```

### 2. Verify Secrets File
Make sure `.streamlit/secrets.toml` exists with your credentials (already done ✅)

---

## Troubleshooting

### Problem: "streamlit: command not found"
**Solution:** Install Streamlit:
```powershell
pip install streamlit
```

### Problem: Port 8501 is already in use
**Solution:** Use a different port:
```powershell
streamlit run app_streamlit.py --server.port 8502
```
Then go to: http://localhost:8502

### Problem: "Module not found" errors
**Solution:** Install all dependencies:
```powershell
pip install -r requirements.txt
```

### Problem: Database connection error
**Solution:** 
- Check that `.streamlit/secrets.toml` exists
- Verify credentials are correct
- Make sure Google Sheet is shared with service account

### Problem: Browser doesn't open automatically
**Solution:** 
- Manually open browser
- Go to: http://localhost:8501
- Or check the terminal for the exact URL

---

## Login Credentials

After the app starts:
- **First time:** Register a new admin account
- **Or use default:** `admin` / `admin123` (if exists)

---

## Stopping the App

Press `Ctrl+C` in the terminal where Streamlit is running.

---

## Quick Reference

**Start app:**
```powershell
streamlit run app_streamlit.py
```

**Start on different port:**
```powershell
streamlit run app_streamlit.py --server.port 8502
```

**Check if dependencies installed:**
```powershell
pip list | Select-String streamlit
```

---

## Step-by-Step for First Time

1. ✅ Open PowerShell in project folder
2. ✅ Run: `pip install -r requirements.txt` (if not done)
3. ✅ Run: `streamlit run app_streamlit.py`
4. ✅ Wait for browser to open
5. ✅ Login/Register
6. ✅ Start using the app!

---

**That's it! Your app should now be running on localhost!** 🎉

