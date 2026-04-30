# Frontend Architecture (PyQt6)

Aplikasi CamoAgent menggunakan **PyQt6** untuk membangun antarmuka pengguna grafis (GUI) desktop yang modern, responsif, dan non-blocking.

## Komponen Utama
Arsitektur frontend terpusat pada file `ui/main_window.py` yang menampung beberapa komponen (widget) kustom:

### 1. `MainWindow` (Jendela Utama)
- Berfungsi sebagai *container* utama yang menggabungkan *sidebar* (ikon), area *chat* utama, dan panel status.
- Bertanggung jawab untuk menyambungkan (mengkoneksikan) berbagai `pyqtSignal` dari komponen backend (`BrowserManager` dan `CrewExecutor`) ke antarmuka pengguna.

### 2. `IconBar` (Navigasi Samping)
- Menyediakan tombol akses cepat menggunakan `EmojiButton` kustom (contoh: 🦊 untuk Browser, 🤖 untuk Crew).
- Memancarkan sinyal kustom `icon_clicked` ketika tombol ditekan, yang kemudian akan ditangkap oleh `MainWindow` untuk menjalankan *service* di backend.

### 3. `ChatWidget` (Antarmuka Obrolan AI)
- Merupakan tempat interaksi pengguna dengan AI.
- **Dukungan Markdown:** Fitur rendering bawaan menggunakan `Qt.TextFormat.MarkdownText` memungkinkan respons AI ditampilkan dengan cantik (mendukung *Header*, *Bold*, *List*, dll).
- **Word Wrapping & Text Interaction:** Memiliki fitur *word-wrap* (`setWordWrap(True)`) agar teks tidak terpotong, dan tautan di dalam obrolan dapat diklik langsung oleh pengguna.

### 4. `StatusPanel` (Panel Log)
- Terletak di sisi kanan aplikasi untuk memantau log sistem secara *real-time*.
- Melacak aktivitas seperti peluncuran browser, status agen (working/ready/error), dan interaksi pengguna.

## Styling
- Aplikasi menggunakan *stylesheet* (mirip CSS) yang disuntikkan ke dalam komponen PyQt6 untuk menciptakan tema *Dark Mode* modern (warna dominan: `#1E1E1E`, `#252526`, `#2D2D30`).

## Manajemen Event (Non-blocking)
Karena PyQt6 berjalan di *Main Thread* (Thread Utama), semua tugas yang memakan waktu lama (seperti peluncuran peramban atau pemrosesan AI) dijalankan di *background threads*. Interaksi antara *worker threads* dan GUI dilakukan sepenuhnya secara aman menggunakan sistem `pyqtSignal` dan `pyqtSlot`.