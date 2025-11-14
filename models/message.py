import json
import base64
from typing import Tuple, List, Dict
from services.database_service import db
from services.crypto_service import (
    encrypt_text_aes_ctr_hmac, decrypt_text_aes_ctr_hmac,
    hide_message_in_image, extract_message_from_image,
    encrypt_file_aes_gcm, decrypt_file_aes_gcm,
    encrypt_for_database, decrypt_from_database
)


class Message:
    @staticmethod
    def send_text(sender_id: str, receiver_id: str, message: str, encryption_key: str) -> Tuple[bool, str]:
        try:
            # Layer 1: Enkripsi message dengan AES-256-CTR + HMAC-SHA256
            encrypted_aes = encrypt_text_aes_ctr_hmac(message, encryption_key)
            
            # Layer 2: Enkripsi dengan ChaCha20-Poly1305 untuk database
            encrypted_db = encrypt_for_database(encrypted_aes)
            
            # Prepare message data
            message_data = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message_type': 'text',
                'encrypted_content': encrypted_db['encrypted'],
                'encrypted_hmac': encrypted_db['hmac']
            }
            
            # Insert ke database
            response = db.from_('messages').insert(message_data).execute()
            
            if not response.data:
                raise Exception('Gagal mengirim pesan')
            
            return True, "Pesan teks berhasil dikirim"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def decrypt_text(encrypted_content: str, encrypted_hmac: str, encryption_key: str) -> str:
        # Layer 1: Decrypt dari ChaCha20-Poly1305
        decrypted_db = decrypt_from_database(encrypted_content, encrypted_hmac)
        
        # Layer 2: Decrypt dari AES-256-CTR + HMAC
        return decrypt_text_aes_ctr_hmac(decrypted_db, encryption_key)
    
    @staticmethod
    def send_image_steganography(sender_id: str, receiver_id: str, image_bytes: bytes, 
                                  secret_message: str, encryption_key: str) -> Tuple[bool, str]:
        try:
            # Layer 1: Hide message in image (LSB + 3DES)
            stego_image = hide_message_in_image(image_bytes, secret_message, encryption_key)
            
            # Convert to base64
            image_base64 = base64.b64encode(stego_image).decode('utf-8')
            
            # Layer 2: Enkripsi dengan ChaCha20-Poly1305 untuk database
            encrypted_db = encrypt_for_database(image_base64)
            
            # Simpan ke database dengan message_type = 'image'
            message_data = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message_type': 'image',
                'encrypted_content': encrypted_db['encrypted'],
                'encrypted_hmac': encrypted_db['hmac']
            }
            
            response = db.from_('messages').insert(message_data).execute()
            
            return True, "Pesan gambar dengan pesan tersembunyi berhasil dikirim"
            
        except Exception as e:
            return False, f"Error sending image: {str(e)}"
    
    @staticmethod
    def extract_from_image(encrypted_content: str, encrypted_hmac: str, encryption_key: str) -> str:
        # Layer 1: Decrypt dari ChaCha20-Poly1305
        image_base64 = decrypt_from_database(encrypted_content, encrypted_hmac)
        
        # Convert from base64 to bytes
        image_data = base64.b64decode(image_base64)
        
        # Layer 2: Extract message dari image (LSB + 3DES)
        return extract_message_from_image(image_data, encryption_key)
    
    @staticmethod
    def send_file(sender_id: str, receiver_id: str, file_bytes: bytes, 
                  filename: str, encryption_key: str) -> Tuple[bool, str]:
        try:
            # Layer 1: Enkripsi file dengan AES-256-GCM
            encrypted_aes = encrypt_file_aes_gcm(file_bytes, encryption_key)
            
            # Simpan filename dan encrypted content sebagai JSON
            file_data = {
                'filename': filename,
                'encrypted_content': encrypted_aes
            }
            
            file_json = json.dumps(file_data)
            
            # Layer 2: Enkripsi dengan ChaCha20-Poly1305 untuk database
            encrypted_db = encrypt_for_database(file_json)
            
            # Simpan ke database dengan message_type = 'file'
            message_data = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message_type': 'file',
                'encrypted_content': encrypted_db['encrypted'],
                'encrypted_hmac': encrypted_db['hmac']
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
