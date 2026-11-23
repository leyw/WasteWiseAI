"""
AI Service Layer — WasteWise AI
================================
Abstraksi tunggal untuk klasifikasi sampah dari gambar.

Fungsi publik:
    analyze_image(image_path: str) -> dict

Cara mengaktifkan Gemini API:
    1. Set AI_PROVIDER=gemini di .env
    2. Set AI_API_KEY=<your_gemini_api_key> di .env
    3. (Opsional) Set GEMINI_MODEL=gemini-2.0-flash di .env
    Tidak ada perubahan di router atau frontend.

Model Gemini yang mendukung vision (multimodal):
    - gemini-2.0-flash       ← direkomendasikan (cepat, murah, mendukung gambar)
    - gemini-1.5-flash       ← alternatif
    - gemini-1.5-pro         ← lebih akurat, lebih lambat
"""

import json
from pathlib import Path
from typing import Optional

from core.config import get_settings

settings = get_settings()

# ── Kategori & data mock ───────────────────────────────────────────────────────

MOCK_DATA = [
    {
        "waste_name": "Botol Plastik PET",
        "category": "plastik",
        "material": "Polietilena tereftalat (PET)",
        "description": "Botol plastik transparan yang umum digunakan untuk air mineral dan minuman ringan.",
        "confidence": 0.91,
        "recommendation": {
            "pemilahan": "Pisahkan dari sampah organik dan masukkan ke tempat sampah berwarna kuning atau wadah khusus plastik.",
            "daur_ulang": "Dapat didaur ulang. Lepaskan tutup dan label sebelum diserahkan ke bank sampah atau pengepul.",
            "persiapan": "Bilas sisa cairan, peras botol agar lebih ringkas, kempes sebelum disimpan.",
            "pembuangan": "Serahkan ke bank sampah terdekat atau pengepul plastik untuk didaur ulang.",
            "tips_pengurangan": "Gunakan botol minum isi ulang (tumbler) untuk mengurangi pemakaian botol plastik sekali pakai.",
        },
    },
    {
        "waste_name": "Sisa Makanan / Kulit Buah",
        "category": "organik",
        "material": "Bahan organik biodegradable",
        "description": "Limbah makanan, sisa sayuran, kulit buah, atau bahan organik lain yang mudah terurai.",
        "confidence": 0.88,
        "recommendation": {
            "pemilahan": "Masukkan ke tempat sampah organik (hijau). Jangan campur dengan plastik atau kertas berminyak.",
            "daur_ulang": "Dapat diolah menjadi kompos untuk pupuk tanaman.",
            "persiapan": "Tiriskan sisa air sebelum dibuang agar tidak mencemari sampah lain.",
            "pembuangan": "Olah menjadi kompos di rumah menggunakan komposter sederhana atau serahkan ke fasilitas pengolahan organik.",
            "tips_pengurangan": "Rencanakan belanja agar tidak ada bahan makanan yang terbuang. Simpan sisa makanan dengan benar.",
        },
    },
    {
        "waste_name": "Kardus / Karton",
        "category": "kertas",
        "material": "Kertas karton berlapis",
        "description": "Kardus bekas kemasan produk, kotak pengiriman, atau karton tebal.",
        "confidence": 0.85,
        "recommendation": {
            "pemilahan": "Pisahkan dari sampah basah. Masukkan ke tempat sampah kertas atau wadah khusus.",
            "daur_ulang": "Dapat didaur ulang menjadi kertas baru. Sangat diminati oleh pengepul.",
            "persiapan": "Lipat atau pipihkan kardus agar tidak memakan banyak tempat. Pastikan kering dan tidak berminyak.",
            "pembuangan": "Serahkan ke bank sampah atau pengepul kertas/kardus.",
            "tips_pengurangan": "Gunakan kembali kardus bekas untuk penyimpanan atau proyek kerajinan sebelum dibuang.",
        },
    },
    {
        "waste_name": "Kaleng Aluminium",
        "category": "logam",
        "material": "Aluminium",
        "description": "Kaleng bekas minuman atau makanan dari bahan aluminium.",
        "confidence": 0.93,
        "recommendation": {
            "pemilahan": "Pisahkan dari sampah organik dan plastik. Masukkan ke tempat sampah logam.",
            "daur_ulang": "Aluminium 100% dapat didaur ulang tanpa batas kali dan bernilai ekonomi tinggi.",
            "persiapan": "Bilas sisa isi kaleng. Penyok atau gepeng agar lebih kompak saat disimpan.",
            "pembuangan": "Serahkan ke bank sampah atau pengepul logam. Aluminium memiliki nilai jual yang baik.",
            "tips_pengurangan": "Pilih produk dengan kemasan yang dapat diisi ulang atau gunakan wadah minuman permanen.",
        },
    },
    {
        "waste_name": "Botol Kaca",
        "category": "kaca",
        "material": "Kaca soda-lime",
        "description": "Botol atau wadah dari bahan kaca, bekas minuman atau bahan makanan.",
        "confidence": 0.87,
        "recommendation": {
            "pemilahan": "Pisahkan dari sampah lain. Tangani dengan hati-hati untuk menghindari pecahan.",
            "daur_ulang": "Dapat didaur ulang sepenuhnya. Kaca yang pecah pun masih dapat diolah ulang.",
            "persiapan": "Bilas bersih. Jika pecah, bungkus dengan koran sebelum dibuang agar tidak melukai petugas kebersihan.",
            "pembuangan": "Serahkan ke bank sampah atau pengepul kaca. Hindari membuang ke TPA karena kaca tidak terurai.",
            "tips_pengurangan": "Gunakan kembali botol kaca untuk menyimpan bahan makanan atau sebagai vas tanaman.",
        },
    },
    {
        "waste_name": "Ponsel Bekas / Elektronik",
        "category": "elektronik",
        "material": "Logam, plastik, komponen elektronik",
        "description": "Perangkat elektronik bekas seperti ponsel, charger, kabel, atau baterai.",
        "confidence": 0.82,
        "recommendation": {
            "pemilahan": "JANGAN campur dengan sampah biasa. Simpan terpisah sebagai sampah elektronik (e-waste).",
            "daur_ulang": "Komponen logam berharga (emas, perak, tembaga) dapat didaur ulang oleh fasilitas khusus.",
            "persiapan": "Hapus data pribadi sebelum menyerahkan perangkat. Jangan membongkar sendiri.",
            "pembuangan": "Serahkan ke program take-back produsen, pusat daur ulang e-waste resmi, atau toko elektronik yang menerima.",
            "tips_pengurangan": "Perbaiki perangkat sebelum membeli yang baru. Pilih produsen dengan program daur ulang.",
        },
    },
    {
        "waste_name": "Baterai / Limbah Berbahaya",
        "category": "b3",
        "material": "Logam berat, bahan kimia berbahaya",
        "description": "Baterai bekas, lampu neon, cat, pestisida, atau bahan kimia rumah tangga lainnya.",
        "confidence": 0.79,
        "recommendation": {
            "pemilahan": "WAJIB dipisahkan dari semua jenis sampah lain. Simpan di wadah tertutup yang aman.",
            "daur_ulang": "Harus ditangani oleh fasilitas pengelolaan B3 berlisensi. Jangan coba daur ulang sendiri.",
            "persiapan": "Jangan memecahkan atau membakar. Simpan dalam wadah aslinya jika memungkinkan.",
            "pembuangan": "Serahkan ke tempat pengumpulan B3 resmi, dinas lingkungan hidup, atau program pengelolaan khusus.",
            "tips_pengurangan": "Pilih produk ramah lingkungan. Gunakan baterai isi ulang. Hindari produk berbahan kimia berbahaya.",
        },
    },
    {
        "waste_name": "Objek Tidak Teridentifikasi",
        "category": "lainnya",
        "material": "Tidak diketahui",
        "description": "Jenis sampah tidak dapat diidentifikasi dengan pasti dari gambar yang diberikan.",
        "confidence": 0.45,
        "recommendation": {
            "pemilahan": "Periksa label atau kemasan untuk menentukan kategori yang tepat.",
            "daur_ulang": "Tidak dapat ditentukan tanpa identifikasi lebih lanjut.",
            "persiapan": "Pastikan sampah dalam kondisi bersih sebelum dibuang.",
            "pembuangan": "Jika ragu, buang ke tempat sampah umum dan hindari mencemari sampah daur ulang.",
            "tips_pengurangan": "Pilih produk dengan kemasan yang jelas terlabel jenis materialnya.",
        },
    },
]

# ── Prompt untuk Gemini ────────────────────────────────────────────────────────

GEMINI_SYSTEM_PROMPT = """Kamu adalah WasteWise AI, asisten pengelolaan sampah yang membantu masyarakat Indonesia mengidentifikasi dan mengelola sampah dengan benar.

Tugasmu adalah menganalisis gambar yang diberikan dan mengidentifikasi objek sampah yang ada di dalamnya.

Aturan penting:
- Gunakan Bahasa Indonesia yang mudah dipahami masyarakat umum.
- Hanya berikan informasi yang dapat kamu pastikan dari gambar.
- Jangan mengarang informasi material jika tidak terlihat jelas.
- Jika gambar tidak jelas atau bukan sampah, nyatakan dengan jujur.
- Jangan memberikan rekomendasi berbahaya untuk limbah B3 dan elektronik.
- Jangan mengklaim confidence sebagai probabilitas akurasi yang terkalibrasi — gunakan null jika tidak yakin.

Kategori sampah yang tersedia (gunakan huruf kecil):
organik | plastik | kertas | logam | kaca | elektronik | b3 | lainnya

Kembalikan HANYA objek JSON valid berikut, tanpa markdown, tanpa penjelasan tambahan, tanpa karakter lain di luar JSON:
{
  "waste_name": "nama spesifik objek yang terlihat di gambar",
  "category": "salah satu kategori di atas",
  "material": "material utama yang dapat dipastikan dari gambar, atau null jika tidak yakin",
  "description": "penjelasan singkat 1-2 kalimat tentang objek sampah ini",
  "confidence": null,
  "recommendation": {
    "pemilahan": "cara memilah sampah ini dengan benar",
    "daur_ulang": "apakah dapat didaur ulang dan bagaimana caranya",
    "persiapan": "cara mempersiapkan sebelum dibuang atau didaur ulang",
    "pembuangan": "cara pembuangan yang tepat sesuai konteks Indonesia",
    "tips_pengurangan": "tips praktis untuk mengurangi sampah sejenis"
  }
}

Jika gambar tidak jelas, gelap, blur, atau tidak menunjukkan objek sampah yang dapat diidentifikasi:
{
  "waste_name": "Objek tidak dapat diidentifikasi",
  "category": "lainnya",
  "material": null,
  "description": "Gambar tidak cukup jelas untuk mengidentifikasi jenis sampah. Coba ambil foto dengan pencahayaan lebih baik.",
  "confidence": null,
  "recommendation": {
    "pemilahan": "Periksa label atau kemasan untuk menentukan kategori yang tepat.",
    "daur_ulang": "Tidak dapat ditentukan tanpa identifikasi lebih lanjut.",
    "persiapan": "Pastikan sampah dalam kondisi bersih sebelum dibuang.",
    "pembuangan": "Jika ragu, buang ke tempat sampah umum.",
    "tips_pengurangan": "Pilih produk dengan kemasan yang jelas mencantumkan jenis materialnya."
  }
}"""

# ── MIME type mapping ──────────────────────────────────────────────────────────

MIME_MAP = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
}


# ── Interface publik ───────────────────────────────────────────────────────────

def _pick_mock(image_path: str) -> dict:
    """Pilih data mock secara deterministik berdasarkan nama file."""
    seed = sum(ord(c) for c in Path(image_path).name)
    return MOCK_DATA[seed % len(MOCK_DATA)]


async def analyze_image(image_path: str) -> dict:
    """
    Analisis gambar sampah dan kembalikan hasil klasifikasi.

    Returns:
        dict dengan keys:
            waste_name, category, material, description,
            confidence, recommendation (dict), is_mock (bool)

    Raises:
        RuntimeError: jika provider dikonfigurasi tetapi gagal.
                      Tidak ada fallback ke mock saat provider = gemini/openai.
    """
    provider = settings.AI_PROVIDER.lower()

    if provider == "mock" or not settings.AI_API_KEY:
        return _run_mock(image_path)

    elif provider == "gemini":
        # Raise exception jika gagal — tidak fallback ke mock
        return await _run_gemini(image_path)

    elif provider == "openai":
        return await _run_openai(image_path)

    else:
        # Provider tidak dikenal → gunakan mock
        return _run_mock(image_path)


# ── Mock implementation ────────────────────────────────────────────────────────

def _run_mock(image_path: str) -> dict:
    data = _pick_mock(image_path)
    return {**data, "is_mock": True}


# ── Gemini implementation — google-genai SDK v2 ───────────────────────────────

async def _run_gemini(image_path: str) -> dict:
    """
    Klasifikasi menggunakan Google Gemini Vision API.
    Menggunakan SDK resmi: google-genai v2.x

    Aktifkan dengan:
        AI_PROVIDER=gemini
        AI_API_KEY=<your_gemini_api_key>
        GEMINI_MODEL=gemini-2.0-flash  (opsional, default: gemini-2.0-flash)

    Raises:
        RuntimeError: dengan pesan yang mudah dipahami jika API gagal.
    """
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        raise RuntimeError(
            "Library google-genai belum terpasang. "
            "Jalankan: pip install google-genai"
        )

    # Validasi API key
    api_key = settings.AI_API_KEY
    if not api_key or api_key.strip() == "":
        raise RuntimeError(
            "GEMINI_API_KEY tidak ditemukan. "
            "Pastikan AI_API_KEY sudah diisi di file .env."
        )

    # Baca file gambar
    image_file = Path(image_path)
    if not image_file.exists():
        raise RuntimeError(f"File gambar tidak ditemukan: {image_path}")

    with open(image_file, "rb") as f:
        image_bytes = f.read()

    if len(image_bytes) == 0:
        raise RuntimeError("File gambar kosong atau tidak dapat dibaca.")

    # Tentukan MIME type
    ext = image_file.suffix.lower().lstrip(".")
    mime_type = MIME_MAP.get(ext, "image/jpeg")

    # Model dari konfigurasi
    model_name = settings.GEMINI_MODEL or "models/gemini-3-flash-preview"

    try:
        import asyncio
        # Inisialisasi client dengan API key
        gemini_client = genai.Client(api_key=api_key)

        # google-genai SDK v2 menggunakan sync I/O — jalankan di thread pool
        # agar tidak memblokir event loop FastAPI
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: gemini_client.models.generate_content(
                model=model_name,
                contents=[
                    genai_types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    GEMINI_SYSTEM_PROMPT,
                ],
            ),
        )

    except Exception as exc:
        err_msg = str(exc)
        # Terjemahkan pesan error umum
        if "API_KEY_INVALID" in err_msg or "API key not valid" in err_msg:
            raise RuntimeError(
                "API Key Gemini tidak valid. "
                "Periksa nilai AI_API_KEY di file .env."
            )
        elif "PERMISSION_DENIED" in err_msg:
            raise RuntimeError(
                "Akses ke Gemini API ditolak. "
                "Pastikan API Key memiliki izin yang benar di Google AI Studio."
            )
        elif "NOT_FOUND" in err_msg or "not found" in err_msg.lower():
            raise RuntimeError(
                f"Model '{model_name}' tidak ditemukan atau tidak tersedia. "
                f"Coba ganti GEMINI_MODEL=gemini-1.5-flash di .env."
            )
        elif "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
            raise RuntimeError(
                "Kuota Gemini API habis. "
                "Tunggu beberapa saat atau periksa penggunaan di Google AI Studio."
            )
        elif "timeout" in err_msg.lower() or "timed out" in err_msg.lower():
            raise RuntimeError(
                "Koneksi ke Gemini API timeout. "
                "Periksa koneksi internet dan coba lagi."
            )
        else:
            raise RuntimeError(
                f"Gemini API error: {err_msg[:200]}"
            )

    # Validasi respons
    if not response or not response.text:
        raise RuntimeError(
            "Gemini tidak mengembalikan respons. "
            "Coba unggah gambar yang lebih jelas."
        )

    raw = response.text.strip()

    # Bersihkan markdown code fence jika ada
    if raw.startswith("```"):
        lines = raw.split("\n")
        # Hapus baris pertama (```json atau ```) dan baris terakhir (```)
        inner = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
        raw = inner.strip()

    # Parse JSON
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as je:
        raise RuntimeError(
            f"Respons Gemini bukan JSON yang valid: {str(je)[:100]}. "
            f"Respons asli: {raw[:200]}"
        )

    # Validasi field wajib
    required_fields = ["waste_name", "category", "description"]
    missing = [f for f in required_fields if f not in result]
    if missing:
        raise RuntimeError(
            f"Respons Gemini tidak lengkap — field yang hilang: {', '.join(missing)}. "
            f"Respons asli: {raw[:200]}"
        )

    # Normalisasi kategori ke huruf kecil
    if "category" in result and result["category"]:
        result["category"] = result["category"].lower()

    # Pastikan recommendation adalah dict
    if "recommendation" not in result or not isinstance(result.get("recommendation"), dict):
        result["recommendation"] = {
            "pemilahan": "Periksa label kemasan untuk memilah dengan benar.",
            "daur_ulang": "Hubungi bank sampah terdekat untuk informasi daur ulang.",
            "persiapan": "Bersihkan sampah sebelum diserahkan.",
            "pembuangan": "Buang sesuai kategori sampah yang tepat.",
            "tips_pengurangan": "Kurangi pemakaian produk sekali pakai.",
        }

    result["is_mock"] = False
    return result


# ── OpenAI implementation (stub — aktifkan dengan AI_PROVIDER=openai) ─────────

async def _run_openai(image_path: str) -> dict:
    """
    Klasifikasi menggunakan OpenAI GPT-4o Vision API.
    Aktifkan dengan: AI_PROVIDER=openai, AI_API_KEY=<key>
    """
    try:
        import openai
        import base64

        client = openai.AsyncOpenAI(api_key=settings.AI_API_KEY)

        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        ext = Path(image_path).suffix.lower().lstrip(".")
        mime_type = MIME_MAP.get(ext, "image/jpeg")

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_data}"}},
                    {"type": "text", "text": GEMINI_SYSTEM_PROMPT},
                ],
            }],
            max_tokens=800,
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            inner = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
            raw = inner.strip()

        result = json.loads(raw)
        if "category" in result and result["category"]:
            result["category"] = result["category"].lower()
        result["is_mock"] = False
        return result

    except Exception as exc:
        raise RuntimeError(f"OpenAI API error: {str(exc)[:200]}")
