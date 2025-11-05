#!/usr/bin/env python
"""Test Google Sheets connection"""
from google_sheets_db import GoogleSheetsDB
import traceback

try:
    print("Attempting to connect to Google Sheets...")
    db = GoogleSheetsDB()
    print("[SUCCESS] Google Sheets connection established successfully!")
    print("\nTesting data retrieval...")
    assets = db.get_all('Assets')
    print(f"Retrieved {len(assets)} assets from the sheet")
    if assets:
        print(f"First asset: {assets[0]}")
except Exception as e:
    print(f"\n[ERROR] Connection failed: {type(e).__name__}")
    print(f"Error message: {e}")
    print("\nFull traceback:")
    traceback.print_exc()


