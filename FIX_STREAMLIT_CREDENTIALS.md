# Fix: Invalid JWT Signature Error in Streamlit

## The Problem

The error `'invalid_grant: Invalid JWT Signature.'` means your credentials are invalid or incorrectly formatted.

## Solution: Check Your Secrets Format

### Step 1: Verify Your credentials.json File

First, make sure your `credentials.json` file is valid:

```bash
python validate_credentials.py
```

If this shows errors, you need to download a new credentials file.

### Step 2: Check Secrets Format

The most common issue is incorrect formatting in `secrets.toml`. Here's what to check:

#### ❌ WRONG - Missing quotes or wrong format:
```toml
private_key = -----BEGIN PRIVATE KEY-----
MIIEvQ...
-----END PRIVATE KEY-----
```

#### ✅ CORRECT - Using triple quotes:
```toml
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQ...
-----END PRIVATE KEY-----"""
```

### Step 3: Common Mistakes

1. **Missing triple quotes** - Must use `"""` for multi-line strings
2. **Wrong private key format** - Must include BEGIN/END lines
3. **Extra quotes** - Don't add quotes around already-quoted values
4. **Line breaks** - Keep the private key as one continuous block

### Step 4: Regenerate Credentials (If Needed)

If your credentials.json is invalid:

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316
2. Click on: `asset-database@asset-database-477316.iam.gserviceaccount.com`
3. Go to "Keys" tab
4. Click "Add Key" → "Create new key" → Select "JSON"
5. Download the new file
6. Copy the values to your secrets.toml

### Step 5: Correct secrets.toml Format

Here's the EXACT format you need:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "your-actual-private-key-id-here"
private_key = """-----BEGIN PRIVATE KEY-----
YourActualPrivateKeyContentHere
MakeSureItIsAllOnOneBlock
NoExtraSpacesOrLineBreaks
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "your-actual-client-id-here"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-actual-cert-url-here"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

### Step 6: For Local Testing

If testing locally, you can also use the credentials.json file directly:

1. Make sure `credentials.json` is in your project root
2. The app will automatically use it as fallback if secrets aren't found

### Step 7: Verify Sheet Sharing

Make sure the Google Sheet is shared with:
- Email: `asset-database@asset-database-477316.iam.gserviceaccount.com`
- Permission: Editor

Sheet URL: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit

## Quick Fix Checklist

- [ ] Validate credentials.json file
- [ ] Check private_key uses triple quotes `"""`
- [ ] Verify private_key includes BEGIN/END lines
- [ ] Check all 4 values are filled in correctly
- [ ] Verify Google Sheet is shared with service account
- [ ] Test connection again

## Still Having Issues?

Run this to test:
```bash
python validate_credentials.py
```

If credentials.json is valid, the issue is in how secrets.toml is formatted.

