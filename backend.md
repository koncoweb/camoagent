# Backend Architecture

Backend aplikasi CamoAgent dirancang untuk menangani tugas berat (otomatisasi browser dan orkestrasi AI) tanpa membuat antarmuka pengguna (GUI) menjadi lambat (*freeze/hang*).

## Arsitektur Multi-Thread
Aplikasi ini membagi beban kerja ke dalam tiga jalur eksekusi (Thread) utama:

1. **Main GUI Thread:**
   Dikelola oleh PyQt6. Hanya digunakan untuk me-render elemen visual dan menangani *input* dari pengguna. Tidak boleh mengeksekusi operasi jaringan atau I/O yang berat.

2. **Browser Thread (`BrowserManager`):**
   Dikelola di dalam `services/browser_manager.py`. Mengisolasi *instance* Camoufox/Playwright. Playwright memiliki aturan ketat terkait *thread-safety*, di mana objek peramban hanya boleh diakses dari *thread* yang menciptakannya.

3. **CrewAI Thread (`CrewExecutor`):**
   Dikelola di dalam `services/crew_executor.py`. Saat pengguna mengirimkan pesan obrolan, eksekusi tugas agen CrewAI (`crew.kickoff()`) dilakukan di *thread* terpisah secara asinkron (berjalan sebagai *daemon*).

## Sistem Komunikasi: Command Queue
Masalah utama dalam arsitektur AI + Browser adalah *Cross-Thread Access Violation* (Agen AI di *Thread* 3 mencoba mengontrol Browser di *Thread* 2). 

Untuk mengatasi hal ini, CamoAgent mengimplementasikan **Pola Command Queue (Antrean Perintah)**:
- **`BrowserConfig` (Singleton):** Berfungsi sebagai penghubung global.
- Saat alat (*tool*) AI ingin berinteraksi dengan browser, alat tersebut tidak memanggil API Playwright secara langsung. Sebaliknya, alat tersebut menaruh instruksi kamus (contoh: `{"action": "click", "params": {"selector": "#btn"}}`) ke dalam `queue.Queue`.
- `BrowserManager` terus-menerus (*loop*) memeriksa antrean ini secara *non-blocking* di *thread* miliknya sendiri. Jika ada perintah masuk, ia akan mengeksekusinya menggunakan objek Playwright aslinya, lalu mengembalikan hasilnya ke *queue* respons.

## Penanganan Kesalahan (Error Handling)
Backend memiliki blok *try-except* untuk menangkap kesalahan tak terduga (seperti *timeout* jaringan atau kehabisan kuota API). Pesan *error* akan diubah ke format ramah pengguna (contoh: peringatan `insufficient_quota` SumoPod/OpenAI) dan dikirim ke GUI melalui sistem *Signal* PyQt6.