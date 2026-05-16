================================================================================
                    SHOPEAGENT - AI SHOPEE MANAGER
                         Panduan Instalasi & Penggunaan
================================================================================

DESKRIPSI
----------
ShopeeAgent adalah aplikasi desktop berbasis AI yang membantu Anda mengelola
iklan dan toko Shopee dengan lebih efisien. Aplikasi ini menggunakan teknologi
multi-agent AI untuk menganalisis performa iklan dan memberikan rekomendasi
optimasi.

================================================================================
PERSYARATAN SISTEM
================================================================================

- Sistem Operasi : Windows 10 atau Windows 11
- Processor      : Intel Core i3 / AMD Ryzen 3 atau lebih tinggi
- RAM            : Minimal 4 GB (disarankan 8 GB)
- Storage        : Minimal 1 GB ruang kosong
- Internet      : Diperlukan untuk pertama kali install dan download browser
- Akun Shopee   : Akun Shopee Seller Center yang aktif

================================================================================
CARA INSTALASI
================================================================================

1. DOUBLE-CLICK file "ShopeeAgent-Setup.exe"

2. Jika muncul peringatan "Windows Protected Your PC":
   - Klik "More info"
   - Klik "Run anyway"

3. Ikuti instruksi di layar instalasi:
   - Pilih lokasi instalasi (default: C:\Program Files\ShopeeAgent)
   - Klik "Install" untuk melanjutkan

4. Tunggu hingga proses instalasi selesai

5. Klik "Finish" untuk menyelesaikan instalasi

6. SHORTCUT akan otomatis dibuat di:
   - Desktop
   - Start Menu

================================================================================
PENGATURAN AWAL (PENTING!)
================================================================================

SETELAH INSTALASI, IKUTI LANGKAH BERIKUT:

1. BUKA FILE .env
   --------------------------------------------------------------------------
   Buka folder instalasi:
   C:\Program Files\ShopeeAgent\

   Edit file bernama ".env" menggunakan Notepad

2. TAMBAHKAN API KEY ANDA
   --------------------------------------------------------------------------
   Ubah baris:
   SUMOPOD_API_KEY=your_api_key_here

   Menjadi (contoh):
   SUMOPOD_API_KEY=sk-xxxxxxxxxxxxx

   CATATAN: Anda bisa mendapatkan API key dari SumoPod AI
   Kunjungi: https://ai.sumopod.com

3. SIMPAN file .env

================================================================================
CARA MENJALANKAN APLIKASI
================================================================================

METODE 1 - DARI DESKTOP:
   Double-click icon "ShopeeAgent" di Desktop

METODE 2 - DARI START MENU:
   1. Klik tombol Start
   2. Ketik "ShopeeAgent"
   3. Klik pada hasil "ShopeeAgent"

================================================================================
CARA PENGGUNAAN
================================================================================

1. BUKA BROWSER SHOPEE
   --------------------------------------------------------------------------
   - Klik icon 🛒 (Shopee Browser) di sidebar kiri
   - Browser Camoufox akan terbuka otomatis ke Shopee Seller Center
   - Login ke akun Shopee Anda secara manual (sekali saja)
   - Session akan tersimpan untuk penggunaan berikutnya

2. NAVIGASI KE HALAMAN IKLAN
   --------------------------------------------------------------------------
   - Di browser, navigasi ke halaman iklan Shopee
   - Menu: Iklan > Iklan Produk

3. MULAI ANALISIS IKLAN
   --------------------------------------------------------------------------
   - Klik icon 📢 (Shopee Ads) di sidebar kiri aplikasi
   - AI akan menganalisis data iklan secara otomatis
   - Tunggu hingga analisis selesai

4. LIHAT HASIL
   --------------------------------------------------------------------------
   - Hasil analisis akan muncul di panel chat
   - Include: ROAS, Break-Even, Status Performa, dan Rekomendasi

================================================================================
TROUBLESHOOTING
================================================================================

MASALAH: Aplikasi tidak bisa dibuka setelah instalasi
--------------------------------------------------------------------------
SOLUSI:
- Pastikan Anda sudah menginstall Visual C++ Redistributable
- Download dari: https://aka.ms/vs/17/release/vc_redist.x64.exe

MASALAH: Error "Permission denied" saat membuka aplikasi
--------------------------------------------------------------------------
SOLUSI:
- Klik kanan icon ShopeeAgent
- Pilih "Run as administrator"

MASALAH: Browser tidak terbuka
--------------------------------------------------------------------------
SOLUSI:
- Buka Command Prompt sebagai Administrator
- Jalankan perintah: python -m camoufox fetch
- Tunggu hingga download selesai

MASALAH: API Error saat menggunakan AI
--------------------------------------------------------------------------
SOLUSI:
- Pastikan API key di file .env sudah benar
- Pastikan Anda memilikiCredits di SumoPod AI
- Cek koneksi internet Anda

MASALAH: Aplikasi crash saat pertama kali dibuka
--------------------------------------------------------------------------
SOLUSI:
- Pastikan .env file ada dan valid
- Pastikan tidak ada karakter khusus di API key
- Hapus file .shopee_session jika ada masalah login

================================================================================
MENGHAPUS APLIKASI (UNINSTALL)
================================================================================

1. BUKA CONTROL PANEL
   - Klik Start > ketik "Control Panel"
   - Pilih "Programs and Features"

2. CARI "SHOPEAGENT"
   - Klik kanan pada "ShopeeAgent"
   - Pilih "Uninstall"

3. IKUTI INSTRUKSI
   - Tunggu hingga proses uninstall selesai

ATAU:
   - Buka folder instalasi (C:\Program Files\ShopeeAgent\)
   - Jalankan file "Uninstall.exe"

================================================================================
INFORMASI LEBIH LANJUT
================================================================================

Website      : https://shopeeagent.com (jika tersedia)
Dokumentasi : https://docs.shopeeagent.com
Support     : Hubungi administrator Anda

================================================================================
Versi       : 1.0.0
Tanggal     : 2025
Lisensi     : MIT License
================================================================================

TERIMA KASIH TELAH MENGGUNAKAN SHOPEAGENT!

Jika panduan ini tidak membantu, silakan hubungi administrator atau tim support
Anda untuk mendapatkan bantuan lebih lanjut.
