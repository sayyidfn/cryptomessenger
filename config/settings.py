import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Supabase Configuration - Support Streamlit Cloud Secrets
    try:
        import streamlit as st
        # Try to access secrets (only works on Streamlit Cloud)
        SUPABASE_URL = st.secrets['SUPABASE_URL']
        SUPABASE_KEY = st.secrets['SUPABASE_KEY']
        DATABASE_MASTER_KEY = st.secrets['DATABASE_MASTER_KEY']
        HMAC_SECRET_KEY = st.secrets['HMAC_SECRET_KEY']
    except (FileNotFoundError, KeyError):
        # Running locally - use .env file
        SUPABASE_URL = os.getenv('SUPABASE_URL')
        SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        DATABASE_MASTER_KEY = os.getenv('DATABASE_MASTER_KEY')
        HMAC_SECRET_KEY = os.getenv('HMAC_SECRET_KEY')
    
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

    # Validation
    if not all([SUPABASE_URL, SUPABASE_KEY, ENCRYPTION_KEY_DB, HMAC_KEY]):
        raise ValueError("Missing required environment variables in .env file")
