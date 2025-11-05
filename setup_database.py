"""Interactive script to set up and configure the database"""
import os
import json
from pathlib import Path
from google_sheets_db import GoogleSheetsDB
from config import Config

def check_credentials():
    """Check if credentials file exists and is valid"""
    print("\n" + "="*60)
    print("STEP 1: Checking Credentials File")
    print("="*60)
    
    creds_path = Path('credentials.json')
    if not creds_path.exists():
        print("\n[ERROR] credentials.json file NOT FOUND!")
        print("\nPlease download it from Google Cloud Console:")
        print("1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316")
        print("2. Click on: asset-database@asset-database-477316.iam.gserviceaccount.com")
        print("3. Go to 'Keys' tab → 'Add Key' → 'Create new key' → Select 'JSON'")
        print("4. Download and save as 'credentials.json' in this folder")
        return False
    
    print(f"[OK] credentials.json exists")
    
    # Validate JSON structure
    try:
        with open(creds_path, 'r', encoding='utf-8') as f:
            creds_data = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing = [f for f in required_fields if f not in creds_data]
        
        if missing:
            print(f"[ERROR] Missing fields: {', '.join(missing)}")
            return False
        
        if creds_data.get('type') != 'service_account':
            print(f"[ERROR] Invalid key type: {creds_data.get('type')}")
            return False
        
        print(f"[OK] Valid service account credentials")
        print(f"[INFO] Service Account: {creds_data.get('client_email')}")
        return True, creds_data.get('client_email')
        
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON format in credentials.json")
        return False
    except Exception as e:
        print(f"[ERROR] Error reading credentials: {e}")
        return False

def check_sheet_sharing(service_account_email):
    """Guide user to check sheet sharing"""
    print("\n" + "="*60)
    print("STEP 2: Verify Google Sheet Sharing")
    print("="*60)
    
    sheet_url = "https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit"
    
    print(f"\n[IMPORTANT] Make sure the Google Sheet is shared with:")
    print(f"   Email: {service_account_email}")
    print(f"   Permission: Editor")
    print(f"\nSheet URL: {sheet_url}")
    print("\n1. Open the link above")
    print("2. Click 'Share' button (top right)")
    print("3. Add the email above with 'Editor' permission")
    print("4. Click 'Share'")
    print("\n[INFO] Proceeding to test connection...")

def test_connection():
    """Test Google Sheets connection"""
    print("\n" + "="*60)
    print("STEP 3: Testing Database Connection")
    print("="*60)
    
    try:
        print("\nAttempting to connect to Google Sheets...")
        db = GoogleSheetsDB()
        print("[SUCCESS] Connected to Google Sheets successfully!")
        
        # Test accessing the sheet
        sheet_id = Config().GOOGLE_SHEET_ID
        print(f"[OK] Sheet ID: {sheet_id}")
        
        return db
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] Credentials file not found: {e}")
        return None
    except Exception as e:
        error_msg = str(e)
        if "Invalid JWT Signature" in error_msg:
            print("\n[ERROR] Invalid JWT Signature - Credentials key is invalid!")
            print("\nSOLUTION: You need to download a NEW key from Google Cloud Console:")
            print("1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316")
            print("2. Click on the service account")
            print("3. Go to 'Keys' tab → 'Add Key' → 'Create new key' → Select 'JSON'")
            print("4. Download and replace credentials.json")
        elif "PERMISSION_DENIED" in error_msg or "access" in error_msg.lower():
            print("\n[ERROR] Permission denied - Sheet not shared!")
            print(f"\nSOLUTION: Share the Google Sheet with the service account email")
        else:
            print(f"\n[ERROR] Connection failed: {error_msg}")
        return None

def initialize_database(db):
    """Initialize database structure"""
    print("\n" + "="*60)
    print("STEP 4: Initializing Database Structure")
    print("="*60)
    
    if not db:
        print("[ERROR] Cannot initialize - database connection failed")
        return False
    
    try:
        # The _initialize_sheets() is called automatically in __init__
        # Just verify sheets exist
        sheet_names = ['Users', 'Locations', 'Categories', 'Subcategories', 
                      'AssetTypes', 'Brands', 'Assets', 'AssetMovements']
        
        print("\nChecking required sheets...")
        for sheet_name in sheet_names:
            try:
                worksheet = db.sheet.worksheet(sheet_name)
                # Get row count
                row_count = len(worksheet.get_all_values())
                print(f"  [OK] {sheet_name} - {row_count} rows")
            except Exception as e:
                print(f"  [WARNING] {sheet_name} - {e}")
        
        print("\n[SUCCESS] Database structure verified!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_default_admin(db):
    """Create default admin user if none exists"""
    print("\n" + "="*60)
    print("STEP 5: Setting Up Default Admin User")
    print("="*60)
    
    if not db:
        print("[ERROR] Cannot create admin - database connection failed")
        return False
    
    try:
        users = db.get_all('Users')
        
        # Check if any admin exists
        has_admin = any(user.get('Role', '').lower() == 'admin' for user in users)
        
        if has_admin:
            print("\n[OK] Admin user already exists")
            return True
        
        print("\nNo admin user found. Creating default admin...")
        print("\nDefault Admin Credentials:")
        print("  Username: admin")
        print("  Email: admin@example.com")
        print("  Password: admin123")
        print("\n[IMPORTANT] Please change this password after first login!")
        
        import hashlib
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        
        admin_data = {
            'Username': 'admin',
            'Email': 'admin@example.com',
            'Password': password_hash,
            'Role': 'admin'
        }
        
        if db.insert('Users', admin_data):
            print("[SUCCESS] Default admin user created!")
            return True
        else:
            print("[ERROR] Failed to create admin user")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("DATABASE SETUP AND CONFIGURATION")
    print("="*60)
    print("\nThis script will help you configure the database connection.")
    
    # Step 1: Check credentials
    creds_result = check_credentials()
    if not creds_result:
        print("\n[SETUP INCOMPLETE] Please fix credentials file and run again.")
        return
    
    _, service_account_email = creds_result
    
    # Step 2: Check sheet sharing
    check_sheet_sharing(service_account_email)
    
    # Step 3: Test connection
    db = test_connection()
    if not db:
        print("\n[SETUP INCOMPLETE] Please fix connection issues and run again.")
        return
    
    # Step 4: Initialize database
    if not initialize_database(db):
        print("\n[WARNING] Database initialization had issues, but continuing...")
    
    # Step 5: Create default admin
    create_default_admin(db)
    
    # Final summary
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\n[SUCCESS] Database is now configured and ready to use!")
    print("\nNext steps:")
    print("1. Start the Flask server: python app.py")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Login with default admin credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n[IMPORTANT] Change the default admin password after first login!")
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()

