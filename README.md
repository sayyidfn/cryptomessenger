# CryptoMessenger

Aplikasi chat terenkripsi end-to-end dengan arsitektur modular yang aman dan mudah dipahami.

## 🚀 Fitur

- ✅ Register & Login dengan Bcrypt password hashing (cost 12)
- ✅ Enkripsi end-to-end untuk pesan teks (AES-256-CTR + HMAC-SHA256)
- ✅ **Steganografi**: Sembunyikan pesan terenkripsi di dalam gambar (LSB + 3DES-CBC)
- ✅ **File Transfer**: Enkripsi file dengan AES-256-GCM
- ✅ Arsitektur modular dengan separation of concerns
- ✅ Multiple algoritma kriptografi modern dan aman
- ✅ ChaCha20-Poly1305 + HMAC-SHA256 untuk database layer
- ✅ Caching mechanism untuk performa optimal (50x lebih cepat)
- ✅ UI modern dengan dark theme dan blue accents

## 📋 Prasyarat

- Python 3.8 atau lebih tinggi
- pip (Python package installer)
- Akses ke database Supabase

## 🛠️ Instalasi

### 1. Buka Project di VS Code

Ekstrak project dan buka folder `appkripto` di VS Code.

### 2. Buat Virtual Environment

```cmd
python -m venv .venv
```

### 3. Aktifkan Virtual Environment

**Windows (cmd.exe):**

```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Upgrade pip

```cmd
python -m pip install --upgrade pip
```

### 5. Install Dependencies

```cmd
pip install -r requirements.txt
```

**Catatan**: Jika terjadi error "path too long", pindahkan folder ke path yang lebih pendek (contoh: `D:\Kripto\`)

### 6. Konfigurasi Environment Variables

File `.env` sudah dibuat dengan konfigurasi default. Pastikan kredensial Supabase sudah benar.

**⚠️ PENTING:** Jangan commit file `.env` ke Git!

## ▶️ Menjalankan Aplikasi

### Cara 1: Manual di Terminal (Recommended)

**Windows CMD:**

```cmd
.venv\Scripts\activate
streamlit run app.py
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
streamlit run app.py
```

### Cara 2: Menggunakan Script

```cmd
run_new.bat
```

### Cara 3: Custom Port

```cmd
streamlit run app.py --server.port 8502
```

### Cara 4: Network Access

```cmd
streamlit run app.py --server.address 0.0.0.0
```

Aplikasi akan terbuka di browser pada: `http://localhost:8501`

## 🧪 Testing

### Test Koneksi Database

```cmd
python -c "from supabase_client import supabase; print(supabase.from_('users').select('id').limit(1).execute())"
```

### Test Kriptografi

```cmd
python crypto_helper.py
```

## 📚 Struktur Proyek

```
appkripto/
├── app.py                          # 🚀 Entry point (NEW)
├── main_old.py                     # 📦 Legacy backup
├── requirements.txt                # 📦 Dependencies
├── .env                           # 🔐 Environment variables
│
├── config/                        # ⚙️ Configuration
│   ├── __init__.py
│   └── settings.py               # Constants & env config
│
├── models/                        # 📊 Business Logic
│   ├── __init__.py
│   ├── user.py                   # User operations
│   └── message.py                # Message operations
│
├── services/                      # 🔧 External Services
│   ├── __init__.py
│   ├── database_service.py       # Supabase client
│   └── crypto_service.py         # All crypto functions
│
├── ui/                           # 🎨 User Interface
│   ├── __init__.py
│   ├── pages.py                  # Login, Register, Chat
│   ├── components.py             # Reusable UI components
│   └── styles.py                 # CSS styling
│
└── docs/                         # 📖 Documentation
    ├── STRUKTUR_PROYEK.md       # Project structure
    ├── ARSITEKTUR.md            # Architecture diagrams
    └── RESTRUKTURISASI.md       # Migration guide
```

### Arsitektur Modular

Project ini menggunakan **Separation of Concerns**:

- **Config Layer**: Environment variables & constants
- **Service Layer**: Database & cryptography operations
- **Model Layer**: Business logic (User, Message)
- **UI Layer**: Streamlit pages & components

Lihat dokumentasi lengkap di folder `docs/` untuk penjelasan detail.

## 🔐 Algoritma Kriptografi

### Algoritma yang Digunakan (Final)

| No  | Segmen                  | Algoritma Utama                  | Algoritma Pendukung | Use Case                            |
| --- | ----------------------- | -------------------------------- | ------------------- | ----------------------------------- |
| 1   | **Register/Login**      | **Bcrypt** (cost factor 12)      | -                   | Password hashing dengan salt        |
| 2   | **Database Layer**      | **ChaCha20-Poly1305** (RFC 7539) | HMAC-SHA256         | Enkripsi semua field di database    |
| 3   | **Pesan Teks**          | **AES-256-CTR**                  | HMAC-SHA256         | End-to-end text messaging           |
| 4   | **File Encryption**     | **AES-256-GCM**                  | -                   | Authenticated encryption untuk file |
| 5   | **Image Steganography** | **LSB + 3DES-CBC**               | HMAC-SHA256         | Hide & encrypt messages in images   |

### Detail Implementasi:

**1. Bcrypt (Password Hashing)**

- **Cost Factor**: 12 (2^12 = 4096 iterations)
- **Use Case**: Hash password saat register dan verifikasi saat login
- **Keunggulan**: Slow hashing, built-in salt, protection against rainbow tables
- **File**: `services/crypto_service.py`

**2. ChaCha20-Poly1305 + HMAC (Database Layer)**

- **Algorithm**: ChaCha20-Poly1305 (RFC 7539) - AEAD
- **Key Size**: 256-bit (derived dari DATABASE_MASTER_KEY)
- **Nonce**: 96-bit (random)
- **Use Case**: Enkripsi semua data sensitif di database (email, username, password, messages)
- **Keunggulan**: AEAD dengan built-in authentication + HMAC terpisah untuk integrity verification dan searchable encryption. Lebih cepat dari AES pada platform tanpa hardware acceleration
- **File**: `services/crypto_service.py`

**3. AES-256-CTR + HMAC-SHA256 (Text Messages)**

- **Mode**: CTR (Counter Mode)
- **Key Size**: 256-bit
- **IV**: 128-bit (random)
- **Use Case**: Enkripsi pesan teks end-to-end
- **Keunggulan**: Standard NIST, parallelizable, HMAC authentication
- **File**: `services/crypto_service.py`

**4. AES-256-GCM (File Encryption)**

- **AES Mode**: GCM (Galois/Counter Mode) - AEAD
- **Key Size**: 256-bit (derived dari user key)
- **Nonce**: 96-bit (random)
- **Use Case**: Enkripsi file dengan authenticated encryption
- **Keunggulan**: Built-in authentication, tidak perlu HMAC terpisah
- **File**: `services/crypto_service.py`

**5. LSB + 3DES-CBC (Steganography)**

- **Method**: Least Significant Bit manipulation
- **Encryption**: 3DES-CBC (192-bit key)
- **IV**: 64-bit (random)
- **Authentication**: HMAC-SHA256
- **Use Case**: Menyembunyikan pesan terenkripsi di dalam gambar
- **Support**: PNG, JPEG
- **File**: `services/crypto_service.py`

## 📖 Cara Menggunakan

### Register

1. Klik tombol "Register"
2. Masukkan email, username, dan password
3. Password akan di-hash dengan Bcrypt (cost 12)
4. Klik "Register"
5. Login dengan akun yang baru dibuat

### Login

1. Masukkan email dan password
2. Klik "Login"

### Chat - Pesan Teks

1. Setelah login, pilih user dari sidebar
2. **Masukkan kunci enkripsi** di form (contoh: "mykey123")
3. Di tab "✉️ Text Message", tulis pesan dan klik "Send Encrypted Message 🔒"
4. Pesan akan terenkripsi dengan AES-256-CTR + HMAC dan tersimpan di database
5. **Bagikan kunci enkripsi secara terpisah** ke penerima untuk decrypt

### Chat - Steganografi (Gambar + Pesan Tersembunyi)

1. Pilih user dari sidebar
2. Klik tab "🖼️ Image + Steganography"
3. Masukkan kunci enkripsi
4. Upload gambar (PNG/JPG)
5. Masukkan pesan yang ingin disembunyikan di dalam gambar
6. Klik "Send Image with Hidden Message 🔐"
7. Penerima bisa melihat gambar dan klik "🔓 Extract Hidden Message" untuk membaca pesan tersembunyi

### Chat - File Transfer

1. Pilih user dari sidebar
2. Klik tab "📎 File"
3. **Masukkan kunci enkripsi** untuk file (contoh: "filekey456")
4. Upload file yang ingin dikirim (maks 200MB)
5. Klik "Send Encrypted File 🔒"
6. File akan dienkripsi dengan AES-256-GCM dan dikirim
7. **Bagikan kunci enkripsi secara terpisah** ke penerima untuk decrypt

### Dekripsi Pesan (Penerima)

**Text Messages:**

1. Klik expander "🔓 Decrypt Message" pada pesan terenkripsi
2. Masukkan kunci enkripsi yang **sama** dengan yang digunakan saat mengirim
3. Klik "Decrypt"
4. Pesan teks akan terdekripsi dengan AES-256-CTR + HMAC
5. Jika kunci salah, akan muncul pesan error

**Steganography:**

1. Klik expander "🔓 Extract Hidden Message" pada gambar
2. Masukkan kunci enkripsi yang sama dengan saat mengirim
3. Klik "Extract Message"
4. Sistem akan extract & dekripsi pesan dengan LSB + 3DES-CBC
5. Kunci harus sama dengan saat mengirim

**File Transfer:**

1. Klik expander "🔓 Decrypt & Download File"
2. Masukkan kunci enkripsi yang sama dengan saat mengirim
3. Klik "Decrypt & Download"
4. File akan didekripsi dengan AES-256-GCM
5. Klik "💾 Save [filename]" untuk download file original

## ⚠️ Catatan Penting

### Keamanan

**✅ Yang Dilakukan:**

- ✅ Password di-hash dengan Bcrypt (cost 12)
- ✅ Data sensitif di-enkripsi di database (ChaCha20-Poly1305)
- ✅ Double encryption layer: Database layer (ChaCha20) + End-to-end encryption (AES/3DES)
- ✅ HMAC untuk integrity verification
- ✅ Encryption key dari environment variable
- ✅ No hardcoded secrets
- ✅ Authenticated encryption (ChaCha20-Poly1305 untuk database, AES-GCM untuk file)
- ✅ Random nonce/IV untuk setiap operasi
- ✅ Session-based caching untuk performa optimal

**⚠️ Yang Harus Diperhatikan:**

- ⚠️ Simpan `.env` dengan aman (jangan commit ke Git!)
- ⚠️ Gunakan HTTPS untuk production
- ⚠️ Backup encryption keys
- ⚠️ Rotasi keys secara berkala
- ⚠️ User harus ingat encryption key untuk decrypt message
- ⚠️ Gunakan password yang kuat (minimal 6 karakter)

### Environment Variables

File `.env` harus berisi:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ENCRYPTION_KEY_DB=your_32_char_encryption_key_here
HMAC_KEY=your_32_char_hmac_key_here___
```

## 🐛 Troubleshooting

### Error: "Module not found"

```cmd
pip install -r requirements.txt
```

### Error: "SUPABASE_URL not set"

Pastikan file `.env` ada dan berisi kredensial yang benar.

### Error: "HMAC verification failed"

Pastikan keys di `.env` sama dengan yang digunakan di Flutter.

### Pesan tidak bisa didekripsi

1. Pastikan kunci enkripsi yang digunakan **sama persis**
2. Kunci enkripsi bersifat case-sensitive
3. Coba gunakan kunci yang sama dengan saat mengirim pesan

## 🛠️ Development

### Running Tests

```cmd
# TODO: Add test suite
pytest tests/
```

### Code Structure

```python
# Clean separation of concerns
UI Layer → Model Layer → Service Layer

# Example flow:
LoginPage.render()
    ↓
User.login(email, password)
    ↓
├─ crypto_service.verify_password()
└─ database_service.query()
```

### Adding New Features

**1. New Crypto Algorithm:**

```python
# services/crypto_service.py
def encrypt_with_new_algo(data, key):
    # Implementation
    pass
```

**2. New Message Type:**

```python
# models/message.py
@staticmethod
def send_new_type(sender_id, receiver_id, data, key):
    # Implementation
    pass
```

**3. New UI Component:**

```python
# ui/components.py
class NewComponent:
    def render(self):
        # Streamlit UI
        pass
```
## 👥 Team

- Sayyid Fakhri Nurjundi (123230172)
- Saif Ali Addamawi (123230169)

## 📄 Lisensi

Project ini untuk keperluan tugas akhir Kriptografi IF-A.

**⚡ Developed with modern cryptography best practices**
**🔐 Secure by design, easy to understand**
