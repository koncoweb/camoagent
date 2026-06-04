================================================================================
                    SHOPEAGENT v1.3.0 — AI SHOPEE MANAGER
                         Panduan Instalasi & Penggunaan
================================================================================

DESKRIPSI
----------
ShopeeAgent adalah aplikasi desktop berbasis AI yang membantu Anda mengelola
toko Shopee dengan lebih efisien. Menggunakan teknologi multi-agent AI untuk:

1. Menganalisis performa iklan Shopee Ads
2. Melakukan riset pasar & analisis kompetitor (SpyAgent)
3. Memberikan rekomendasi strategis untuk bisnis Anda

================================================================================
PERSYARATAN SISTEM
================================================================================

- Sistem Operasi : Windows 10 atau Windows 11
- Processor      : Intel Core i3 / AMD Ryzen 3 atau lebih tinggi
- RAM            : Minimal 4 GB (disarankan 8 GB)
- Storage        : Minimal 1 GB ruang kosong
- Internet       : Diperlukan untuk install dan download browser
- Akun Shopee    : Akun Shopee Seller Center (untuk Ads Agent)
- API Key        : Key dari SumoPod AI atau OpenAI (untuk fitur AI)

================================================================================
CARA INSTALASI
================================================================================

1. DOUBLE-CLICK file "ShopeeAgent-Setup.exe"

2. Jika muncul peringatan "Windows Protected Your PC":
   - Klik "More Info" lalu "Run Anyway"

3. Ikuti petunjuk di layar

4. Setelah selesai, shortcut akan muncul di Desktop

================================================================================
SETUP AWAL (PENTING!)
================================================================================

1. JALANKAN ShopeeAgent dari Desktop shortcut

2. KLIK ikon ⚙️ (Settings) di sidebar kiri
   - Settings terbuka sebagai jendela terpisah
   - Chat di belakang TETAP ADA — tidak hilang

3. TAMBAHKAN API KEY ANDA
   - Pilih Provider: SumoPod AI (default) atau OpenAI
   - Masukkan API key di kolom yang tersedia
   - Klik "Apply Settings" -> API key TERSIMPAN PERMANEN

   CATATAN: Anda bisa mendapatkan API key dari:
   - SumoPod AI: https://ai.sumopod.com
   - OpenAI: https://platform.openai.com

4. PILIH MODEL AI
   - SumoPod: MiniMax-M2.7-highspeed (recommended)
   - OpenAI: gpt-4o-mini

================================================================================
FITUR UTAMA
================================================================================

🛒 Browser Shopee (Seller Center)
- Buka browser ke seller.shopee.co.id
- Login sekali, auto-save session
- Digunakan untuk Ads Agent

📢 Shopee Ads Agent
- Analisis performa iklan Shopee Anda
- Hitung ROAS, Break-Even, Max CPC
- Klasifikasi: Bagus / Cukup / Rugi
- Rekomendasi optimasi bid

🕵️ SpyAgent — Market Research (BARU!)
- Buka browser ke shopee.co.id (marketplace)
- TIDAK PERLU LOGIN — scan sebagai pembeli biasa
- 4 tombol aksi di atas chat:
  📡 Scan Market — Ekstrak data produk
  💬 Review Mine — Analisis ulasan pelanggan
  🏪 Store Profile — Profil toko kompetitor
  🎯 Full Report — Laporan market intelligence lengkap

🤖 AI Crew — Lihat konfigurasi agen AI
📊 Analytics — Dashboard performa & history
⚙️ Settings — Konfigurasi API key & model

================================================================================
TIPS PENGGUNAAN
================================================================================

1. API KEY DISIMPAN PERMANEN
   - Setting → Apply → key tersimpan di file .env
   - Tidak perlu input ulang setelah restart aplikasi

2. SESSION LOGIN DISIMPAN OTOMATIS
   - Login sekali di browser Seller Center
   - Session auto-save saat browser ditutup

3. NAVIGASI AMAN
   - Klik menu lain saat spy/ads active = kembali ke chat
   - Chat TIDAK hilang saat pindah panel Crew/Analytics
   - Settings terbuka sebagai jendela TERPISAH

4. SPY AGENT TIDAK PERLU LOGIN
   - Bisa langsung scan produk di marketplace
   - Cari keyword atau browse kategori, lalu klik Scan

================================================================================
TROUBLESHOOTING
================================================================================

MASALAH: Aplikasi tidak bisa dibuka
SOLUSI: Pastikan antivirus tidak memblokir. Tambahkan ke exception.

MASALAH: Browser tidak muncul
SOLUSI: Internet diperlukan untuk download Camoufox (sekali saja).

MASALAH: API key tidak tersimpan
SOLUSI: Gunakan Settings dialog (⚙️), klik Apply. Atau edit langsung
        file .env di folder C:\Program Files\ShopeeAgent\

MASALAH: SpyAgent browser timeout
SOLUSI: Koneksi internet lambat. Coba lagi — app sudah dioptimasi
        dengan timeout 60 detik + fallback.

================================================================================
KONTAK & DUKUNGAN
================================================================================

Untuk bantuan teknis, hubungi pengembang aplikasi.
