"""Test Streamlit connection to Google Sheets"""
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
import json

st.title("Test Google Sheets Connection")

st.write("Testing connection to Google Sheets...")

# Try to load credentials
try:
    # Option 1: Try Streamlit secrets
    if 'GOOGLE_SHEETS' in st.secrets:
        st.success("✅ Found credentials in Streamlit secrets")
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
        
        st.write("**Credentials loaded from secrets:**")
        st.json({
            "type": creds_dict["type"],
            "project_id": creds_dict["project_id"],
            "client_email": creds_dict["client_email"],
            "private_key_id": creds_dict["private_key_id"][:20] + "..."
        })
        
        credentials = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets',
                   'https://www.googleapis.com/auth/drive']
        )
    else:
        st.warning("⚠️ No secrets found, trying credentials.json file...")
        if os.path.exists('credentials.json'):
            st.success("✅ Found credentials.json file")
            credentials = Credentials.from_service_account_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/drive']
            )
        else:
            st.error("❌ No credentials found in secrets or credentials.json file")
            st.stop()
    
    # Try to connect
    st.write("**Attempting connection...**")
    client = gspread.authorize(credentials)
    
    sheet_id = st.secrets.get("GOOGLE_SHEET_ID", "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec")
    sheet = client.open_by_key(sheet_id)
    
    st.success("✅ **Connection successful!**")
    st.write(f"**Sheet name:** {sheet.title}")
    st.write(f"**Sheet ID:** {sheet_id}")
    
    # List worksheets
    st.write("**Available worksheets:**")
    worksheets = sheet.worksheets()
    for ws in worksheets:
        st.write(f"- {ws.title}")
    
except Exception as e:
    st.error(f"❌ **Connection failed:** {e}")
    
    if "Invalid JWT Signature" in str(e):
        st.error("""
        **Invalid JWT Signature Error**
        
        This means your credentials are invalid. Common causes:
        
        1. **Wrong private_key format in secrets.toml**
           - Must use triple quotes (three double quotes)
           - Must include BEGIN/END lines
           
        2. **Invalid credentials.json file**
           - Need to download a new key from Google Cloud Console
           
        3. **Credentials copied incorrectly**
           - Missing characters or extra spaces
           
        **Fix:**
        1. Check your secrets.toml format (see FIX_STREAMLIT_CREDENTIALS.md)
        2. Or download a fresh credentials.json from Google Cloud Console
        3. Verify Google Sheet is shared with service account email
        """)
    
    st.exception(e)

