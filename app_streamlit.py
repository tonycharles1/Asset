"""
Streamlit Asset Management System
Converted from Flask application
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import io

# Page configuration
st.set_page_config(
    page_title="Asset Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @font-face {
        font-family: 'DIN';
        src: local('DIN'), local('DIN-Regular'), local('FF DIN'), local('FF-DIN-Regular');
        font-weight: 400;
        font-style: normal;
    }
    
    * {
        font-family: 'DIN', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #718096;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        background-color: #ff6b35;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #e55a2b;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'db' not in st.session_state:
    st.session_state.db = None
if 'show_add_asset' not in st.session_state:
    st.session_state.show_add_asset = False

# Database connection class for Streamlit
class GoogleSheetsDB:
    def __init__(self):
        self.client = None
        self.sheet = None
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets using Streamlit secrets"""
        try:
            # Get credentials from Streamlit secrets
            if 'GOOGLE_SHEETS' in st.secrets:
                try:
                    creds_dict = {
                        "type": st.secrets["GOOGLE_SHEETS"]["type"],
                        "project_id": st.secrets["GOOGLE_SHEETS"]["project_id"],
                        "private_key_id": st.secrets["GOOGLE_SHEETS"]["private_key_id"],
                        "private_key": st.secrets["GOOGLE_SHEETS"]["private_key"],
                        "client_email": st.secrets["GOOGLE_SHEETS"]["client_email"],
                        "client_id": st.secrets["GOOGLE_SHEETS"]["client_id"],
                        "auth_uri": st.secrets["GOOGLE_SHEETS"]["auth_uri"],
                        "token_uri": st.secrets["GOOGLE_SHEETS"]["token_uri"],
                        "auth_provider_x509_cert_url": st.secrets["GOOGLE_SHEETS"]["auth_provider_x509_cert_url"],
                        "client_x509_cert_url": st.secrets["GOOGLE_SHEETS"]["client_x509_cert_url"]
                    }
                    
                    credentials = Credentials.from_service_account_info(
                        creds_dict,
                        scopes=['https://www.googleapis.com/auth/spreadsheets',
                               'https://www.googleapis.com/auth/drive']
                    )
                except Exception as e:
                    st.warning(f"Error loading from secrets: {e}. Trying credentials.json file...")
                    # Fallback to file
                    if os.path.exists('credentials.json'):
                        credentials = Credentials.from_service_account_file(
                            'credentials.json',
                            scopes=['https://www.googleapis.com/auth/spreadsheets',
                                   'https://www.googleapis.com/auth/drive']
                        )
                    else:
                        raise Exception("No credentials found in secrets or credentials.json file")
            else:
                # Fallback to credentials.json file
                if os.path.exists('credentials.json'):
                    credentials = Credentials.from_service_account_file(
                        'credentials.json',
                        scopes=['https://www.googleapis.com/auth/spreadsheets',
                               'https://www.googleapis.com/auth/drive']
                    )
                else:
                    raise Exception("No credentials found. Please add secrets.toml or credentials.json file")
            
            self.client = gspread.authorize(credentials)
            sheet_id = st.secrets.get("GOOGLE_SHEET_ID", "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec")
            self.sheet = self.client.open_by_key(sheet_id)
            self._initialize_sheets()
            
        except Exception as e:
            st.error(f"Error connecting to Google Sheets: {e}")
            st.stop()
    
    def _initialize_sheets(self):
        """Initialize all required sheets if they don't exist"""
        sheet_names = ['Users', 'Locations', 'Categories', 'Subcategories', 
                      'AssetTypes', 'Brands', 'Assets', 'AssetMovements', 'ActivityLogs']
        
        for sheet_name in sheet_names:
            try:
                worksheet = self.sheet.worksheet(sheet_name)
                self._ensure_headers(sheet_name)
            except:
                worksheet = self.sheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
                self._set_headers(sheet_name)
    
    def _set_headers(self, sheet_name: str):
        """Set headers for each sheet"""
        worksheet = self.sheet.worksheet(sheet_name)
        
        headers = {
            'Users': ['Username', 'Email', 'Password', 'Role'],
            'Locations': ['ID', 'Location Name'],
            'Categories': ['ID', 'Category Name'],
            'Subcategories': ['ID', 'Subcategory Name', 'Category ID'],
            'AssetTypes': ['Asset Code', 'Asset Type', 'Depreciation Value (%)'],
            'Brands': ['ID', 'Brand Name'],
            'Assets': ['Asset Code', 'Item Name', 'Asset Category', 'Asset SubCategory', 
                      'Brand', 'Asset Description', 'Amount', 'Location', 
                      'Date of Purchase', 'Warranty', 'Department', 'Ownership',
                      'Asset Status', 'Image Attachment', 'Document Attachment'],
            'AssetMovements': ['ID', 'Asset Code', 'From Location', 'To Location', 
                              'Movement Date', 'Moved By', 'Notes'],
            'ActivityLogs': ['ID', 'Date & Time', 'Type', 'User', 'Action', 'Entity Type', 
                           'Entity ID', 'Description', 'Details']
        }
        
        if sheet_name in headers:
            worksheet.append_row(headers[sheet_name])
    
    def _ensure_headers(self, sheet_name: str):
        """Ensure headers exist and are up-to-date"""
        # Simplified version - same logic as Flask version
        pass
    
    def get_all(self, sheet_name: str) -> List[Dict]:
        """Get all records from a sheet"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            all_values = worksheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                return []
            
            headers = [str(h).strip() for h in all_values[0]]
            records = []
            
            for row in all_values[1:]:
                if not any(row):
                    continue
                
                record = {}
                for i, header in enumerate(headers):
                    value = row[i] if i < len(row) else ''
                    record[header] = value.strip() if value else ''
                
                if any(record.values()):
                    records.append(record)
            
            return records
        except Exception as e:
            st.error(f"Error getting records from {sheet_name}: {e}")
            return []
    
    def get_by_id(self, sheet_name: str, id_field: str, id_value: str) -> Optional[Dict]:
        """Get a record by ID"""
        records = self.get_all(sheet_name)
        for record in records:
            if str(record.get(id_field)) == str(id_value):
                return record
        return None
    
    def get_next_id(self, sheet_name: str) -> int:
        """Get next available ID"""
        records = self.get_all(sheet_name)
        if not records:
            return 1
        ids = []
        for record in records:
            try:
                ids.append(int(record.get('ID', 0)))
            except:
                pass
        return max(ids, default=0) + 1
    
    def insert(self, sheet_name: str, data: Dict) -> bool:
        """Insert a new record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            headers = worksheet.row_values(1)
            row = [data.get(header, '') for header in headers]
            worksheet.append_row(row)
            return True
        except Exception as e:
            st.error(f"Error inserting record: {e}")
            return False
    
    def update(self, sheet_name: str, id_field: str, id_value: str, data: Dict) -> bool:
        """Update a record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            records = self.get_all(sheet_name)
            headers = worksheet.row_values(1)
            
            for i, record in enumerate(records, start=2):
                if str(record.get(id_field)) == str(id_value):
                    row = [data.get(header, record.get(header, '')) for header in headers]
                    worksheet.update(f"A{i}:{chr(64+len(headers))}{i}", [row])
                    return True
            return False
        except Exception as e:
            st.error(f"Error updating record: {e}")
            return False
    
    def delete(self, sheet_name: str, id_field: str, id_value: str) -> bool:
        """Delete a record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            records = self.get_all(sheet_name)
            
            for i, record in enumerate(records, start=2):
                if str(record.get(id_field)) == str(id_value):
                    worksheet.delete_rows(i)
                    return True
            return False
        except Exception as e:
            st.error(f"Error deleting record: {e}")
            return False

# Initialize database connection
@st.cache_resource
def get_db():
    """Get database connection (cached)"""
    try:
        return GoogleSheetsDB()
    except:
        return None

# Authentication functions
def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, password_hash: str) -> bool:
    """Check if password matches hash"""
    return hash_password(password) == password_hash

def login_page():
    """Login page"""
    st.title("Asset Management System")
    st.markdown('<p class="sub-header">Please login to continue</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                db = get_db()
                if db:
                    users = db.get_all('Users')
                    user = next((u for u in users if u.get('Username') == username), None)
                    
                    if user and check_password(password, user.get('Password', '')):
                        st.session_state.authenticated = True
                        st.session_state.user_id = username
                        st.session_state.role = user.get('Role', 'user')
                        st.session_state.db = db
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Database connection failed")
    
    with tab2:
        with st.form("register_form"):
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            reg_role = st.selectbox("Role", ["user", "admin"], key="reg_role")
            submit_reg = st.form_submit_button("Register", use_container_width=True)
            
            if submit_reg:
                if reg_password != reg_confirm:
                    st.error("Passwords do not match")
                elif reg_username and reg_email and reg_password:
                    db = get_db()
                    if db:
                        users = db.get_all('Users')
                        existing = next((u for u in users if u.get('Username') == reg_username), None)
                        if existing:
                            st.error("Username already exists")
                        else:
                            user_data = {
                                'Username': reg_username,
                                'Email': reg_email,
                                'Password': hash_password(reg_password),
                                'Role': reg_role
                            }
                            if db.insert('Users', user_data):
                                st.success("Registration successful! Please login.")
                            else:
                                st.error("Registration failed")
                else:
                    st.error("Please fill in all fields")

# Main app
def main():
    """Main application"""
    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Initialize database
    if st.session_state.db is None:
        st.session_state.db = get_db()
    
    if st.session_state.db is None:
        st.error("Database connection failed. Please check your configuration.")
        st.stop()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 📦 Asset Management")
        st.markdown(f"**User:** {st.session_state.user_id}")
        st.markdown(f"**Role:** {st.session_state.role}")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["Dashboard", "Assets", "Locations", "Categories", "Subcategories", 
             "Asset Types", "Brands", "Asset Movements", "Depreciation", 
             "Asset Report", "Movement Report", "Logs"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.role = None
            st.session_state.db = None
            st.rerun()
    
    # Route to appropriate page
    try:
        if page == "Dashboard":
            from pages import dashboard
            dashboard.show(st.session_state.db, st.session_state.role)
        elif page == "Assets":
            from pages import assets
            assets.show(st.session_state.db, st.session_state.role)
        elif page == "Locations":
            from pages import locations
            locations.show(st.session_state.db, st.session_state.role)
        elif page == "Categories":
            from pages import categories
            categories.show(st.session_state.db, st.session_state.role)
        elif page == "Subcategories":
            from pages import subcategories
            subcategories.show(st.session_state.db, st.session_state.role)
        elif page == "Asset Types":
            from pages import asset_types
            asset_types.show(st.session_state.db, st.session_state.role)
        elif page == "Brands":
            from pages import brands
            brands.show(st.session_state.db, st.session_state.role)
        elif page == "Asset Movements":
            from pages import asset_movements
            asset_movements.show(st.session_state.db, st.session_state.role)
        elif page == "Depreciation":
            from pages import depreciation
            depreciation.show(st.session_state.db, st.session_state.role)
        elif page == "Asset Report":
            from pages import asset_report
            asset_report.show(st.session_state.db, st.session_state.role)
        elif page == "Movement Report":
            from pages import movement_report
            movement_report.show(st.session_state.db, st.session_state.role)
        elif page == "Logs":
            from pages import logs
            logs.show(st.session_state.db, st.session_state.role)
    except Exception as e:
        st.error(f"Error loading page: {e}")
        st.exception(e)

if __name__ == "__main__":
    main()

