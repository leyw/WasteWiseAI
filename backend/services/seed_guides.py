"""
Seed data panduan pengelolaan sampah untuk 7 kategori utama.
Dijalankan sekali saat startup jika tabel guides masih kosong.
"""

GUIDES_SEED = [
    {
        "title": "Panduan Mengelola Sampah Organik",
        "category": "organik",
        "icon": "Leaf",
        "content": """## Sampah Organik

Sampah organik adalah sampah yang berasal dari sisa makhluk hidup dan dapat terurai secara alami oleh mikroorganisme.

### Contoh Sampah Organik
- Sisa makanan (nasi, sayuran, buah)
- Kulit buah dan sayuran
- Daun kering dan ranting
- Ampas kopi dan teh
- Kotoran hewan ternak

### Cara Memilah
Pisahkan sampah organik dari sampah anorganik sejak di sumber (dapur). Gunakan wadah khusus dengan tutup untuk mencegah bau dan serangga.

### Cara Mengelola

**1. Komposting Sederhana**
Buat kompos di rumah menggunakan ember berlubang atau bin kompos. Campurkan sampah organik dengan dedaunan kering (rasio 1:1). Aduk setiap 2–3 hari dan kompos siap dalam 4–8 minggu.

**2. Eco-Enzyme**
Campurkan sisa buah dan sayuran dengan gula merah dan air (1:3:10). Fermentasikan selama 3 bulan dalam wadah tertutup. Hasilnya bisa digunakan sebagai pembersih alami dan pupuk cair.

**3. Lubang Resapan Biopori**
Buat lubang di tanah berdiameter 10 cm sedalam 100 cm. Masukkan sampah organik secara berkala. Sampah akan terurai dan meningkatkan resapan air tanah.

### Tips Pengurangan
- Rencanakan menu masak agar tidak ada bahan yang terbuang
- Simpan makanan dengan benar untuk memperpanjang kesegaran
- Beli produk lokal dan musiman yang lebih tahan lama""",
    },
    {
        "title": "Panduan Mengelola Sampah Plastik",
        "category": "plastik",
        "icon": "Package",
        "content": """## Sampah Plastik

Plastik adalah salah satu penyumbang sampah terbesar di Indonesia. Plastik membutuhkan ratusan tahun untuk terurai di alam.

### Jenis Plastik yang Umum Ditemui
- **PET (1)** — Botol air mineral, botol minuman
- **HDPE (2)** — Botol sampo, wadah deterjen
- **PP (5)** — Wadah makanan, sedotan, tutup botol
- **PS (6)** — Styrofoam, kotak makanan sekali pakai

### Cara Memilah
Pisahkan plastik berdasarkan jenisnya jika memungkinkan. Semua plastik bersih dapat diserahkan ke bank sampah.

### Cara Mempersiapkan Sebelum Daur Ulang
1. Bilas dan bersihkan dari sisa makanan atau minuman
2. Lepaskan label kertas jika ada
3. Penyok atau gepengkan botol agar lebih ringkas
4. Kering sebelum disimpan

### Cara Pembuangan
- Serahkan ke **bank sampah** terdekat
- Berikan ke **pengepul plastik** (rongsok)
- Manfaatkan program daur ulang dari produsen

### Tips Pengurangan (Prinsip 3R)
- **Refuse**: Tolak plastik sekali pakai yang tidak perlu
- **Reduce**: Kurangi pemakaian plastik
- **Reuse**: Gunakan kembali wadah plastik yang masih layak
- Bawa tas belanja sendiri (totebag)
- Gunakan botol minum isi ulang (tumbler)""",
    },
    {
        "title": "Panduan Mengelola Sampah Kertas",
        "category": "kertas",
        "icon": "FileText",
        "content": """## Sampah Kertas

Kertas dapat didaur ulang hingga 5–7 kali dan merupakan salah satu material yang paling mudah dikelola.

### Contoh Sampah Kertas
- Koran dan majalah bekas
- Kardus dan karton
- Kertas HVS bekas
- Buku bekas
- Kemasan kertas produk

### Cara Memilah
- Pisahkan kertas kering dari kertas basah/berminyak
- Kertas berminyak (bungkus gorengan) tidak dapat didaur ulang
- Tissue bekas juga tidak dapat didaur ulang — masuk sampah organik

### Cara Mempersiapkan
1. Pastikan kertas dalam kondisi kering
2. Lepaskan selotip, klip, atau staples jika ada
3. Lipat atau gulung untuk menghemat tempat
4. Pisahkan kardus dari kertas biasa (nilai jualnya berbeda)

### Cara Pembuangan
- **Bank sampah** menerima semua jenis kertas kering
- **Pengepul** (tukang loak) membeli kardus dan koran bekas
- Donasikan buku bekas ke perpustakaan atau komunitas

### Tips Pengurangan
- Kurangi cetak dokumen — gunakan tanda tangan digital
- Gunakan kedua sisi kertas saat mencetak
- Gunakan tas belanja kain daripada kantong kertas sekali pakai""",
    },
    {
        "title": "Panduan Mengelola Sampah Logam",
        "category": "logam",
        "icon": "Wrench",
        "content": """## Sampah Logam

Logam adalah material yang 100% dapat didaur ulang tanpa kehilangan kualitas, menjadikannya sangat berharga.

### Jenis Logam yang Umum
- **Aluminium** — Kaleng minuman, foil, peralatan masak
- **Besi/Baja** — Kaleng makanan, peralatan bekas
- **Tembaga** — Kabel listrik, pipa

### Cara Memilah
Pisahkan logam dari sampah lain. Gunakan magnet untuk membedakan besi (menempel) dari aluminium (tidak menempel).

### Cara Mempersiapkan
1. Bilas kaleng dari sisa makanan atau minuman
2. Gepengkan kaleng aluminium agar lebih ringkas
3. Pastikan tidak ada bagian tajam yang berbahaya
4. Jika ada cat atau pelapis, tetap bisa diserahkan ke pengepul

### Cara Pembuangan
- Serahkan ke **bank sampah** atau **pengepul logam**
- Aluminium memiliki **nilai jual tertinggi** di antara sampah daur ulang
- Besi tua dapat dijual ke tempat pengepul besi

### Tips Pengurangan
- Pilih produk dengan kemasan yang dapat diisi ulang
- Rawat peralatan logam agar tahan lama
- Beli produk bekas daripada yang baru jika memungkinkan""",
    },
    {
        "title": "Panduan Mengelola Sampah Kaca",
        "category": "kaca",
        "icon": "GlassWater",
        "content": """## Sampah Kaca

Kaca dapat didaur ulang sepenuhnya tanpa batas kali dan tidak kehilangan kualitasnya. Namun, kaca pecah berbahaya dan harus ditangani dengan hati-hati.

### Contoh Sampah Kaca
- Botol kaca bekas minuman
- Toples dan wadah makanan
- Cermin dan kaca jendela pecah
- Lampu pijar (bukan LED/neon)

### Cara Memilah
Pisahkan kaca dari sampah lain. Tangani dengan hati-hati untuk menghindari cedera.

### Cara Mempersiapkan
1. Bilas botol atau toples dari sisa isi
2. Lepaskan tutup logam atau plastik
3. Jika kaca **pecah**, bungkus terlebih dahulu dengan beberapa lapis koran
4. Beri label "KACA PECAH — BERBAHAYA" pada bungkusan

### Cara Pembuangan
- Botol utuh: serahkan ke **bank sampah** atau **pengepul kaca**
- Kaca pecah: bungkus rapat sebelum dibuang ke tempat sampah umum
- Beberapa supermarket menerima botol kaca untuk ditukar

### Tips Pengurangan
- Gunakan kembali botol dan toples kaca untuk penyimpanan
- Pilih produk dengan kemasan kaca daripada plastik
- Beli produk dalam kemasan besar untuk mengurangi jumlah botol""",
    },
    {
        "title": "Panduan Mengelola Sampah Elektronik (E-Waste)",
        "category": "elektronik",
        "icon": "Monitor",
        "content": """## Sampah Elektronik (E-Waste)

Sampah elektronik mengandung bahan berbahaya seperti timbal, merkuri, dan kadmium. Penanganan yang salah dapat mencemari lingkungan dan membahayakan kesehatan.

### Contoh E-Waste
- Ponsel, tablet, laptop bekas
- Charger dan kabel
- Baterai (lithium, NiMH)
- TV, monitor, printer
- Peralatan rumah tangga elektronik

### PERINGATAN PENTING
- **JANGAN** membakar e-waste — menghasilkan gas beracun
- **JANGAN** membuang ke tempat sampah biasa
- **JANGAN** membongkar sendiri tanpa pengetahuan khusus

### Cara Mempersiapkan
1. **Hapus semua data pribadi** sebelum menyerahkan perangkat
2. Lepaskan baterai jika memungkinkan (serahkan terpisah)
3. Simpan dalam kantong atau kotak untuk melindungi dari benturan

### Cara Pembuangan yang Benar
- **Program take-back produsen** — banyak merek menerima produk bekas mereka
- **Pusat daur ulang e-waste resmi** — terdaftar di Dinas LHK setempat
- **Toko elektronik** — beberapa menerima perangkat lama saat membeli baru
- **Bank sampah** yang memiliki fasilitas e-waste

### Tips Pengurangan
- Perbaiki perangkat sebelum membeli baru (repair culture)
- Pilih merek dengan program daur ulang dan garansi panjang
- Beli produk rekondisi/refurbished yang masih layak pakai""",
    },
    {
        "title": "Panduan Mengelola Limbah B3 (Bahan Berbahaya dan Beracun)",
        "category": "b3",
        "icon": "AlertTriangle",
        "content": """## Limbah B3 (Bahan Berbahaya dan Beracun)

Limbah B3 adalah limbah yang mengandung zat berbahaya yang dapat merusak lingkungan dan kesehatan manusia jika tidak ditangani dengan benar.

### Contoh Limbah B3 Rumah Tangga
- Baterai bekas (semua jenis)
- Cat dan thinner
- Obat-obatan kadaluwarsa
- Pestisida dan herbisida
- Lampu neon dan lampu hemat energi (CFL)
- Bahan pembersih kimia (asam, basa kuat)

### PERINGATAN KERAS
- **JANGAN PERNAH** membuang ke saluran air, got, atau sungai
- **JANGAN** membakar — menghasilkan gas beracun berbahaya
- **JANGAN** mencampur dengan sampah biasa
- **JANGAN** mencoba mendaur ulang sendiri

### Cara Penyimpanan Sementara
1. Simpan dalam wadah aslinya dengan tutup rapat
2. Beri label yang jelas
3. Jauhkan dari jangkauan anak-anak
4. Simpan di tempat sejuk, kering, dan berventilasi
5. Jauhkan dari sumber api dan panas

### Cara Pembuangan yang Aman
- **Dinas Lingkungan Hidup** setempat memiliki fasilitas pengumpulan B3
- **Apotek** — terima obat kadaluwarsa untuk dimusnahkan
- **Produsen** — beberapa menerima produk B3 bekas (baterai, cat)
- **Fasyankes (rumah sakit/klinik)** — untuk obat-obatan

### Kontak Darurat
Jika terjadi tumpahan atau kecelakaan, hubungi:
- **BPBD (Badan Penanggulangan Bencana Daerah)** setempat
- **Dinas Lingkungan Hidup** kota/kabupaten""",
    },
]


def seed_guides(db):
    """Isi tabel guides dengan data awal jika masih kosong."""
    from models.guide import Guide
    if db.query(Guide).count() == 0:
        for data in GUIDES_SEED:
            guide = Guide(**data)
            db.add(guide)
        db.commit()
        print(f"[OK] Seeded {len(GUIDES_SEED)} panduan ke database.")
    else:
        print("[OK] Tabel guides sudah berisi data, seed dilewati.")
