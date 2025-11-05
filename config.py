import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    GOOGLE_SHEETS_CREDENTIALS = os.environ.get('GOOGLE_SHEETS_CREDENTIALS') or 'credentials.json'
    # Default to Teddybuddies Asset Database Sheet ID
    GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID') or '1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec'

