# 🚀 Panduan Upload Project ke GitHub

Panduan lengkap dari NOL sampai project kamu online di GitHub.

---

## 📋 **CHECKLIST PERSIAPAN**

Sebelum mulai, pastikan:
- ✅ `.gitignore` sudah ada (untuk exclude `.env`, `.venv`, `__pycache__`)
- ✅ File `.env` berisi kredensial asli (JANGAN di-commit!)
- ✅ README.md sudah lengkap dan generic
- ✅ Project sudah berjalan dengan baik di lokal

---

## **BAGIAN 1: Install Git (Jika Belum Ada)**

### Step 1: Cek Apakah Git Sudah Terinstall

Buka **CMD** atau **PowerShell**, ketik:

```cmd
git --version
```

**Jika muncul** `git version 2.x.x` → Git sudah terinstall, lanjut ke **BAGIAN 2**.

**Jika muncul** `'git' is not recognized...` → Lanjut ke Step 2.

---

### Step 2: Download Git

1. Buka browser, kunjungi: **https://git-scm.com/download/win**
2. Download **64-bit Git for Windows Setup**
3. Jalankan installer
4. Pilih semua opsi default (Next → Next → Install)
5. Setelah selesai, **restart VS Code**

---

### Step 3: Konfigurasi Git (First Time Only)

Setelah install Git, buka terminal dan ketik:

```cmd
git config --global user.name "Nama Kamu"
git config --global user.email "email@kamu.com"
```

**Contoh:**
```cmd
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
```

---

## **BAGIAN 2: Buat Repository di GitHub**

### Step 1: Login ke GitHub

1. Buka browser, kunjungi: **https://github.com**
2. Login dengan akun kamu
3. Jika belum punya akun, klik **Sign Up** (gratis)

---

### Step 2: Buat Repository Baru

1. Klik tombol **"+"** di kanan atas
2. Pilih **"New repository"**
3. Isi form:
   - **Repository name**: `cryptomessenger` (atau nama lain yang kamu mau)
   - **Description**: `Aplikasi chat terenkripsi end-to-end dengan multiple algoritma kriptografi`
   - **Visibility**: 
     - ✅ **Public** (jika mau jadi portfolio)
     - ✅ **Private** (jika hanya untuk tugas/pribadi)
   - ❌ **JANGAN centang** "Add a README file" (kita sudah punya README.md)
   - ❌ **JANGAN centang** "Add .gitignore" (kita sudah punya .gitignore)
   - ❌ **JANGAN pilih** license (bisa ditambah nanti)
4. Klik **"Create repository"**

---

### Step 3: Salin URL Repository

Setelah repository dibuat, GitHub akan tunjukkan halaman setup. 

**SALIN URL** yang muncul di bagian "Quick setup", contoh:
```
https://github.com/username/cryptomessenger.git
```

**Simpan URL ini**, kita akan pakai nanti!

---

## **BAGIAN 3: Upload Project dari VS Code**

### Step 1: Buka Terminal di VS Code

1. Buka project `appkripto` di VS Code
2. Tekan **Ctrl + `** (backtick) untuk buka terminal
3. Pastikan terminal ada di folder project (bukan di `.venv`)

**Cek path terminal:**
```cmd
cd
```

Harus muncul path: `d:\KULIAH\Semester 5\...\appkripto`

---

### Step 2: Initialize Git Repository

Di terminal, ketik:

```cmd
git init
```

**Output:** `Initialized empty Git repository in ...`

---

### Step 3: Hubungkan dengan GitHub

Ganti `[URL-REPOSITORY-KAMU]` dengan URL yang kamu salin tadi:

```cmd
git remote add origin [URL-REPOSITORY-KAMU]
```

**Contoh:**
```cmd
git remote add origin https://github.com/johndoe/cryptomessenger.git
```

**Verifikasi koneksi:**
```cmd
git remote -v
```

Harus muncul:
```
origin  https://github.com/username/cryptomessenger.git (fetch)
origin  https://github.com/username/cryptomessenger.git (push)
```

---

### Step 4: Tambahkan File ke Git

**PENTING:** Sebelum `git add`, cek file `.env` JANGAN ter-commit!

```cmd
git status
```

Pastikan **TIDAK ADA** file `.env` atau `.venv/` di list!

**Jika aman, tambahkan semua file:**

```cmd
git add .
```

**Cek lagi file yang akan di-commit:**

```cmd
git status
```

Harus muncul banyak file dengan status `new file:` (warna hijau).

---

### Step 5: Commit Perubahan

```cmd
git commit -m "Initial commit: CryptoMessenger with 5 encryption algorithms"
```

**Output:** `XX files changed, XXX insertions(+)`

---

### Step 6: Rename Branch ke `main` (Opsional tapi Recommended)

GitHub sekarang pakai `main` sebagai default branch (bukan `master`).

```cmd
git branch -M main
```

---

### Step 7: Push ke GitHub (UPLOAD!)

Ini step terakhir untuk upload!

```cmd
git push -u origin main
```

**GitHub akan minta login:**

#### **PENTING: Cara Login di 2025**

❌ **JANGAN pakai password biasa** (sudah deprecated sejak 2021)  
✅ **Harus pakai Personal Access Token (PAT)**

---

## **BAGIAN 4: Buat Personal Access Token**

### Step 1: Buka GitHub Settings

1. Login ke **GitHub.com**
2. Klik **foto profil** (kanan atas) → **Settings**
3. Scroll ke bawah, klik **Developer settings** (paling bawah sidebar kiri)
4. Klik **Personal access tokens** → **Tokens (classic)**
5. Klik **"Generate new token"** → **"Generate new token (classic)"**

---

### Step 2: Konfigurasi Token

1. **Note**: `CryptoMessenger Upload` (untuk mengingatkan fungsinya)
2. **Expiration**: `90 days` (atau pilih `No expiration` jika mau permanent)
3. **Select scopes**: Centang **`repo`** (full control of private repositories)
4. Scroll ke bawah, klik **"Generate token"**

---

### Step 3: Salin Token

⚠️ **SUPER PENTING**: Token hanya muncul **SEKALI**!

Token akan muncul seperti ini:
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**SALIN TOKEN INI** dan simpan di tempat aman (Notepad, password manager, dll).

---

### Step 4: Gunakan Token untuk Push

Kembali ke VS Code terminal, jalankan lagi:

```cmd
git push -u origin main
```

**Ketika muncul popup login:**
- **Username**: `username-github-kamu`
- **Password**: `paste-token-yang-kamu-salin` (bukan password asli!)

Atau jika pakai **Windows Credential Manager**, token akan tersimpan otomatis.

---

### Step 5: Tunggu Upload Selesai

Terminal akan menunjukkan progress:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX.XX KiB | XX.XX MiB/s, done.
Total XX (delta X), reused 0 (delta 0), pack-reused 0
To https://github.com/username/cryptomessenger.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**SELAMAT! Project sudah terupload ke GitHub! 🎉**

---

## **BAGIAN 5: Verifikasi di GitHub**

### Step 1: Buka Repository di Browser

Kunjungi: `https://github.com/[username]/cryptomessenger`

### Step 2: Cek File yang Terupload

Pastikan:
- ✅ File `README.md` muncul dan ter-render di homepage
- ✅ Folder `config/`, `models/`, `services/`, `ui/`, `docs/` ada
- ✅ File `app.py`, `requirements.txt` ada
- ❌ File `.env` **TIDAK ADA** (harus ter-exclude)
- ❌ Folder `.venv/` **TIDAK ADA** (harus ter-exclude)

### Step 3: Cek README Tampilan

Scroll di halaman repository, README.md akan otomatis ter-render.

Cek apakah:
- ✅ Markdown formatting benar (header, code blocks, table)
- ✅ Emoji muncul dengan baik
- ✅ Struktur jelas dan rapi

---

## **BONUS: Perintah Git yang Sering Dipakai**

Setelah upload pertama, jika kamu edit code dan mau update di GitHub:

```cmd
# 1. Cek file yang berubah
git status

# 2. Tambahkan file yang berubah
git add .

# 3. Commit dengan pesan
git commit -m "Update: Perbaiki bug di chat encryption"

# 4. Push ke GitHub
git push
```

**Sesederhana itu!** Tidak perlu `-u origin main` lagi setelah push pertama.

---

## **TROUBLESHOOTING**

### ❌ Error: "git is not recognized..."

**Solusi:**
1. Install Git dari https://git-scm.com/download/win
2. Restart VS Code
3. Coba lagi

---

### ❌ Error: "Support for password authentication was removed..."

**Solusi:**
- Jangan pakai password biasa
- Pakai **Personal Access Token** (lihat **BAGIAN 4**)

---

### ❌ Error: "Permission denied (publickey)"

**Solusi:**
- Pakai HTTPS, bukan SSH
- URL harus: `https://github.com/...` (bukan `git@github.com:...`)

---

### ❌ Error: "File .env was committed by mistake"

**Solusi untuk remove file sensitif:**

```cmd
# Remove dari Git history
git rm --cached .env

# Commit
git commit -m "Remove sensitive .env file"

# Push
git push
```

**Pastikan `.gitignore` sudah ada `.env` agar tidak ter-commit lagi!**

---

### ❌ Error: "Large file detected (.venv/)"

**Solusi:**

1. Pastikan `.gitignore` ada `.venv/`
2. Remove dari staging:
   ```cmd
   git rm -r --cached .venv/
   git commit -m "Remove .venv from Git"
   git push
   ```

---

## **TIPS PRO**

### 1. **Tambah Badge di README.md**

Edit `README.md`, tambah di bagian paling atas:

```markdown
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
```

### 2. **Tambah Screenshot**

1. Buat folder `screenshots/` di root project
2. Tambahkan screenshot aplikasi (login page, chat page)
3. Edit README.md:
   ```markdown
   ## 📸 Screenshots
   
   ![Login Page](screenshots/login.png)
   ![Chat Interface](screenshots/chat.png)
   ```

### 3. **Tambah License**

Buat file `LICENSE` di root project:

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[... rest of MIT license text]
```

### 4. **Set Repository Topics**

Di GitHub repository page:
1. Klik **⚙️ Settings** (di repo, bukan account)
2. Scroll ke **Topics**
3. Tambahkan: `cryptography`, `encryption`, `streamlit`, `python`, `aes`, `chacha20`, `steganography`

---

## **SELESAI! 🎉**

Sekarang project kamu sudah online di GitHub!

**Link yang bisa kamu share:**
```
https://github.com/[username]/cryptomessenger
```

**Untuk teman yang mau clone:**
```cmd
git clone https://github.com/[username]/cryptomessenger.git
cd cryptomessenger
```

Lalu ikuti instruksi di `README.md` untuk setup virtual environment dan install dependencies.

---

**Semoga berhasil! Good luck! 🚀**
