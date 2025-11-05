# Adding credentials.json to Streamlit Secrets

## ⚠️ Important: Flask vs Streamlit

**Your current application is built with Flask, not Streamlit.**

- **Streamlit Cloud** only hosts Streamlit apps
- To use Streamlit Cloud, you need to convert your Flask app to Streamlit
- OR deploy your Flask app on Render/Railway (recommended)

## If You Want to Use Streamlit Cloud

You have two options:

### Option 1: Convert Flask App to Streamlit (Major Rewrite)
- This requires rewriting the entire application
- Estimated time: 2-4 weeks
- See conversion guide below

### Option 2: Deploy Flask App on Render/Railway (Recommended)
- Keep your Flask app as-is
- Deploy in minutes
- Free hosting available
- See `DEPLOYMENT_GUIDE.md`

---

## Streamlit Secrets Format

If you're converting to Streamlit, here's how to add credentials:

### Step 1: Go to Streamlit Cloud Secrets

1. Go to https://share.streamlit.io
2. Select your app
3. Click "Settings" → "Secrets"

### Step 2: Add credentials.json Content

Add this to your Streamlit secrets (in `.streamlit/secrets.toml` format):

```toml
# Google Sheets Credentials
[GOOGLE_SHEETS]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = """-----BEGIN PRIVATE KEY-----
your-private-key-here
-----END PRIVATE KEY-----"""
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

# Google Sheet ID
GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"

# Flask Secret Key (if needed)
SECRET_KEY = "your-secret-key-here"
```

### Step 3: Access in Streamlit Code

```python
import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials

# Access secrets
secrets = st.secrets["GOOGLE_SHEETS"]

# Convert to credentials format
creds_dict = {
    "type": secrets["type"],
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    "private_key": secrets["private_key"],
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"]
}

# Create credentials
credentials = Credentials.from_service_account_info(
    creds_dict,
    scopes=['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']
)

# Connect to Google Sheets
client = gspread.authorize(credentials)
sheet = client.open_by_key(st.secrets["GOOGLE_SHEET_ID"])
```

---

## Converting Flask App to Streamlit

If you want to convert your Flask app to Streamlit, here's what needs to change:

### Major Changes Required:

1. **Routes → Pages**
   - Flask routes → Streamlit pages (st.sidebar navigation)
   - Each page becomes a separate `.py` file

2. **Templates → Streamlit Components**
   - Jinja2 templates → Streamlit widgets (st.form, st.table, etc.)
   - HTML/CSS → Streamlit components

3. **Session Management**
   - Flask sessions → Streamlit session_state
   - Authentication system needs complete rewrite

4. **Forms**
   - Flask forms → Streamlit forms (st.form)
   - File uploads → st.file_uploader

5. **Tables**
   - HTML tables → st.dataframe or st.table

6. **Charts**
   - Already using Chart.js → Streamlit charts (st.bar_chart, st.line_chart, etc.)

### Estimated Conversion Time: 2-4 weeks

---

## Recommendation

**Deploy your Flask app on Render or Railway instead:**

✅ **Advantages:**
- No code changes needed
- Deploy in minutes
- Free hosting
- Keep all your features
- Works perfectly with your current code

❌ **Streamlit Conversion:**
- Major rewrite required
- Weeks of development
- Potential feature loss
- Learning new framework

---

## Need Help?

1. **Deploy Flask on Render/Railway** → See `DEPLOYMENT_GUIDE.md`
2. **Convert to Streamlit** → This is a major project, let me know if you want to proceed

