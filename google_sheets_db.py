import gspread
from google.oauth2.service_account import Credentials
from config import Config
from typing import List, Dict, Optional
import json

class GoogleSheetsDB:
    def __init__(self):
        self.config = Config()
        self.client = None
        self.sheet = None
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets"""
        import time
        max_retries = 3
        retry_delay = 10  # seconds
        
        for attempt in range(max_retries):
            try:
                scope = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                creds = Credentials.from_service_account_file(
                    self.config.GOOGLE_SHEETS_CREDENTIALS,
                    scopes=scope
                )
                self.client = gspread.authorize(creds)
                if self.config.GOOGLE_SHEET_ID:
                    self.sheet = self.client.open_by_key(self.config.GOOGLE_SHEET_ID)
                else:
                    # Create a new sheet if no ID provided
                    self.sheet = self.client.create('Teddybuddies Asset Database')
                    self.config.GOOGLE_SHEET_ID = self.sheet.id
                self._initialize_sheets()
                return  # Success, exit the retry loop
            except Exception as e:
                error_str = str(e)
                # Check if it's a rate limit error
                if '429' in error_str or 'RATE_LIMIT_EXCEEDED' in error_str or 'Quota exceeded' in error_str:
                    if attempt < max_retries - 1:
                        print(f"Rate limit exceeded. Waiting {retry_delay} seconds before retry {attempt + 1}/{max_retries}...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        print(f"Rate limit exceeded after {max_retries} attempts. Please wait a minute and restart the server.")
                        raise
                else:
                    # Not a rate limit error, raise immediately
                    print(f"Error connecting to Google Sheets: {e}")
                    raise
    
    def _initialize_sheets(self):
        """Initialize all required sheets if they don't exist"""
        sheet_names = ['Users', 'Locations', 'Categories', 'Subcategories', 
                      'AssetTypes', 'Brands', 'Assets', 'AssetMovements', 'ActivityLogs']
        
        for sheet_name in sheet_names:
            try:
                worksheet = self.sheet.worksheet(sheet_name)
                # Ensure headers are up-to-date for existing sheets
                self._ensure_headers(sheet_name)
            except gspread.WorksheetNotFound:
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
        """Ensure headers exist and are up-to-date for existing sheets"""
        worksheet = self.sheet.worksheet(sheet_name)
        
        expected_headers = {
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
        
        if sheet_name not in expected_headers:
            return
        
        # Get current headers
        try:
            current_headers = worksheet.row_values(1)
        except:
            current_headers = []
        
        # If no headers exist, set them
        if not current_headers:
            worksheet.append_row(expected_headers[sheet_name])
            return
        
        # Check if we need to add missing headers
        missing_headers = []
        for header in expected_headers[sheet_name]:
            if header not in current_headers:
                missing_headers.append(header)
        
        # Add missing headers
        if missing_headers:
            # Get the last column index
            last_col = len(current_headers)
            # Add new headers starting from the next column
            start_col = last_col + 1
            for i, header in enumerate(missing_headers):
                col_idx = start_col + i
                worksheet.update_cell(1, col_idx, header)
    
    def get_all(self, sheet_name: str) -> List[Dict]:
        """Get all records from a sheet"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            # Get all values including empty rows
            all_values = worksheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                # No headers or no data rows
                return []
            
            # Get headers from first row
            headers = [str(h).strip() for h in all_values[0]]
            
            # Process data rows
            records = []
            for row in all_values[1:]:
                # Skip completely empty rows
                if not any(row):
                    continue
                
                # Create a dictionary for this row
                record = {}
                for i, header in enumerate(headers):
                    # Get value from row, or empty string if index is out of range
                    value = row[i] if i < len(row) else ''
                    record[header] = value.strip() if value else ''
                
                # Only add records that have at least one non-empty value
                if any(record.values()):
                    records.append(record)
            
            return records
        except Exception as e:
            print(f"Error getting records from {sheet_name}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_by_id(self, sheet_name: str, id_field: str, id_value: str) -> Optional[Dict]:
        """Get a record by ID"""
        records = self.get_all(sheet_name)
        for record in records:
            if str(record.get(id_field)) == str(id_value):
                return record
        return None
    
    def insert(self, sheet_name: str, data: Dict) -> bool:
        """Insert a new record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            headers = worksheet.row_values(1)
            row = [data.get(header, '') for header in headers]
            worksheet.append_row(row)
            return True
        except Exception as e:
            print(f"Error inserting record into {sheet_name}: {e}")
            return False
    
    def update(self, sheet_name: str, id_field: str, id_value: str, data: Dict) -> bool:
        """Update a record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            records = worksheet.get_all_values()
            headers = records[0] if records else []
            
            # Find the row index
            row_idx = None
            id_col_idx = headers.index(id_field) if id_field in headers else None
            
            if id_col_idx is None:
                return False
            
            for i, row in enumerate(records[1:], start=2):
                if len(row) > id_col_idx and str(row[id_col_idx]) == str(id_value):
                    row_idx = i
                    break
            
            if row_idx is None:
                return False
            
            # Update the row
            for header, value in data.items():
                if header in headers:
                    col_idx = headers.index(header) + 1
                    worksheet.update_cell(row_idx, col_idx, value)
            
            return True
        except Exception as e:
            print(f"Error updating record in {sheet_name}: {e}")
            return False
    
    def delete(self, sheet_name: str, id_field: str, id_value: str) -> bool:
        """Delete a record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            records = worksheet.get_all_values()
            headers = records[0] if records else []
            
            id_col_idx = headers.index(id_field) if id_field in headers else None
            if id_col_idx is None:
                return False
            
            row_idx = None
            for i, row in enumerate(records[1:], start=2):
                if len(row) > id_col_idx and str(row[id_col_idx]) == str(id_value):
                    row_idx = i
                    break
            
            if row_idx:
                worksheet.delete_rows(row_idx)
                return True
            return False
        except Exception as e:
            print(f"Error deleting record from {sheet_name}: {e}")
            return False
    
    def get_next_id(self, sheet_name: str, id_field: str = 'ID') -> int:
        """Get the next available ID"""
        records = self.get_all(sheet_name)
        if not records:
            return 1
        ids = [int(record.get(id_field, 0)) for record in records if record.get(id_field)]
        return max(ids) + 1 if ids else 1
    
    def generate_asset_code(self, asset_type: str) -> str:
        """Generate asset code based on asset type"""
        records = self.get_all('Assets')
        # Count existing assets of this type
        type_count = sum(1 for r in records if r.get('Asset Type', '') == asset_type)
        # Format: TYPE-001, TYPE-002, etc.
        return f"{asset_type.upper().replace(' ', '')[:4]}-{str(type_count + 1).zfill(4)}"

