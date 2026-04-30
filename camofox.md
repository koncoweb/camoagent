# Camoufox & Stealth Automation

CamoAgent menggunakan **Camoufox** (berbasis Playwright) sebagai lapisan *stealth browser* untuk menavigasi web tanpa terdeteksi oleh sistem keamanan anti-bot (seperti Cloudflare, Datadome, atau proteksi internal Shopee).

## Konsep Inti Camoufox
Sesuai dengan dokumentasi resmi, Camoufox menggunakan tiga prinsip utama:
1. **Lightweight:** Berbasis Firefox yang telah dioptimalkan (tanpa telemetri).
2. **Undetectable:** Mengubah *fingerprint* di level C++, bukan sekadar menyuntikkan manipulasi JavaScript (seperti Puppeteer/Playwright standar) yang mudah terdeteksi.
3. **Consistent:** Menjaga konsistensi perangkat keras palsu agar selalu terlihat natural.

## Integrasi & Konfigurasi di CamoAgent
Peluncuran peramban ditangani oleh `BrowserManager` (`services/browser_manager.py`).

### Fitur *Humanize* (Stealth & Anti-Bot)
```python
with Camoufox(headless=False, humanize=True) as browser:
```
Aplikasi secara aktif menggunakan parameter `humanize=True`. Fitur ini sangat krusial saat menavigasi situs *e-commerce* seperti Shopee. Ia memastikan bahwa semua pergerakan *mouse*, klik, dan pengguliran halaman (yang diperintahkan oleh CrewAI) akan dihitung algoritmanya menggunakan `HumanCursor` (C++) agar menyerupai pergerakan dan penundaan respons (*delay*) layaknya manusia sungguhan.

### Interaksi Halaman (*Page Evaluation*)
Karena banyak situs modern yang memuat konten melalui JavaScript (*lazy-loading*) dan memiliki struktur HTML yang sangat kotor jika dibaca secara mentah, interaksi alat telah dioptimalkan:
- **Pengguliran (Scrolling):** Alat `ScrollDownTool` menggunakan `window.scrollBy` dan penundaan (`time.sleep`) yang memberi waktu bagi peramban untuk menyelesaikan *request* API latar belakang (misalnya memuat gambar atau daftar produk Shopee tambahan).
- **Ekstraksi Teks Bersih:** Daripada menarik ribuan baris elemen HTML tak berguna, agen disarankan menggunakan `document.body.innerText` (melalui `GetPageTextTool`). Cara ini tidak hanya menghemat *context window/token* LLM, tetapi juga mempercepat proses analisis data secara drastis.