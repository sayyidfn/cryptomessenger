"""
CryptoMessenger - Aplikasi chat terenkripsi end-to-end.
Entry point aplikasi dengan struktur modular.

Struktur Proyek:
- config/: Konfigurasi aplikasi
- models/: Business logic & data models
- services/: External services (database, crypto)
- ui/: User interface components & pages
- utils/: Helper functions

Author: CryptoMessenger Team
"""

import streamlit as st
from config.settings import PAGE_CONFIG, APP_TITLE
from ui.styles import apply_global_styles

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply global styles
apply_global_styles()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None
if 'encryption_key' not in st.session_state:
    st.session_state.encryption_key = ''

def main():
    """Main application entry point."""
    
    # Import pages dynamically to avoid circular imports
    from ui.pages import LoginPage, RegisterPage, ChatPage
    
    # Route to appropriate page
    if st.session_state.page == 'login':
        LoginPage().render()
    elif st.session_state.page == 'register':
        RegisterPage().render()
    elif st.session_state.page == 'chat':
        ChatPage().render()

if __name__ == "__main__":
    main()
