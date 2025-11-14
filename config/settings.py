import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load credentials from Streamlit Secrets or .env
try:
    import streamlit as st
    # Try to access secrets (only works on Streamlit Cloud)
    SUPABASE_URL = st.secrets['SUPABASE_URL']
    SUPABASE_KEY = st.secrets['SUPABASE_KEY']
    DATABASE_MASTER_KEY = st.secrets['DATABASE_MASTER_KEY']
    HMAC_SECRET_KEY = st.secrets['HMAC_SECRET_KEY']
except (FileNotFoundError, KeyError, ImportError):
    # Running locally - use .env file
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    DATABASE_MASTER_KEY = os.getenv('DATABASE_MASTER_KEY')
    HMAC_SECRET_KEY = os.getenv('HMAC_SECRET_KEY')

# Validation
if not all([SUPABASE_URL, SUPABASE_KEY, DATABASE_MASTER_KEY, HMAC_SECRET_KEY]):
    raise ValueError("Missing required environment variables. Please check .env file or Streamlit Secrets.")

# Encryption Configuration
ENCRYPTION_KEY_DB = DATABASE_MASTER_KEY
HMAC_KEY = HMAC_SECRET_KEY

# App Configuration
APP_TITLE = "CryptoMessenger"
APP_ICON = "💬"
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# File Upload Limits
MAX_FILE_SIZE_MB = 200
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Settings class for backward compatibility
class Settings:
    SUPABASE_URL = SUPABASE_URL
    SUPABASE_KEY = SUPABASE_KEY
    DATABASE_MASTER_KEY = DATABASE_MASTER_KEY
    HMAC_SECRET_KEY = HMAC_SECRET_KEY
    ENCRYPTION_KEY_DB = ENCRYPTION_KEY_DB
    HMAC_KEY = HMAC_KEY
    APP_TITLE = APP_TITLE
    APP_ICON = APP_ICON
    PAGE_CONFIG = PAGE_CONFIG
    MAX_FILE_SIZE_MB = MAX_FILE_SIZE_MB
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_BYTES
