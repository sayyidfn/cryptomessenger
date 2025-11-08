# Dark Theme Colors
COLORS = {
    'background': '#0f172a',
    'surface': '#1e293b',
    'primary': '#3b82f6',
    'primary_dark': '#2563eb',
    'text': '#f1f5f9',
    'text_secondary': '#94a3b8',
    'border': 'rgba(148, 163, 184, 0.2)',
    'success': '#10b981',
    'error': '#ef4444',
    'warning': '#f59e0b'
}

# Global CSS
GLOBAL_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {COLORS['background']} 0%, #1a2332 100%);
    }}
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        color: {COLORS['text']};
        padding: 12px;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: rgba(30, 41, 59, 0.5);
        padding: 8px;
        border-radius: 12px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px;
        color: {COLORS['text_secondary']};
        padding: 12px 20px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS['primary']};
        color: white;
    }}
    
    .stFileUploader {{
        background: rgba(30, 41, 59, 0.5);
        border: 2px dashed {COLORS['border']};
        border-radius: 12px;
        padding: 20px;
    }}
    
    .stExpander {{
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['background']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['primary']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['primary_dark']};
    }}
</style>
"""

def apply_global_styles():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
