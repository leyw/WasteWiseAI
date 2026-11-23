# WasteWise AI

Aplikasi web berbasis AI untuk membantu masyarakat Indonesia mengenali jenis sampah dari foto, memahami karakteristiknya, dan mendapatkan rekomendasi pengelolaan atau daur ulang yang tepat.

---

## Fitur Utama

| Fitur | Deskripsi |
|---|---|
| **Dashboard** | Ringkasan total analisis, kategori terbanyak, dan aktivitas terbaru |
| **Analisis Sampah** | Upload gambar, identifikasi jenis sampah via AI, tampilkan hasil dan rekomendasi |
| **Riwayat Analisis** | Lihat, filter, dan hapus riwayat analisis sebelumnya |
| **Statistik** | Grafik distribusi kategori sampah (bar chart + pie chart) |
| **Panduan** | Konten panduan pengelolaan 7 kategori sampah dari database |
| **Auth** | Register dan login dengan JWT |

---

## Teknologi

### Backend
- Python 3.10+
- FastAPI + Uvicorn
- SQLAlchemy + SQLite
- Passlib (bcrypt) + python-jose (JWT)
- Pillow (validasi gambar)

### Frontend
- React 18 + Vite
- Tailwind CSS
- React Router DOM v6
- Axios
- Recharts (grafik)
- Lucide React (ikon)

### AI Integration
- Abstraksi service layer — mudah diganti provider
- Mode **mock** aktif secara default (tidak memerlukan API key)
- Siap untuk **Google Gemini** dan **OpenAI GPT-4o** (tinggal set `.env`)

---

## Struktur Folder

```
WasteWaiseAI/
├── backend/
│   ├── main.py              ← Entry point FastAPI
│   ├── requirements.txt
│   ├── .env.example
│   ├── uploads/             ← Gambar yang diupload (auto-created)
│   ├── wastewise.db         ← SQLite database (auto-created)
│   ├── core/
│   │   ├── config.py        ← Settings dari .env
│   │   ├── database.py      ← SQLAlchemy engine & session
│   │   └── security.py      ← JWT + bcrypt helpers
│   ├── models/              ← ORM: User, Analysis, Guide
│   ├── schemas/             ← Pydantic schemas
│   ├── routers/             ← auth, analyze, history, statistics, guides, health
│   └── services/
│       ├── ai_service.py    ← AI abstraction layer (mock + Gemini + OpenAI)
│       └── seed_guides.py   ← Data panduan awal
└── frontend/
    ├── vite.config.js       ← Proxy /api ke backend
    ├── tailwind.config.js
    └── src/
        ├── App.jsx           ← Router + protected routes
        ├── api/client.js     ← Axios + JWT interceptor
        ├── context/AuthContext.jsx
        ├── components/
        │   ├── layout/      ← Sidebar, Navbar, Layout
        │   └── ui/          ← Card, Badge, LoadingSpinner, ErrorMessage
        └── pages/           ← Dashboard, Analyze, History, Statistics, Guides, Auth
```

---

## Instalasi & Menjalankan

### Prasyarat
- Python 3.10+
- Node.js 18+
- npm

---

### 1. Clone / Unduh Proyek

```bash
# Masuk ke folder proyek
cd WasteWaiseAI
```

---

### 2. Setup Backend

```bash
cd backend

# Buat virtual environment (opsional tapi direkomendasikan)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependency
pip install -r requirements.txt

# Buat file .env dari contoh
copy .env.example .env     # Windows
# cp .env.example .env      # Linux/macOS
```

Edit file `backend/.env` sesuai kebutuhan (lihat bagian Konfigurasi API Key di bawah).

```bash
# Jalankan backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend berjalan di: **http://localhost:8000**
Dokumentasi API: **http://localhost:8000/api/docs**

> Database SQLite dan data panduan awal dibuat otomatis saat pertama kali dijalankan.

---

### 3. Setup Frontend

Buka terminal baru:

```bash
cd frontend

# Install dependency
npm install

# Jalankan frontend
npm run dev
```

Frontend berjalan di: **http://localhost:5173**

---

## Konfigurasi API Key

File `backend/.env`:

```env
# Keamanan JWT — ganti dengan nilai acak yang kuat
# Generate: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=changeme-generate-a-strong-random-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
DATABASE_URL=sqlite:///./wastewise.db

# AI Provider
# Pilihan: mock | gemini | openai
AI_PROVIDER=mock
AI_API_KEY=

# Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE_MB=5
```

### Mengaktifkan Google Gemini Vision

1. Dapatkan API key dari [Google AI Studio](https://aistudio.google.com/)
2. Install library tambahan:
   ```bash
   pip install google-generativeai
   ```
3. Set di `backend/.env`:
   ```env
   AI_PROVIDER=gemini
   AI_API_KEY=AIza...your_key_here
   ```
4. Restart backend — tidak ada perubahan kode lain yang diperlukan.

### Mengaktifkan OpenAI GPT-4o Vision

1. Dapatkan API key dari [OpenAI Platform](https://platform.openai.com/)
2. Install library tambahan:
   ```bash
   pip install openai
   ```
3. Set di `backend/.env`:
   ```env
   AI_PROVIDER=openai
   AI_API_KEY=sk-...your_key_here
   ```
4. Restart backend.

> **Catatan:** Jika `AI_PROVIDER=mock` atau `AI_API_KEY` kosong, semua hasil analisis menggunakan data contoh dan ditandai dengan badge **"Hasil Mock"**. Ini bukan hasil klasifikasi AI nyata.

---

## Contoh Penggunaan

### Alur Dasar

1. Buka **http://localhost:5173/register** → daftar akun
2. Login dengan akun yang baru dibuat
3. Di halaman **Analisis Sampah** → upload foto sampah
4. Klik **Analisis Sampah** → tunggu hasil
5. Lihat hasil identifikasi (nama, kategori, material) dan rekomendasi
6. Buka **Riwayat** untuk melihat semua analisis sebelumnya
7. Buka **Statistik** untuk melihat grafik distribusi kategori
8. Buka **Panduan** untuk membaca cara pengelolaan per kategori

### Format Gambar yang Didukung
- JPG / JPEG
- PNG
- WEBP
- Ukuran maksimal: **5 MB**

### Kategori Sampah
| Kategori | Keterangan |
|---|---|
| Organik | Sisa makanan, daun, bahan biodegradable |
| Plastik | Botol, kantong, kemasan plastik |
| Kertas | Kardus, koran, kertas HVS |
| Logam | Kaleng aluminium, besi, tembaga |
| Kaca | Botol kaca, toples |
| Elektronik | Ponsel, charger, perangkat elektronik |
| B3 | Baterai, cat, pestisida, obat kadaluwarsa |
| Lainnya | Kategori yang tidak teridentifikasi |

---

## Endpoint API

| Method | Path | Auth | Deskripsi |
|---|---|---|---|
| GET | `/api/health` | ✗ | Status backend |
| POST | `/api/auth/register` | ✗ | Daftar akun |
| POST | `/api/auth/login` | ✗ | Login, terima JWT |
| GET | `/api/auth/me` | ✓ | Profil pengguna aktif |
| POST | `/api/analyze` | ✓ | Upload gambar & analisis |
| GET | `/api/history` | ✓ | Daftar riwayat (filter: `?category=`) |
| GET | `/api/history/{id}` | ✓ | Detail riwayat |
| DELETE | `/api/history/{id}` | ✓ | Hapus riwayat |
| GET | `/api/statistics` | ✓ | Statistik analisis |
| GET | `/api/guides` | ✗ | Daftar panduan |
| GET | `/api/guides/{id}` | ✗ | Detail panduan |
| POST | `/api/guides` | ✓ | Tambah panduan |
| PUT | `/api/guides/{id}` | ✓ | Update panduan |
| DELETE | `/api/guides/{id}` | ✓ | Hapus panduan |

---

## Lisensi

Proyek ini dibuat untuk keperluan capstone individu. Bebas digunakan dan dimodifikasi untuk keperluan pendidikan.
