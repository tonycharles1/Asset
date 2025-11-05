# How to Add Secrets to Streamlit

## Step-by-Step Guide: Converting credentials.json to Streamlit Secrets

### Step 1: Open Your credentials.json File

Open your `credentials.json` file (it should be in your project folder).

### Step 2: Copy the Values

You'll see a JSON file that looks like this:
```json
{
  "type": "service_account",
  "project_id": "asset-database-477316",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "asset-database@asset-database-477316.iam.gserviceaccount.com",
  "client_id": "123456789...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

### Step 3: Create .streamlit/secrets.toml File

**For Local Development:**
1. Create folder: `.streamlit` (if it doesn't exist)
2. Create file: `.streamlit/secrets.toml`
3. Copy the format below

**For Streamlit Cloud:**
1. Go to your app on Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Paste the content below

### Step 4: Fill in the TOML Format

Replace `YOUR_VALUE_HERE` with actual values from your credentials.json:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "YOUR_PRIVATE_KEY_ID_FROM_CREDENTIALS_JSON"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_FROM_CREDENTIALS_JSON
(keep the entire key including BEGIN and END lines)
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "YOUR_CLIENT_ID_FROM_CREDENTIALS_JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CLIENT_X509_CERT_URL_FROM_CREDENTIALS_JSON"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

### Step 5: Mapping credentials.json to secrets.toml

| credentials.json Field | secrets.toml Field | Example |
|------------------------|-------------------|---------|
| `"type"` | `type` | `"service_account"` |
| `"project_id"` | `project_id` | `"asset-database-477316"` |
| `"private_key_id"` | `private_key_id` | `"abc123def456..."` |
| `"private_key"` | `private_key` | Keep the entire key with BEGIN/END lines |
| `"client_email"` | `client_email` | `"asset-database@..."` |
| `"client_id"` | `client_id` | `"123456789..."` |
| `"auth_uri"` | `auth_uri` | `"https://accounts.google.com/o/oauth2/auth"` |
| `"token_uri"` | `token_uri` | `"https://oauth2.googleapis.com/token"` |
| `"auth_provider_x509_cert_url"` | `auth_provider_x509_cert_url` | `"https://www.googleapis.com/oauth2/v1/certs"` |
| `"client_x509_cert_url"` | `client_x509_cert_url` | `"https://www.googleapis.com/robot/v1/metadata/x509/..."` |

### Step 6: Important Notes

1. **private_key**: 
   - Keep the `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----` lines
   - Use triple quotes `"""` to allow multi-line strings
   - Keep the entire key exactly as it appears

2. **Quotes**: 
   - Use double quotes `"` for string values
   - TOML format, not JSON

3. **Section**: 
   - `[GOOGLE_SHEETS]` is a section header in TOML
   - All credentials go under this section

4. **GOOGLE_SHEET_ID**: 
   - This is outside the section (top-level)
   - Already set to your sheet ID

### Example (Filled Out)

Here's what a filled-out secrets.toml looks like:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
(entire private key content here)
...
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "123456789012345678901"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/asset-database%40asset-database-477316.iam.gserviceaccount.com"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

### Quick Copy Template

Copy this template and fill in your values:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "PASTE_FROM_CREDENTIALS_JSON"
private_key = """-----BEGIN PRIVATE KEY-----
PASTE_ENTIRE_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "PASTE_FROM_CREDENTIALS_JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "PASTE_FROM_CREDENTIALS_JSON"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

### Where to Add Secrets

**Local Development:**
- File: `.streamlit/secrets.toml`
- Location: `C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System\.streamlit\secrets.toml`

**Streamlit Cloud:**
- Go to: https://share.streamlit.io
- Select your app → Settings → Secrets
- Paste the entire TOML content

### Verification

After adding secrets, test locally:
```bash
streamlit run app_streamlit.py
```

If you see "Database connection failed", check:
1. All values are filled in
2. private_key has BEGIN/END lines
3. No extra quotes or brackets
4. TOML format is correct

---

## Still Need Help?

If you have your credentials.json open, I can help you convert specific values. Just let me know which field you're stuck on!

