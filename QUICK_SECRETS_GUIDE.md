# Quick Secrets Guide - Copy & Paste

## 📋 Simple Instructions

### 1. Open Your credentials.json File
You should have this file in your project folder.

### 2. Copy This Template

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "PASTE_YOUR_PRIVATE_KEY_ID_HERE"
private_key = """-----BEGIN PRIVATE KEY-----
PASTE_YOUR_ENTIRE_PRIVATE_KEY_HERE
(keep the BEGIN and END lines)
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "PASTE_YOUR_CLIENT_ID_HERE"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "PASTE_YOUR_CLIENT_X509_CERT_URL_HERE"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

### 3. Fill in 4 Values from credentials.json

From your credentials.json, find and copy these 4 values:

1. **private_key_id** → Copy the value (looks like: `"a1b2c3d4e5f6..."`)
2. **private_key** → Copy the ENTIRE key including:
   ```
   -----BEGIN PRIVATE KEY-----
   (the long key content)
   -----END PRIVATE KEY-----
   ```
3. **client_id** → Copy the value (looks like: `"123456789012..."`)
4. **client_x509_cert_url** → Copy the value (looks like: `"https://www.googleapis.com/robot/v1/metadata/x509/..."`)

### 4. Replace the Placeholders

In the template above, replace:
- `PASTE_YOUR_PRIVATE_KEY_ID_HERE` → with your private_key_id
- `PASTE_YOUR_ENTIRE_PRIVATE_KEY_HERE` → with your private_key (keep BEGIN/END lines)
- `PASTE_YOUR_CLIENT_ID_HERE` → with your client_id
- `PASTE_YOUR_CLIENT_X509_CERT_URL_HERE` → with your client_x509_cert_url

### 5. Save to Secrets

**For Local Testing:**
- Save as: `.streamlit/secrets.toml`

**For Streamlit Cloud:**
- Go to: https://share.streamlit.io
- Your App → Settings → Secrets
- Paste the entire content

### ✅ Done!

That's it! The other values (type, project_id, email, etc.) are already filled in for you.

---

## Example credentials.json Structure

Your credentials.json looks like:
```json
{
  "type": "service_account",
  "project_id": "asset-database-477316",
  "private_key_id": "← COPY THIS",
  "private_key": "-----BEGIN PRIVATE KEY-----\n← COPY THIS ENTIRE KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "asset-database@asset-database-477316.iam.gserviceaccount.com",
  "client_id": "← COPY THIS",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "← COPY THIS"
}
```

Just copy the 4 values marked with arrows!

