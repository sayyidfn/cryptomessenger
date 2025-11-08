import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Encryption Configuration
ENCRYPTION_KEY_DB = os.getenv('DATABASE_MASTER_KEY')
HMAC_KEY = os.getenv('HMAC_SECRET_KEY')

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
