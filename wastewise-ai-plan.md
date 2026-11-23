# WasteWise AI — Project Plan

## Top-Level Overview

WasteWise AI adalah aplikasi web MVP yang membantu masyarakat Indonesia mengidentifikasi jenis sampah dari foto, memahami karakteristiknya, dan mendapatkan rekomendasi pengelolaan atau daur ulang. Seluruh konten UI menggunakan Bahasa Indonesia.

**Stack:**
- Frontend: React.js + Vite + Tailwind CSS (JavaScript)
- Backend: Python + FastAPI + SQLite
- AI Integration: Abstracted service layer dengan mock/fallback (API Vision menyusul)
- Auth: JWT sederhana (login/register)
- Image storage: file lokal di `backend/uploads/`, path di database

**Scope MVP:**
1. Auth (login/register)
2. Dashboard
3. Upload & Analisis Gambar
4. Klasifikasi & Rekomendasi AI (mock dulu)
5. Riwayat Analisis
6. Statistik
7. Panduan Pengelolaan Sampah (konten dari database)

---

## Arsitektur Sistem

```
[Browser]
    │
    ▼
[React Frontend :5173]
    │  REST (JSON + multipart/form-data)
    ▼
[FastAPI Backend :8000]
    ├── /api/auth        ← register, login, me
    ├── /api/analyze     ← upload gambar → AI service → simpan
    ├── /api/history     ← daftar & detail riwayat
    ├── /api/statistics  ← statistik agregat
    ├── /api/guides      ← CRUD panduan (konten dari DB)
    └── /api/health      ← health check
         │
         ├── [AI Service Layer]  ← abstraksi (mock → real API nanti)
         ├── [SQLite via SQLAlchemy]
         └── [uploads/ folder]  ← file gambar
```

---

## Struktur Folder

```
WasteWaiseAI/
├── wastewise-ai-plan.md
├── README.md
│
├── backend/
│   ├── main.py                  ← entry point FastAPI
│   ├── requirements.txt
│   ├── .env                     ← AI_API_KEY, SECRET_KEY, dll
│   ├── .env.example
│   ├── uploads/                 ← gambar yang diupload
│   ├── wastewise.db             ← SQLite database
│   │
│   ├── core/
│   │   ├── config.py            ← settings dari .env
│   │   ├── database.py          ← SQLAlchemy engine & session
│   │   └── security.py          ← JWT helpers
│   │
│   ├── models/
│   │   ├── user.py              ← ORM model User
│   │   ├── analysis.py          ← ORM model Analysis
│   │   └── guide.py             ← ORM model Guide
│   │
│   ├── schemas/
│   │   ├── user.py              ← Pydantic schemas User
│   │   ├── analysis.py          ← Pydantic schemas Analysis
│   │   └── guide.py             ← Pydantic schemas Guide
│   │
│   ├── routers/
│   │   ├── auth.py              ← /api/auth/*
│   │   ├── analyze.py           ← /api/analyze
│   │   ├── history.py           ← /api/history/*
│   │   ├── statistics.py        ← /api/statistics
│   │   ├── guides.py            ← /api/guides/*
│   │   └── health.py            ← /api/health
│   │
│   └── services/
│       └── ai_service.py        ← abstraksi AI: mock + interface untuk real API
│
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── .env                     ← VITE_API_BASE_URL
    │
    └── src/
        ├── main.jsx
        ├── App.jsx              ← router utama
        │
        ├── api/
        │   └── client.js        ← axios instance + interceptor token
        │
        ├── context/
        │   └── AuthContext.jsx  ← auth state global
        │
        ├── components/
        │   ├── layout/
        │   │   ├── Sidebar.jsx
        │   │   ├── Navbar.jsx
        │   │   └── Layout.jsx
        │   └── ui/
        │       ├── Card.jsx
        │       ├── Badge.jsx
        │       ├── LoadingSpinner.jsx
        │       └── ErrorMessage.jsx
        │
        └── pages/
            ├── LoginPage.jsx
            ├── RegisterPage.jsx
            ├── DashboardPage.jsx
            ├── AnalyzePage.jsx
            ├── HistoryPage.jsx
            ├── HistoryDetailPage.jsx
            ├── StatisticsPage.jsx
            └── GuidesPage.jsx
```

---

## Desain Database (SQLite)

### Tabel `users`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| username | TEXT UNIQUE NOT NULL | Nama pengguna |
| email | TEXT UNIQUE NOT NULL | Email |
| hashed_password | TEXT NOT NULL | Password di-hash dengan bcrypt |
| created_at | DATETIME | Waktu daftar |

### Tabel `analyses`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| user_id | INTEGER FK → users.id | Pemilik analisis |
| filename | TEXT NOT NULL | Nama file asli |
| image_path | TEXT NOT NULL | Path relatif di uploads/ |
| waste_name | TEXT | Nama/objek sampah |
| category | TEXT | Kategori (Plastik, Organik, dst) |
| material | TEXT | Material utama |
| description | TEXT | Penjelasan singkat |
| confidence | REAL | Tingkat keyakinan (0–1), nullable |
| recommendation | TEXT | Rekomendasi pengelolaan (JSON string) |
| is_mock | BOOLEAN DEFAULT TRUE | Tandai apakah hasil mock |
| created_at | DATETIME | Waktu analisis |

### Tabel `guides`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| title | TEXT NOT NULL | Judul panduan |
| category | TEXT | Kategori sampah terkait |
| content | TEXT NOT NULL | Isi panduan (Markdown/plain text) |
| icon | TEXT | Nama ikon (opsional) |
| created_at | DATETIME | Waktu dibuat |
| updated_at | DATETIME | Waktu diperbarui |

---

## Daftar Endpoint API

### Auth — `/api/auth`
| Method | Path | Fungsi |
|---|---|---|
| POST | /api/auth/register | Daftar akun baru |
| POST | /api/auth/login | Login, terima JWT token |
| GET | /api/auth/me | Ambil profil pengguna aktif |

### Analisis — `/api/analyze`
| Method | Path | Fungsi |
|---|---|---|
| POST | /api/analyze | Upload gambar, jalankan AI, simpan ke DB |

Request: `multipart/form-data` dengan field `file` (image).
Response: objek hasil analisis lengkap.

### Riwayat — `/api/history`
| Method | Path | Fungsi |
|---|---|---|
| GET | /api/history | Daftar riwayat milik user aktif (pagination opsional) |
| GET | /api/history/{id} | Detail satu riwayat |
| DELETE | /api/history/{id} | Hapus riwayat |

### Statistik — `/api/statistics`
| Method | Path | Fungsi |
|---|---|---|
| GET | /api/statistics | Total analisis, per kategori, kategori terbanyak |

### Panduan — `/api/guides`
| Method | Path | Fungsi |
|---|---|---|
| GET | /api/guides | Daftar semua panduan |
| GET | /api/guides/{id} | Detail panduan |
| POST | /api/guides | Tambah panduan baru |
| PUT | /api/guides/{id} | Update panduan |
| DELETE | /api/guides/{id} | Hapus panduan |

### Health — `/api/health`
| Method | Path | Fungsi |
|---|---|---|
| GET | /api/health | Status backend: OK + timestamp |

---

## Rencana Integrasi AI Vision

### Strategi Abstraksi
File `backend/services/ai_service.py` mendefinisikan satu fungsi publik:

```python
async def analyze_image(image_path: str) -> AnalysisResult
```

`AnalysisResult` adalah dataclass/TypedDict berisi:
- `waste_name`, `category`, `material`, `description`, `confidence`, `recommendation` (dict), `is_mock` (bool)

### Mode Mock (default aktif)
Ketika `AI_PROVIDER=mock` atau API key kosong:
- Return data dummy yang bervariasi berdasarkan nama file atau random seed
- `is_mock=True` selalu diset
- UI menampilkan badge **"⚠ Hasil Mock — Bukan Klasifikasi AI Nyata"**

### Cara Ganti ke API Nyata
1. Set `AI_PROVIDER=gemini` (atau `openai`) di `.env`
2. Set `AI_API_KEY=<key>` di `.env`
3. Tambah implementasi di `ai_service.py` di bawah block `if provider == "gemini":`
4. Tidak ada perubahan di router atau frontend — interface sama

---

## Kategori Sampah

| Kode | Label |
|---|---|
| organik | Organik |
| plastik | Plastik |
| kertas | Kertas |
| logam | Logam |
| kaca | Kaca |
| elektronik | Elektronik |
| b3 | B3 / Limbah Berbahaya |
| lainnya | Lainnya |

---

## Teknologi & Dependency

### Backend (`requirements.txt`)
```
fastapi
uvicorn[standard]
sqlalchemy
python-jose[cryptography]   # JWT
passlib[bcrypt]             # password hashing
python-multipart            # file upload
Pillow                      # validasi & resize gambar
python-dotenv
aiofiles
```

### Frontend (`package.json` dependencies)
```
react, react-dom
react-router-dom            # routing
axios                       # HTTP client
react-hook-form             # form management
lucide-react                # ikon lingkungan
recharts                    # chart statistik
```
devDependencies: `vite`, `@vitejs/plugin-react`, `tailwindcss`, `postcss`, `autoprefixer`

---

## Risiko Teknis & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| API Vision belum tersedia | Fitur inti tidak bisa diuji | Mock service aktif by default, semua fitur lain tetap berjalan |
| Gambar tidak jelas / kategori tidak dikenali | Hasil tidak akurat | Tampilkan status "Tidak dapat dipastikan", minta upload ulang |
| CORS error saat dev | Frontend tidak bisa akses backend | Konfigurasi `CORSMiddleware` di FastAPI sejak awal |
| File upload terlalu besar | Server lambat / crash | Validasi maks 5MB di frontend & backend; resize dengan Pillow sebelum kirim ke AI |
| SQLite concurrent write | Race condition | Hanya satu user lokal, risiko minimal; gunakan `check_same_thread=False` |
| JWT secret lemah di dev | Security issue | Pakai `SECRET_KEY` dari `.env`; beri contoh generate random key di README |

---

## Checklist MVP

### Setup Proyek
- [x] Inisialisasi backend (FastAPI + SQLAlchemy + .env)
- [x] Inisialisasi frontend (Vite + React + Tailwind)
- [x] Konfigurasi CORS backend
- [x] Konfigurasi proxy Vite ke backend

### Auth
- [x] Model & schema `User`
- [x] Endpoint register & login (JWT)
- [x] `AuthContext` di frontend
- [x] Halaman Login & Register
- [x] Protected routes

### Core Backend
- [x] Model & schema `Analysis`
- [x] `ai_service.py` dengan mock
- [x] Endpoint `POST /api/analyze` (upload + validasi + AI + simpan)
- [x] Endpoint `GET /api/history` & `GET /api/history/{id}`
- [x] Endpoint `DELETE /api/history/{id}`
- [x] Endpoint `GET /api/statistics`
- [x] Model & schema `Guide`
- [x] Endpoint CRUD `/api/guides`
- [x] Endpoint `GET /api/health`
- [x] Seed data panduan awal (opsional tapi direkomendasikan)

### Core Frontend
- [x] Layout utama (Sidebar + Navbar + konten)
- [x] Halaman Dashboard (ringkasan + aktivitas terbaru)
- [x] Halaman Analisis (upload, preview, trigger analisis, tampilkan hasil + badge mock)
- [x] Halaman Riwayat (daftar + detail)
- [x] Halaman Statistik (chart kategori + total)
- [x] Halaman Panduan (daftar + detail konten)

### Integrasi & Kualitas
- [x] Frontend terhubung ke semua endpoint
- [x] Error handling di semua form & request
- [x] Loading indicator di proses analisis
- [x] Validasi file (format + ukuran) di frontend & backend
- [x] Responsif (mobile + desktop)

### Finalisasi
- [x] README.md lengkap
- [x] `.env.example` untuk backend & frontend
- [x] Aplikasi dapat dijalankan dari nol dengan instruksi README

---

## Sub-Tasks Implementasi

### Sub-Task 1 — Backend Foundation
**Intent:** Menyiapkan fondasi backend: project structure, database, config, security, dan health endpoint.
**Expected Outcomes:**
- Backend dapat dijalankan dengan `uvicorn main:app`
- Database terbuat otomatis saat startup
- `/api/health` merespons `{"status": "ok"}`
- CORS dikonfigurasi untuk `http://localhost:5173`

**Todo List:**
1. Buat `backend/` folder dengan semua file struktur
2. Buat `requirements.txt`
3. Buat `core/config.py` (Settings dari `.env`)
4. Buat `core/database.py` (SQLAlchemy engine, session, Base)
5. Buat `core/security.py` (hash password, buat/verifikasi JWT)
6. Buat `routers/health.py`
7. Buat `main.py` (app, CORS, include routers, create_all tables)
8. Buat `.env` dan `.env.example`

**Relevant Context:** `backend/core/`, `backend/main.py`
**Status:** `[x] done`

---

### Sub-Task 2 — Auth Backend & Frontend
**Intent:** Implementasi register, login, dan protected route.
**Expected Outcomes:**
- User bisa register dan login via API
- JWT dikembalikan saat login
- Frontend memiliki LoginPage, RegisterPage, AuthContext
- Halaman selain auth ter-redirect ke login jika belum login

**Todo List:**
1. Buat `models/user.py` (ORM)
2. Buat `schemas/user.py` (Pydantic)
3. Buat `routers/auth.py` (register, login, me)
4. Register router di `main.py`
5. Inisialisasi frontend Vite + Tailwind
6. Buat `src/api/client.js` (axios + token interceptor)
7. Buat `src/context/AuthContext.jsx`
8. Buat `src/pages/LoginPage.jsx` dan `RegisterPage.jsx`
9. Buat `src/App.jsx` dengan React Router + protected route logic
10. Buat komponen layout dasar (Sidebar, Navbar, Layout)

**Relevant Context:** `backend/routers/auth.py`, `frontend/src/context/AuthContext.jsx`
**Status:** `[x] done`

---

### Sub-Task 3 — AI Service & Analyze Endpoint
**Intent:** Implementasi mock AI service dan endpoint analisis gambar.
**Expected Outcomes:**
- `POST /api/analyze` menerima gambar, menjalankan mock AI, menyimpan ke DB, dan mengembalikan hasil
- Hasil mock diberi tanda `is_mock: true`
- Validasi format (jpg/png/webp) dan ukuran (maks 5MB) berjalan

**Todo List:**
1. Buat `models/analysis.py` (ORM)
2. Buat `schemas/analysis.py` (Pydantic)
3. Buat `services/ai_service.py` (interface + mock implementation)
4. Buat `routers/analyze.py`
5. Buat folder `uploads/` dengan `.gitkeep`
6. Register router di `main.py`

**Relevant Context:** `backend/services/ai_service.py`, `backend/routers/analyze.py`
**Status:** `[x] done`

---

### Sub-Task 4 — History & Statistics Endpoints
**Intent:** Endpoint untuk membaca riwayat dan statistik analisis.
**Expected Outcomes:**
- `GET /api/history` mengembalikan daftar riwayat user aktif
- `GET /api/history/{id}` mengembalikan detail
- `DELETE /api/history/{id}` menghapus riwayat
- `GET /api/statistics` mengembalikan total + per kategori + kategori terbanyak

**Todo List:**
1. Buat `routers/history.py`
2. Buat `routers/statistics.py`
3. Register routers di `main.py`

**Relevant Context:** `backend/routers/history.py`, `backend/routers/statistics.py`
**Status:** `[x] done`

---

### Sub-Task 5 — Guides (Panduan) Backend
**Intent:** CRUD endpoint untuk konten panduan pengelolaan sampah.
**Expected Outcomes:**
- Semua endpoint `/api/guides` berfungsi
- Data panduan awal (seed) untuk 7 kategori sampah tersedia saat startup

**Todo List:**
1. Buat `models/guide.py` (ORM)
2. Buat `schemas/guide.py` (Pydantic)
3. Buat `routers/guides.py` (CRUD)
4. Buat fungsi seed data panduan di `main.py` (jalankan sekali saat startup jika tabel kosong)
5. Register router di `main.py`

**Relevant Context:** `backend/routers/guides.py`, `backend/models/guide.py`
**Status:** `[x] done`

---

### Sub-Task 6 — Frontend Core Pages
**Intent:** Implementasi semua halaman utama frontend yang terhubung ke backend.
**Expected Outcomes:**
- DashboardPage menampilkan ringkasan dan aktivitas terbaru
- AnalyzePage: upload gambar, preview, analisis, tampilkan hasil dengan badge mock
- HistoryPage: daftar riwayat dengan link ke detail
- HistoryDetailPage: detail lengkap satu analisis
- StatisticsPage: chart/grafik per kategori
- GuidesPage: daftar dan detail panduan

**Todo List:**
1. Buat komponen UI reusable (Card, Badge, LoadingSpinner, ErrorMessage)
2. Buat `DashboardPage.jsx`
3. Buat `AnalyzePage.jsx` (upload + preview + hasil + badge mock)
4. Buat `HistoryPage.jsx` dan `HistoryDetailPage.jsx`
5. Buat `StatisticsPage.jsx` (gunakan Recharts)
6. Buat `GuidesPage.jsx`
7. Hubungkan semua halaman ke routing di `App.jsx`

**Relevant Context:** `frontend/src/pages/`, `frontend/src/components/`
**Status:** `[x] done`

---

### Sub-Task 7 — Finalization & README
**Intent:** Pastikan semua fitur MVP berjalan, rapikan, buat dokumentasi.
**Expected Outcomes:**
- Semua checklist MVP tercentang
- README.md lengkap dengan instruksi instalasi dan konfigurasi
- `.env.example` tersedia di backend dan frontend
- Aplikasi dapat dijalankan dari nol mengikuti README

**Todo List:**
1. Review semua endpoint — pastikan error handling konsisten
2. Review semua halaman frontend — pastikan loading state & error state tampil
3. Pastikan badge mock tampil di setiap hasil analisis mock
4. Buat `README.md`
5. Buat `backend/.env.example` dan `frontend/.env.example`
6. Uji alur lengkap: register → login → upload gambar → lihat riwayat → lihat statistik → buka panduan

**Relevant Context:** `README.md`, `.env.example`
**Status:** `[x] done`
