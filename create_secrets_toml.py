"""
Helper script to convert credentials.json to secrets.toml format
Run this to automatically create your .streamlit/secrets.toml file
"""

import json
import os
from pathlib import Path

def create_secrets_toml():
    """Create secrets.toml from credentials.json"""
    
    # Read credentials.json
    creds_file = 'credentials.json'
    if not os.path.exists(creds_file):
        print(f"[ERROR] Error: {creds_file} not found!")
        print("Please make sure credentials.json is in the project root directory.")
        return False
    
    try:
        with open(creds_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except Exception as e:
        print(f"[ERROR] Error reading credentials.json: {e}")
        return False
    
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path('.streamlit')
    streamlit_dir.mkdir(exist_ok=True)
    
    # Create secrets.toml content
    secrets_content = f"""[GOOGLE_SHEETS]
type = "{creds.get('type', 'service_account')}"
project_id = "{creds.get('project_id', '')}"
private_key_id = "{creds.get('private_key_id', '')}"
private_key = \"\"\"{creds.get('private_key', '')}\"\"\"
client_email = "{creds.get('client_email', '')}"
client_id = "{creds.get('client_id', '')}"
auth_uri = "{creds.get('auth_uri', 'https://accounts.google.com/o/oauth2/auth')}"
token_uri = "{creds.get('token_uri', 'https://oauth2.googleapis.com/token')}"
auth_provider_x509_cert_url = "{creds.get('auth_provider_x509_cert_url', 'https://www.googleapis.com/oauth2/v1/certs')}"
client_x509_cert_url = "{creds.get('client_x509_cert_url', '')}"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
"""
    
    # Write to .streamlit/secrets.toml
    secrets_file = streamlit_dir / 'secrets.toml'
    try:
        with open(secrets_file, 'w', encoding='utf-8') as f:
            f.write(secrets_content)
        
        print("[SUCCESS] Successfully created .streamlit/secrets.toml")
        print(f"[INFO] File location: {secrets_file.absolute()}")
        print("\n[SUCCESS] Your secrets.toml file is ready!")
        print("\nYou can now:")
        print("  1. Test locally: streamlit run app_streamlit.py")
        print("  2. Copy this content to Streamlit Cloud -> Settings -> Secrets")
        print("\n[WARNING] Note: Keep this file secure and never commit it to Git!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error writing secrets.toml: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Creating secrets.toml from credentials.json")
    print("=" * 60)
    print()
    
    if create_secrets_toml():
        print("\n[SUCCESS] Done! You can now run: streamlit run app_streamlit.py")
    else:
        print("\n[ERROR] Failed to create secrets.toml. Please check the errors above.")

