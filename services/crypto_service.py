import base64
import os
import hmac
import hashlib
from typing import Dict, Optional
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305, AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import bcrypt
from config.settings import Settings

# Load keys from environment variables
_HMAC_KEY = Settings.HMAC_SECRET_KEY.encode('utf-8')
_DATABASE_MASTER_KEY = Settings.DATABASE_MASTER_KEY
    
# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def _sha256_bytes(text: str) -> bytes:
    return hashlib.sha256(text.encode('utf-8')).digest()

def _bytes_equal(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)

# ============================================================================
# HMAC-SHA256 (DATABASE INTEGRITY)
# ============================================================================

def generate_hmac(data: str) -> str:
    if not data:
        raise ValueError('Data tidak boleh kosong')

    mac = hmac.new(
        _HMAC_KEY,
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return mac

def verify_hmac(data: str, hmac_value: str) -> bool:
    try:
        calculated = generate_hmac(data)
        return hmac.compare_digest(calculated, hmac_value)
    except:
        return False

# ============================================================================
# BCRYPT PASSWORD HASHING
# ============================================================================

def hash_password_bcrypt(password: str) -> str:
    if not password or len(password) < 6:
        raise ValueError('Password harus minimal 6 karakter')

    # Bcrypt dengan cost factor 12 (2^12 iterations)
    hashed = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(rounds=12)
    )
    return hashed.decode('utf-8')

def verify_password_bcrypt(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed.encode('utf-8')
        )
    except:
        return False

# ============================================================================
# CHACHA20-POLY1305 (FIELD-LEVEL ENCRYPTION)
# ============================================================================

def encrypt_field(plain_value: str) -> Dict[str, str]:
    if plain_value == '':
        return {'encrypted': '', 'hmac': ''}

    # Generate 256-bit key dari database master key
    key = _sha256_bytes(_DATABASE_MASTER_KEY)

    # ChaCha20-Poly1305 AEAD
    aead = ChaCha20Poly1305(key)

    # Generate random 96-bit nonce (12 bytes)
    nonce = os.urandom(12)

    # Encrypt (output = ciphertext + 16-byte tag)
    ciphertext = aead.encrypt(
        nonce,
        plain_value.encode('utf-8'),
        None  # no additional authenticated data
    )

    # Gabungkan: nonce + ciphertext + tag
    combined = nonce + ciphertext
    encrypted_b64 = base64.b64encode(combined).decode('utf-8')

    # Generate HMAC dari PLAINTEXT (untuk searching)
    hmac_value = generate_hmac(plain_value)

    return {
        'encrypted': encrypted_b64,
        'hmac': hmac_value
    }

def decrypt_field(encrypted_b64: str, hmac_value: str) -> str:
    if not encrypted_b64 or not hmac_value:
        return ''

    # Generate key
    key = _sha256_bytes(_DATABASE_MASTER_KEY)
    aead = ChaCha20Poly1305(key)

    # Decode Base64
    combined = base64.b64decode(encrypted_b64)

    if len(combined) < 12 + 16:
        raise ValueError('Format data terenkripsi tidak valid')

    # Extract nonce dan ciphertext+tag
    nonce = combined[:12]
    ciphertext = combined[12:]  # includes 16-byte tag

    # Decrypt (akan throw exception jika tag invalid)
    plaintext = aead.decrypt(nonce, ciphertext, None)

    return plaintext.decode('utf-8')

# ============================================================================
# CHACHA20-POLY1305 (DATABASE LAYER)
# ============================================================================

def encrypt_for_database(data: str) -> Dict[str, str]:
    if not data:
        raise ValueError('Data tidak boleh kosong')

    # Generate 256-bit key
    key = _sha256_bytes(_DATABASE_MASTER_KEY)
    chacha = ChaCha20Poly1305(key)

    # Generate random nonce (12 bytes untuk ChaCha20-Poly1305)
    nonce = os.urandom(12)

    # Encrypt
    ciphertext = chacha.encrypt(
        nonce,
        data.encode('utf-8'),
        None
    )

    # Gabungkan nonce + ciphertext (ciphertext sudah include tag)
    combined = nonce + ciphertext
    encrypted_b64 = base64.b64encode(combined).decode('utf-8')

    # Generate HMAC dari encrypted data (untuk integrity)
    hmac_value = generate_hmac(encrypted_b64)

    return {
        'encrypted': encrypted_b64,
        'hmac': hmac_value
    }

def decrypt_from_database(encrypted_b64: str, hmac_value: str) -> str:
    if not encrypted_b64 or not hmac_value:
        raise ValueError('Data terenkripsi dan HMAC tidak boleh kosong')

    # Verify HMAC first
    if not verify_hmac(encrypted_b64, hmac_value):
        raise Exception('Verifikasi HMAC gagal - data mungkin telah diubah')
    # Generate key
    key = _sha256_bytes(_DATABASE_MASTER_KEY)
    chacha = ChaCha20Poly1305(key)

    # Decode
    combined = base64.b64decode(encrypted_b64)

    if len(combined) < 12:
        raise ValueError('Data terenkripsi tidak valid')

    # Extract nonce dan ciphertext+tag
    nonce = combined[:12]
    ciphertext = combined[12:]

    # Decrypt
    plaintext = chacha.decrypt(nonce, ciphertext, None)

    return plaintext.decode('utf-8')

# ============================================================================
# AES-256-CTR + HMAC (TEXT MESSAGES)
# ============================================================================

def encrypt_text_aes_ctr_hmac(plain_text: str, user_key: str) -> str:
    if not plain_text:
        raise ValueError('Plaintext tidak boleh kosong')
    if not user_key:
        raise ValueError('Kunci enkripsi tidak boleh kosong')

    # Generate key dari user key (SHA-256 = 32 bytes untuk AES-256)
    key = _sha256_bytes(user_key)

    # Generate random IV (16 bytes untuk AES-CTR)
    iv = os.urandom(16)

    # AES-256-CTR cipher
    cipher = Cipher(
        algorithms.AES(key),
        modes.CTR(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()

    # Encrypt
    ciphertext = encryptor.update(plain_text.encode('utf-8')) + encryptor.finalize()

    # Gabungkan IV + ciphertext
    combined = iv + ciphertext
    encrypted_b64 = base64.b64encode(combined).decode('utf-8')

    # Generate HMAC-SHA256 untuk authentication
    hmac_value = generate_hmac(encrypted_b64)

    # Format: encrypted|hmac
    return f"{encrypted_b64}|{hmac_value}"

def decrypt_text_aes_ctr_hmac(encrypted_text: str, user_key: str) -> str:
    if not encrypted_text:
        raise ValueError('Teks terenkripsi tidak boleh kosong')
    if not user_key:
        raise ValueError('Kunci dekripsi tidak boleh kosong')

    # Split encrypted dan HMAC
    parts = encrypted_text.split('|')
    if len(parts) != 2:
        raise ValueError('Format teks terenkripsi tidak valid')

    encrypted_b64, hmac_value = parts

    # Verify HMAC first
    if not verify_hmac(encrypted_b64, hmac_value):
        raise Exception('Verifikasi HMAC gagal - data mungkin telah diubah')

    # Generate key
    key = _sha256_bytes(user_key)

    # Decode
    combined = base64.b64decode(encrypted_b64)

    if len(combined) < 16:
        raise ValueError('Data terenkripsi tidak valid')

    # Extract IV dan ciphertext
    iv = combined[:16]
    ciphertext = combined[16:]

    # AES-256-CTR cipher
    cipher = Cipher(
        algorithms.AES(key),
        modes.CTR(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()

    # Decrypt
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode('utf-8')

# ============================================================================
# 3DES ENCRYPTION (STEGANOGRAPHY)
# ============================================================================

def encrypt_3des(plaintext: str, encryption_key: str) -> str:
    # Generate 192-bit key untuk 3DES (24 bytes)
    key_bytes = hashlib.sha256(encryption_key.encode()).digest()[:24]
    
    # Generate random IV (8 bytes untuk DES/3DES)
    iv = os.urandom(8)
    
    # 3DES encryption dengan CBC mode
    cipher = Cipher(
        algorithms.TripleDES(key_bytes),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    # Padding untuk block cipher (8 bytes block size)
    plaintext_bytes = plaintext.encode('utf-8')
    padding_length = 8 - (len(plaintext_bytes) % 8)
    padded_plaintext = plaintext_bytes + bytes([padding_length] * padding_length)
    
    # Encrypt
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    
    # Generate HMAC untuk integrity
    h = hmac.new(key_bytes, iv + ciphertext, hashlib.sha256)
    hmac_tag = h.digest()
    
    # Format: IV(8) + Ciphertext + HMAC(32)
    encrypted_data = iv + ciphertext + hmac_tag
    
    return base64.b64encode(encrypted_data).decode('utf-8')


def decrypt_3des(encrypted_data: str, encryption_key: str) -> str:
    # Decode dari base64
    data = base64.b64decode(encrypted_data)
    
    # Parse components
    iv = data[:8]
    hmac_tag = data[-32:]
    ciphertext = data[8:-32]
    
    # Generate key
    key_bytes = hashlib.sha256(encryption_key.encode()).digest()[:24]
    
    # Verify HMAC
    h = hmac.new(key_bytes, iv + ciphertext, hashlib.sha256)
    expected_hmac = h.digest()
    
    if not _bytes_equal(hmac_tag, expected_hmac):
        raise ValueError("Pemeriksaan integritas 3DES gagal - kunci salah atau data rusak")
    
    # Decrypt
    cipher = Cipher(
        algorithms.TripleDES(key_bytes),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    padding_length = padded_plaintext[-1]
    plaintext = padded_plaintext[:-padding_length]
    
    return plaintext.decode('utf-8')


# ============================================================================
# TESTING/DEBUG FUNCTIONS
# ============================================================================

if __name__ == '__main__':
    # Test encrypt/decrypt field
    print("Testing bagian Enkripsi (ChaCha20-Poly1305)...")
    test_email = "test@example.com"
    encrypted = encrypt_field(test_email)
    print(f"Encrypted: {encrypted['encrypted'][:50]}...")
    print(f"HMAC: {encrypted['hmac']}")

    decrypted = decrypt_field(encrypted['encrypted'], encrypted['hmac'])
    print(f"Decrypted: {decrypted}")
    assert decrypted == test_email, "Tes enkripsi field gagal!"
    print("✅ Field enkripsi OK\n")

    # Test bcrypt
    print("Testing Bcrypt Password Hashing...")
    password = "MySecurePass123"
    hashed = hash_password_bcrypt(password)
    print(f"Hashed: {hashed}")

    is_valid = verify_password_bcrypt(password, hashed)
    print(f"Verification: {is_valid}")
    assert is_valid, "Bcrypt tes gagal!"
    print("✅ Bcrypt OK\n")

    # Test text message encryption
    print("Testing bagian Enkripsi Pesan Teks (AES-CTR-HMAC)...")
    message = "Hello, this is a secret message!"
    user_key = "MyEncryptionKey123"
    encrypted_msg = encrypt_text_aes_ctr_hmac(message, user_key)
    print(f"Encrypted: {encrypted_msg[:80]}...")

    decrypted_msg = decrypt_text_aes_ctr_hmac(encrypted_msg, user_key)
    print(f"Decrypted: {decrypted_msg}")
    assert decrypted_msg == message, "Tes enkripsi pesan teks gagal!"
    print("✅ Enkripsi pesan teks OK\n")

    print("Semua tes berhasil! ✅")


# ============================================================================
# STEGANOGRAPHY - LSB (LEAST SIGNIFICANT BIT)
# ============================================================================

def hide_message_in_image(image_bytes: bytes, message: str, encryption_key: str) -> bytes:
    from PIL import Image
    import io
    
    # Enkripsi pesan dengan 3DES
    encrypted_message = encrypt_3des(message, encryption_key)
    
    # Tambahkan delimiter untuk menandai akhir pesan
    data_to_hide = encrypted_message + "<<<END>>>"
    binary_message = ''.join(format(ord(char), '08b') for char in data_to_hide)
    
    # Load image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert ke RGB jika perlu
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    pixels = list(image.getdata())
    
    # Cek apakah gambar cukup besar untuk menyimpan pesan
    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Gambar terlalu kecil untuk menyembunyikan pesan")
    
    # Hide message in LSB
    new_pixels = []
    message_index = 0
    
    for pixel in pixels:
        if message_index < len(binary_message):
            # Modify each RGB channel
            r, g, b = pixel
            
            if message_index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            if message_index < len(binary_message):
                g = (g & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            if message_index < len(binary_message):
                b = (b & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            new_pixels.append((r, g, b))
        else:
            new_pixels.append(pixel)
    
    # Create new image
    stego_image = Image.new(image.mode, image.size)
    stego_image.putdata(new_pixels)
    
    # Save to bytes
    output = io.BytesIO()
    stego_image.save(output, format='PNG')
    return output.getvalue()


def extract_message_from_image(image_bytes: bytes, encryption_key: str) -> str:
    from PIL import Image
    import io
    
    # Load image
    image = Image.open(io.BytesIO(image_bytes))
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    pixels = list(image.getdata())
    
    # Extract binary message from LSB
    binary_message = ""
    
    for pixel in pixels:
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
    
    # Convert binary to string
    extracted_data = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            extracted_data += chr(int(byte, 2))
            
            # Check for end delimiter
            if extracted_data.endswith("<<<END>>>"):
                encrypted_message = extracted_data[:-9]  # Remove delimiter
                # Dekripsi pesan dengan 3DES
                try:
                    decrypted_message = decrypt_3des(encrypted_message, encryption_key)
                    return decrypted_message
                except Exception as e:
                    raise ValueError(f"Gagal mendekripsi pesan: {str(e)}")
    
    raise ValueError("Tidak ditemukan pesan tersembunyi atau kunci enkripsi salah")


# ============================================================================
# FILE ENCRYPTION (AES-256-GCM with User Key)
# ============================================================================

def encrypt_file_aes_gcm(file_bytes: bytes, encryption_key: str) -> str:
    # Generate 256-bit key dari user key
    key = _sha256_bytes(encryption_key)
    
    # Generate random nonce (12 bytes untuk GCM)
    nonce = os.urandom(12)
    
    # Encrypt dengan AES-256-GCM
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, file_bytes, None)
    
    # Format: nonce(12) + ciphertext+tag
    encrypted_data = nonce + ciphertext
    
    # Encode ke base64
    return base64.b64encode(encrypted_data).decode('utf-8')


def decrypt_file_aes_gcm(encrypted_data: str, encryption_key: str) -> bytes:
    # Decode dari base64
    data = base64.b64decode(encrypted_data)
    
    # Parse components
    nonce = data[:12]
    ciphertext = data[12:]
    
    # Generate key
    key = _sha256_bytes(encryption_key)
    
    # Decrypt
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    
    return plaintext


