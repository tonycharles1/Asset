"""Script to validate credentials.json file"""
import json
import os
from pathlib import Path

def validate_credentials():
    """Validate the credentials.json file"""
    creds_path = Path('credentials.json')
    
    print("=" * 60)
    print("CREDENTIALS VALIDATION")
    print("=" * 60)
    
    # Check if file exists
    if not creds_path.exists():
        print("\n[ERROR] credentials.json file NOT FOUND!")
        print("Please download it from Google Cloud Console.")
        return False
    
    print(f"\n[OK] File exists: {creds_path.absolute()}")
    print(f"[OK] File size: {creds_path.stat().st_size} bytes")
    print(f"[OK] Last modified: {creds_path.stat().st_mtime}")
    
    # Check if file is readable
    try:
        with open(creds_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"[OK] File is readable")
    except Exception as e:
        print(f"\n[ERROR] Cannot read file: {e}")
        return False
    
    # Check if it's valid JSON
    try:
        creds_data = json.loads(content)
        print("[OK] Valid JSON format")
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON format: {e}")
        print("The file may be corrupted. Please download a fresh copy.")
        return False
    
    # Check required fields
    required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 
                      'client_email', 'client_id', 'auth_uri', 'token_uri']
    
    missing_fields = []
    for field in required_fields:
        if field not in creds_data:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"\n[ERROR] Missing required fields: {', '.join(missing_fields)}")
        print("This is not a valid service account key file.")
        return False
    
    print("[OK] All required fields present")
    
    # Check if it's a service account key
    if creds_data.get('type') != 'service_account':
        print(f"\n[ERROR] Wrong key type: {creds_data.get('type')}")
        print("Expected: service_account")
        return False
    
    print(f"[OK] Key type: {creds_data.get('type')}")
    print(f"[OK] Project ID: {creds_data.get('project_id')}")
    print(f"[OK] Service Account Email: {creds_data.get('client_email')}")
    
    # Check private key format
    private_key = creds_data.get('private_key', '')
    if not private_key.startswith('-----BEGIN PRIVATE KEY-----'):
        print(f"\n[WARNING] Private key format may be incorrect")
        print("The private key should start with '-----BEGIN PRIVATE KEY-----'")
    else:
        print("[OK] Private key format looks correct")
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print("\n[SUCCESS] Credentials file structure is valid!")
    print(f"\nService Account Email: {creds_data.get('client_email')}")
    print("\nIMPORTANT: Make sure this email is shared with your Google Sheet:")
    print("https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit")
    print("\nShare permission: Editor")
    
    return True

if __name__ == '__main__':
    try:
        validate_credentials()
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()

