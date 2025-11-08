import streamlit as st
from datetime import datetime
import base64
import json
from models.user import User
from models.message import Message


class LoginPage:
    def render(self):
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        
        with col2:
            # Logo & Title
            st.markdown("""
                <div style='text-align: center; margin-bottom: 40px;'>
                    <div style='font-size: 64px; margin-bottom: 4px;'>💬</div>
                    <h1 style='color: #f1f5f9; font-size: 42px; font-weight: 700; margin-bottom: 4px;'>CryptoMessenger</h1>
                    <p style='color: #94a3b8; font-size: 16px;'>End-to-end encrypted chat</p>
                    <h1 style='color: #f1f5f9; font-size: 32px; font-weight: 600; margin-bottom: 8px;'>Login</h1>
                </div>
            """, unsafe_allow_html=True)
            
            # Login Form
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="Enter your email")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    login_button = st.form_submit_button("Login", use_container_width=True, type="primary")
                with col_btn2:
                    register_button = st.form_submit_button("Register", use_container_width=True)
                
                if login_button:
                    if not email or not password:
                        st.error("✕ Email dan password harus diisi!")
                    else:
                        with st.spinner("Logging in..."):
                            success, result = User.login(email, password)
                            
                            if success:
                                st.session_state.user = result
                                st.session_state.page = 'chat'
                                st.success("✓ Login berhasil!")
                                st.rerun()
                            else:
                                st.error(f"✕ {result}")
                
                if register_button:
                    st.session_state.page = 'register'
                    st.rerun()


class RegisterPage:
    def render(self):
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        
        with col2:
            # Logo & Title
            st.markdown("""
                <div style='text-align: center; margin-bottom: 40px;'>
                    <div style='font-size: 64px; margin-bottom: 4px;'>💬</div>
                    <h1 style='color: #f1f5f9; font-size: 42px; font-weight: 700; margin-bottom: 4px;'>CryptoMessenger</h1>
                    <p style='color: #94a3b8; font-size: 16px;'>End-to-end encrypted chat</p>
                    <h1 style='color: #f1f5f9; font-size: 32px; font-weight: 600; margin-bottom: 8px;'>Register</h1>
                </div>
            """, unsafe_allow_html=True)
            
            # Register Form
            with st.form("register_form"):
                email = st.text_input("📧 Email", placeholder="Enter your email")
                username = st.text_input("👤 Username", placeholder="Choose a username")
                password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    register_button = st.form_submit_button("Register", use_container_width=True, type="primary")
                with col_btn2:
                    back_button = st.form_submit_button("Back to Login", use_container_width=True)
                
                if register_button:
                    if not all([email, username, password, confirm_password]):
                        st.error("✕ Semua field harus diisi!")
                    elif password != confirm_password:
                        st.error("✕ Password tidak cocok!")
                    elif len(password) < 6:
                        st.error("✕ Password minimal 6 karakter!")
                    else:
                        with st.spinner("Creating account..."):
                            success, result = User.register(email, username, password)
                            
                            if success:
                                st.success(f"✓ {result}")
                                st.session_state.page = 'login'
                                st.rerun()
                            else:
                                st.error(f"✕ {result}")
                
                if back_button:
                    st.session_state.page = 'login'
                    st.rerun()


class ChatPage:
    def render(self):
        # Import here to avoid circular import
        from ui.components import Sidebar, ChatArea, MessageInput
        
        # Check if user is logged in
        if not st.session_state.user:
            st.session_state.page = 'login'
            st.rerun()
        
        # Render sidebar
        Sidebar().render()
        
        # Main chat area
        if st.session_state.selected_user:
            # Render chat messages
            ChatArea().render()
            
            # Render message input tabs
            MessageInput().render()
        else:
            # Empty state
            st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
            st.markdown("""
                <div style='text-align: center; padding: 60px 20px;'>
                    <div style='font-size: 80px; margin-bottom: 20px; opacity: 0.3;'>💬</div>
                    <h2 style='color: #f1f5f9; font-size: 28px; margin-bottom: 12px; font-weight: 700;'>Select a User to Start Chatting</h2>
                    <p style='color: #94a3b8; font-size: 16px;'>Choose a user from the sidebar to begin a secure conversation</p>
                </div>
            """, unsafe_allow_html=True)
