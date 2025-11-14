import uuid
from datetime import datetime
from typing import Tuple, List, Dict
from services.database_service import db
from services.crypto_service import (
    encrypt_field, decrypt_field, generate_hmac,
    hash_password_bcrypt, verify_password_bcrypt,
    encrypt_for_database, decrypt_from_database
)


class User:
    @staticmethod
    def register(email: str, username: str, password: str) -> Tuple[bool, str]:
        try:
            # Validasi input
            if not all([email, username, password]):
                raise ValueError('Semua field harus diisi')
            
            if len(password) < 6:
                raise ValueError('Password harus minimal 6 karakter')
            
            # Check apakah email sudah terdaftar
            email_hmac_check = generate_hmac(email)
            existing = db.from_('users').select('id').eq('email_hmac', email_hmac_check).execute()
            
            if existing.data:
                raise Exception('Email sudah terdaftar')
            
            # Enkripsi data
            email_enc = encrypt_field(email)
            username_enc = encrypt_field(username)
            
            # Password: Hash dengan Bcrypt, lalu enkripsi hash-nya
            password_bcrypt = hash_password_bcrypt(password)
            password_db = encrypt_for_database(password_bcrypt)
            
            # Generate user ID
            user_id = str(uuid.uuid4())
            
            # Prepare data untuk insert
            user_data = {
                'id': user_id,
                'email': email_enc['encrypted'],
                'email_hmac': email_enc['hmac'],
                'username': username_enc['encrypted'],
                'username_hmac': username_enc['hmac'],
                'password_hash': password_db['encrypted'],
                'password_hmac': password_db['hmac'],
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Insert ke database
            response = db.from_('users').insert(user_data).execute()
            
            if not response.data:
                raise Exception('Gagal membuat user')
            
            return True, "Registrasi berhasil! Silakan login."
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, any]:
        try:
            # Cari user by email HMAC
            email_hmac_check = generate_hmac(email)
            response = db.from_('users').select('*').eq('email_hmac', email_hmac_check).execute()
            
            if not response.data:
                raise Exception('Email atau password salah')
            
            user_row = response.data[0]
            
            # Dekripsi password hash dari database
            encrypted_password = user_row['password_hash']
            password_hmac = user_row['password_hmac']
            stored_hash = decrypt_from_database(encrypted_password, password_hmac)
            
            # Verify password dengan Bcrypt
            if not verify_password_bcrypt(password, stored_hash):
                raise Exception('Email atau password salah')
            
            # Dekripsi data user
            decrypted_email = decrypt_field(
                user_row['email'],
                user_row['email_hmac']
            )
            
            decrypted_username = decrypt_field(
                user_row['username'],
                user_row['username_hmac']
            )
            
            # Return user data
            user_data = {
                'id': user_row['id'],
                'email': decrypted_email,
                'username': decrypted_username,
                'rsa_public_key': user_row.get('rsa_public_key', ''),
                'encrypted_rsa_private_key': user_row.get('encrypted_rsa_private_key', ''),
                'created_at': user_row['created_at']
            }
            
            return True, user_data
            
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_all() -> List[Dict]:
        try:
            response = db.from_('users').select('*').execute()
            
            if not response.data:
                return []
            
            users = []
            for user_row in response.data:
                try:
                    decrypted_email = decrypt_field(
                        user_row['email'],
                        user_row['email_hmac']
                    )
                    
                    decrypted_username = decrypt_field(
                        user_row['username'],
                        user_row['username_hmac']
                    )
                    
                    users.append({
                        'id': user_row['id'],
                        'username': decrypted_username,
                        'email': decrypted_email
                    })
                except:
                    continue
            
            return users
            
        except:
            return []
