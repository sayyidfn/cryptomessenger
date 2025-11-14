import streamlit as st
import base64
import json
from datetime import datetime
from models.user import User
from models.message import Message


class Sidebar:
    def render(self):
        with st.sidebar:
            # User info
            st.markdown(f"""
                <div style='
                    # background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                    padding: 24px;
                    border-radius: 16px;
                    margin-bottom: 24px;
                    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
                '>
                    <div style='text-align: center;'>
                        <div style='font-size: 48px; margin-bottom: 12px;'>👤</div>
                        <h2 style='color: white; font-size: 20px; margin-bottom: 4px; font-weight: 700;'>{st.session_state.user['username']}</h2>
                        <p style='color: rgba(255,255,255,0.8); font-size: 13px;'>{st.session_state.user['email']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.selected_user = None
                st.session_state.page = 'login'
                st.rerun()
            
            st.markdown("<div style='margin: 24px 0; height: 1px; background: rgba(255,255,255,0.2);'></div>", unsafe_allow_html=True)
            
            st.markdown("<h3 style='font-size: 18px; margin-bottom: 16px; font-weight: 600;'>👥 Pengguna Aktif</h3>", unsafe_allow_html=True)
            
            # Load users
            users = User.get_all()
            
            # Filter out current user
            other_users = [u for u in users if u['id'] != st.session_state.user['id']]
            
            for user in other_users:
                # User button
                is_selected = st.session_state.selected_user and st.session_state.selected_user['id'] == user['id']
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(
                    f"{'✅ ' if is_selected else ''}💬 {user['username']}",
                    key=f"user_{user['id']}",
                    use_container_width=True,
                    type=button_style
                ):
                    st.session_state.selected_user = user
                    st.rerun()


class ChatArea:
    def render(self):
        # Chat Header
        st.markdown(f"""
            <div style='
                background: rgba(30, 41, 59, 0.5);
                backdrop-filter: blur(10px);
                padding: 20px 24px;
                border-radius: 16px;
                margin-bottom: 24px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(59, 130, 246, 0.2);
            '>
                <div style='display: flex; align-items: center; gap: 14px;'>
                    <div style='
                        width: 50px;
                        height: 50px;
                        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                    '>👤</div>
                    <div>
                        <h2 style='color: #f1f5f9; font-size: 22px; margin: 0; font-weight: 700;'>{st.session_state.selected_user['username']}</h2>
                        <p style='color: #94a3b8; font-size: 13px; margin: 4px 0 0 0;'>End-to-end encrypted chat</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Messages container
        messages = Message.get_messages(
            st.session_state.user['id'],
            st.session_state.selected_user['id']
        )
        
        if messages:
            for msg in messages:
                self._render_message(msg)
        else:
            st.info("💬 Belum ada pesan. Mulai percakapan!")
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    def _render_message(self, msg):
        is_sent = msg['sender_id'] == st.session_state.user['id']
        message_type = msg.get('message_type', 'text').lower()
        
        # Format timestamp
        try:
            timestamp = datetime.fromisoformat(msg['created_at'].replace('Z', '+00:00'))
            time_str = timestamp.strftime("%H:%M")
        except:
            time_str = ""
        
        # Render based on message type
        if message_type == 'image':
            self._render_image_message(msg, is_sent, time_str)
        elif message_type == 'file':
            self._render_file_message(msg, is_sent, time_str)
        else:
            self._render_text_message(msg, is_sent, time_str)
    
    def _render_text_message(self, msg, is_sent, time_str):
        if is_sent:
            # Pengirim: tampilkan plaintext
            try:
                decrypted_text = Message.decrypt_text(msg['encrypted_content'], st.session_state.encryption_key)
            except:
                decrypted_text = "🔒 Tidak dapat mendekripsi pesan sendiri"
            
            st.markdown(
                f"""
                <div style='display: flex; justify-content: flex-end; margin-bottom: 12px;'>
                    <div style='
                        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                        color: white;
                        padding: 12px 16px;
                        border-radius: 16px;
                        border-bottom-right-radius: 4px;
                        max-width: 70%;
                        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                    '>
                        <div style='font-size: 14px; line-height: 1.5; margin-bottom: 4px;'>{decrypted_text}</div>
                        <div style='font-size: 11px; opacity: 0.8; text-align: right;'>{time_str}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Penerima: tampilkan form decrypt
            st.markdown(
                f"""
                <div style='display: flex; justify-content: flex-start; margin-bottom: 12px;'>
                    <div style='
                        background: rgba(30, 41, 59, 0.8);
                        color: #e2e8f0;
                        padding: 12px 16px;
                        border-radius: 16px;
                        border-bottom-left-radius: 4px;
                        max-width: 70%;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                        border: 1px solid rgba(59, 130, 246, 0.2);
                    '>
                        <div style='font-size: 14px; line-height: 1.5; margin-bottom: 4px;'>🔒 Pesan teks terenkripsi</div>
                        <div style='font-size: 11px; color: #94a3b8; text-align: left;'>{time_str}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Form untuk decrypt text message
            with st.expander("🔓 Dekripsi Pesan", expanded=False):
                decrypt_key = st.text_input(
                    "🔑 Kunci Enkripsi",
                    type="password",
                    key=f"decrypt_key_text_{msg['id']}",
                    placeholder="Masukkan kunci enkripsi"
                )
                
                if st.button(f"Dekripsi", key=f"decrypt_btn_text_{msg['id']}"):
                    if decrypt_key and decrypt_key.strip():
                        try:
                            decrypted_text = Message.decrypt_text(msg['encrypted_content'], decrypt_key)
                            st.success(f"✅ Pesan: **{decrypted_text}**")
                        except Exception as e:
                            st.error(f"❌ Kunci enkripsi salah: {str(e)}")
                    else:
                        st.warning("⚠️ Harap masukkan kunci enkripsi!")
    
    def _render_image_message(self, msg, is_sent, time_str):
        if is_sent:
            st.markdown(
                f"""
                <div style='display: flex; justify-content: flex-end; margin-bottom: 8px;'>
                    <div style='
                        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                        color: white;
                        padding: 8px 12px;
                        border-radius: 12px;
                        border-bottom-right-radius: 4px;
                        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
                    '>
                        <div style='font-size: 13px; font-weight: 600;'>🖼️ Gambar dengan pesan tersembunyi</div>
                        <div style='font-size: 11px; opacity: 0.8; margin-top: 2px;'>{time_str}</div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            # Show image aligned right using columns
            try:
                image_data = base64.b64decode(msg['encrypted_content'])
                col1, col2 = st.columns([2, 1])
                with col2:
                    st.image(image_data)
            except Exception as e:
                st.error(f"Error menampilkan gambar: {str(e)}")
        else:
            st.markdown(
                f"""
                <div style='display: flex; justify-content: flex-start; margin-bottom: 8px;'>
                    <div style='
                        background: rgba(30, 41, 59, 0.8);
                        color: #e2e8f0;
                        padding: 8px 12px;
                        border-radius: 12px;
                        border-bottom-left-radius: 4px;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                        border: 1px solid rgba(148, 163, 184, 0.2);
                    '>
                        <div style='font-size: 13px; font-weight: 600;'>🖼️ Gambar dengan pesan tersembunyi</div>
                        <div style='font-size: 11px; opacity: 0.7; margin-top: 2px;'>{time_str}</div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            # Show image aligned left with decrypt form
            try:
                image_data = base64.b64decode(msg['encrypted_content'])
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(image_data)
                    
                    # Form untuk ekstrak pesan tersembunyi
                    with st.expander("🔓 Ekstrak Pesan Tersembunyi", expanded=False):
                        decrypt_key = st.text_input(
                            "🔑 Kunci Enkripsi",
                            type="password",
                            key=f"decrypt_key_img_{msg['id']}",
                            placeholder="Masukkan kunci enkripsi"
                        )
                        
                        if st.button(f"Ekstrak Pesan", key=f"extract_btn_{msg['id']}"):
                            if decrypt_key and decrypt_key.strip():
                                try:
                                    hidden_message = Message.extract_from_image(image_data, decrypt_key)
                                    st.success(f"✅ Pesan tersembunyi: **{hidden_message}**")
                                except Exception as e:
                                    st.error(f"❌ Kunci enkripsi salah atau ekstraksi gagal: {str(e)}")
                            else:
                                st.warning("⚠️ Harap masukkan kunci enkripsi!")
            except Exception as e:
                st.error(f"Error menampilkan gambar: {str(e)}")
    
    def _render_file_message(self, msg, is_sent, time_str):
        try:
            file_data = json.loads(msg['encrypted_content'])
            filename = file_data['filename']
            
            if is_sent:
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-end; margin-bottom: 12px;'>
                        <div style='
                            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                            color: white;
                            padding: 12px 16px;
                            border-radius: 16px;
                            border-bottom-right-radius: 4px;
                            max-width: 400px;
                            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                        '>
                            <div style='font-size: 13px; margin-bottom: 4px; font-weight: 600;'>📎 {filename}</div>
                            <div style='font-size: 11px; opacity: 0.8;'>{time_str}</div>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-start; margin-bottom: 12px;'>
                        <div style='
                            background: rgba(30, 41, 59, 0.8);
                            color: #e2e8f0;
                            padding: 12px 16px;
                            border-radius: 16px;
                            border-bottom-left-radius: 4px;
                            max-width: 400px;
                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                            border: 1px solid rgba(148, 163, 184, 0.2);
                        '>
                            <div style='font-size: 13px; margin-bottom: 4px; font-weight: 600;'>📎 {filename}</div>
                            <div style='font-size: 11px; opacity: 0.7;'>{time_str}</div>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # AES-GCM Decryption
                with st.expander("🔓 Dekripsi & Unduh File", expanded=False):
                    decrypt_key = st.text_input(
                        "🔑 Kunci Enkripsi",
                        type="password",
                        key=f"decrypt_key_file_{msg['id']}",
                        placeholder="Masukkan kunci enkripsi"
                    )
                    
                    if st.button(f"Dekripsi & Unduh", key=f"decrypt_btn_file_{msg['id']}"):
                        if decrypt_key and decrypt_key.strip():
                            try:
                                from services.crypto_service import decrypt_file_aes_gcm
                                
                                # Decrypt file dengan AES-GCM
                                decrypted_file = decrypt_file_aes_gcm(
                                    file_data['encrypted_content'],
                                    decrypt_key
                                )
                                
                                st.download_button(
                                    label=f"💾 Simpan {filename}",
                                    data=decrypted_file,
                                    file_name=filename,
                                    mime="application/octet-stream",
                                    key=f"save_{msg['id']}"
                                )
                                st.success(f"✅ File berhasil didekripsi!")
                            except Exception as e:
                                st.error(f"❌ Kunci enkripsi salah atau file rusak: {str(e)}")
                        else:
                            st.warning("⚠️ Harap masukkan kunci enkripsi!")
        except Exception as e:
            st.error(f"Error memproses file: {str(e)}")


class MessageInput:
    def render(self):
        tab1, tab2, tab3 = st.tabs(["✉️ Pesan Teks", "🖼️ Gambar + Steganografi", "📎 File"])
        
        with tab1:
            self._render_text_tab()
        
        with tab2:
            self._render_image_tab()
        
        with tab3:
            self._render_file_tab()
    
    def _render_text_tab(self):
        with st.form("text_form", clear_on_submit=True):
            st.markdown("<label style='color: #94a3b8; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;'>🔑 Kunci Enkripsi</label>", unsafe_allow_html=True)
            encryption_key = st.text_input(
                "Kunci Enkripsi Teks",
                value=st.session_state.encryption_key,
                type="password",
                placeholder="Masukkan kunci enkripsi...",
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.markdown("<label style='color: #94a3b8; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;'>💬 Pesan</label>", unsafe_allow_html=True)
            message = st.text_area(
                "Pesan",
                placeholder="Ketik pesan Anda di sini...",
                height=100,
                label_visibility="collapsed"
            )

            if st.form_submit_button("Kirim Pesan Terenkripsi 🔒", use_container_width=True, type="primary"):
                if not encryption_key or not encryption_key.strip():
                    st.error("❌ Harap masukkan kunci enkripsi!")
                elif not message or not message.strip():
                    st.error("❌ Harap masukkan pesan!")
                else:
                    with st.spinner("Mengirim..."):
                        st.session_state.encryption_key = encryption_key
                        success, result = Message.send_text(
                            st.session_state.user['id'],
                            st.session_state.selected_user['id'],
                            message,
                            encryption_key
                        )
                        
                        if success:
                            st.success(f"✅ {result}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
    
    def _render_image_tab(self):
        with st.form("image_form", clear_on_submit=True):
            st.markdown("<label style='color: #94a3b8; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;'>🔑 Kunci Enkripsi</label>", unsafe_allow_html=True)
            encryption_key = st.text_input(
                "Kunci Enkripsi Gambar",
                value=st.session_state.encryption_key,
                type="password",
                placeholder="Masukkan kunci enkripsi...",
                label_visibility="collapsed",
                key="image_encryption_key"
            )
            
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.markdown("<label style='color: #94a3b8; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;'>🖼️ Unggah Gambar</label>", unsafe_allow_html=True)
            uploaded_image = st.file_uploader("Pilih gambar", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.markdown("<label style='color: #94a3b8; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;'>🔒 Pesan Rahasia</label>", unsafe_allow_html=True)
            secret_message = st.text_area(
                "Pesan Rahasia",
                placeholder="Masukkan pesan rahasia untuk disembunyikan dalam gambar...",
                height=80,
                label_visibility="collapsed"
            )
            
            if st.form_submit_button("Kirim Gambar dengan Pesan Tersembunyi 🔒", use_container_width=True, type="primary"):
                if not encryption_key or not encryption_key.strip():
                    st.error("❌ Harap masukkan kunci enkripsi!")
                elif not uploaded_image:
                    st.error("❌ Harap unggah gambar!")
                elif not secret_message or not secret_message.strip():
                    st.error("❌ Harap masukkan pesan rahasia!")
                else:
                    with st.spinner("Menyembunyikan pesan dan mengirim..."):
                        st.session_state.encryption_key = encryption_key
                        success, result = Message.send_image_steganography(
                            st.session_state.user['id'],
                            st.session_state.selected_user['id'],
                            uploaded_image.getvalue(),
                            secret_message,
                            encryption_key
                        )
                        
                        if success:
                            st.success(f"✅ {result}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
    
    def _render_file_tab(self):
        with st.form("file_form", clear_on_submit=True):
            st.markdown("<label style='color: #94a3b8; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;'>🔑 Kunci Enkripsi</label>", unsafe_allow_html=True)
            encryption_key = st.text_input(
                "Kunci Enkripsi File",
                value=st.session_state.encryption_key,
                type="password",
                placeholder="Masukkan kunci enkripsi...",
                label_visibility="collapsed",
                key="file_encryption_key"
            )
            
            st.markdown("<label style='color: #94a3b8; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block; margin-top: 12px;'>📎 Unggah File</label>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Pilih file", label_visibility="collapsed", key="file_upload")
            
            if uploaded_file:
                st.info(f"📎 Terpilih: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.form_submit_button("Kirim File Terenkripsi 🔒", use_container_width=True, type="primary"):
                if not uploaded_file:
                    st.error("❌ Harap unggah file!")
                elif not encryption_key or not encryption_key.strip():
                    st.error("❌ Harap masukkan kunci enkripsi!")
                else:
                    with st.spinner("Mengenkripsi dan mengirim file..."):
                        success, result = Message.send_file(
                            st.session_state.user['id'],
                            st.session_state.selected_user['id'],
                            uploaded_file.getvalue(),
                            uploaded_file.name,
                            encryption_key
                        )
                        
                        if success:
                            st.success(f"✅ {result}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
