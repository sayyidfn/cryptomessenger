import json
import base64
from typing import Tuple, List, Dict
from services.database_service import db
from services.crypto_service import (
    encrypt_text_aes_ctr_hmac, decrypt_text_aes_ctr_hmac,
    hide_message_in_image, extract_message_from_image,
    encrypt_file_aes_gcm, decrypt_file_aes_gcm
)


class Message:
    @staticmethod
    def send_text(sender_id: str, receiver_id: str, message: str, encryption_key: str) -> Tuple[bool, str]:
        try:
            # Enkripsi message dengan AES-256-CTR + HMAC-SHA256
            encrypted_content = encrypt_text_aes_ctr_hmac(message, encryption_key)
            
            # Prepare message data
            message_data = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message_type': 'text',
                'encrypted_content': encrypted_content
            }
            
            # Insert ke database
            response = db.from_('messages').insert(message_data).execute()
            
            if not response.data:
                raise Exception('Gagal mengirim pesan')
            
            return True, "Pesan teks berhasil dikirim"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def decrypt_text(encrypted_content: str, encryption_key: str) -> str:
        return decrypt_text_aes_ctr_hmac(encrypted_content, encryption_key)
    
    @staticmethod
    def send_image_steganography(sender_id: str, receiver_id: str, image_bytes: bytes, 
                                  secret_message: str, encryption_key: str) -> Tuple[bool, str]:
        try:
            # Hide message in image
            stego_image = hide_message_in_image(image_bytes, secret_message, encryption_key)
            
            # Convert to base64 untuk disimpan di database
            image_base64 = base64.b64encode(stego_image).decode('utf-8')
            
            # Simpan ke database dengan message_type = 'image'
            message_data = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message_type': 'image',
                'encrypted_content': image_base64
            }
            
            response = db.from_('messages').insert(message_data).execute()
            
            return True, "Pesan gambar dengan pesan tersembunyi berhasil dikirim"
            
        except Exception as e:
            return False, f"Error sending image: {str(e)}"
    
    @staticmethod
    def extract_from_image(image_data: bytes, encryption_key: str) -> str:
        return extract_message_from_image(image_data, encryption_key)
    
    @staticmethod
    def send_file(sender_id: str, receiver_id: str, file_bytes: bytes, 
                  filename: str, encryption_key: str) -> Tuple[bool, str]:
        try:
            # Enkripsi file dengan AES-256-GCM
            encrypted_content = encrypt_file_aes_gcm(file_bytes, encryption_key)
            
            # Simpan filename dan encrypted content sebagai JSON
            file_data = {
                'filename': filename,
                'encrypted_content': encrypted_content
            }
            
            file_json = json.dumps(file_data)
            
            # Simpan ke database dengan message_type = 'file'
            message_data = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message_type': 'file',
                'encrypted_content': file_json
            }
            
            response = db.from_('messages').insert(message_data).execute()
            
            return True, "Pesan file berhasil dikirim"
            
        except Exception as e:
            return False, f"Error sending file: {str(e)}"
    
    @staticmethod
    def get_messages(user1_id: str, user2_id: str) -> List[Dict]:
        try:
            # Query messages antara dua user (both directions)
            response = db.from_('messages').select('*').or_(
                f'and(sender_id.eq.{user1_id},receiver_id.eq.{user2_id}),and(sender_id.eq.{user2_id},receiver_id.eq.{user1_id})'
            ).order('created_at', desc=False).execute()
            
            return response.data if response.data else []
            
        except:
            return []
