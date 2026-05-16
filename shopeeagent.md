Saat ini saya sedang mengembangkan sistem AI Agent menggunakan CrewAI dan Camoufox. Agen saya sudah berhasil membuka browser secara otonom melalui Camoufox. Sekarang, saya ingin kamu memperbarui kode CrewAI dan logika Custom Tools-nya untuk mereplikasi fitur analisis dari ekstensi Chrome "Auto Ads Shopee".

Tolong integrasikan fitur dan logika berikut ke dalam alur CrewAI saya saat ini. Fokus pada penulisan logika alat (tools) ekstraksi data, kalkulasi matematis, dan pembaruan Agent/Task definitions.

1. Pembaruan Logika Custom Tool (Camoufox Data Extraction)
Buat/perbarui custom tool Camoufox bernama extract_shopee_ads_metrics. Tool ini bertugas untuk:

Mengekstrak data dari dashboard iklan Shopee. Data yang wajib diambil untuk setiap baris kampanye/produk: Nama Produk, Biaya Iklan (Shopee Cost), Omset Penjualan (GMV), Jumlah Klik, dan Tingkat Konversi (CR).

Output dari tool ini harus berupa struktur JSON array yang rapi.
(Catatan untuk AI: Karena struktur DOM Shopee bisa berubah, berikan saya struktur dasar playwirght/camoufox scrapingnya, dan asumsikan saya sudah memiliki selector yang benar)

2. Penambahan Alat Kalkulasi Finansial (Local Tool)
Buat sebuah Python function atau custom tool baru bernama calculate_actual_financials yang memproses JSON dari tool pertama. Gunakan formula matematis ini:

Input Data Eksternal (Mock data saja di kode): HPP Produk, Biaya Operasional, dan Potongan Admin Kategori Shopee (dalam %).

Formula yang wajib ada dalam fungsi ini:

Actual Cost = Shopee Cost * 1.11 (Menambahkan PPN iklan 11%).

Actual ROAS = GMV / Actual Cost.

Profit Bersih per Produk = Harga Jual - HPP - (Persentase Admin * Harga Jual) - Biaya Operasional.

Break-Even ROAS = Harga Jual / Profit Bersih per Produk.

Max CPC (Target Bid Maksimal) = Profit Bersih per Produk * Tingkat Konversi (CR).

Fungsi ini harus menambahkan field Actual Cost, Actual ROAS, Break-Even ROAS, dan Max CPC ke dalam setiap baris JSON produk.

3. Pembaruan Definisi Agent & Task di CrewAI
Tolong tuliskan ulang definisi Agent dan Task menggunakan spesifikasi berikut:

Agent 1: Data Extractor Agent
Role: Shopee Dashboard Navigator.

Goal: Menjalankan Camoufox, membaca tabel metrik iklan, dan mengembalikannya dalam format JSON yang bersih.

Tools: extract_shopee_ads_metrics.

Agent 2: Financial Analyst Agent
Role: E-commerce Financial Analyst.

Goal: Menerima JSON mentah, menghitung PPN 11%, Break-Even ROAS, dan Max CPC, lalu mengklasifikasikan performa (Bagus/Cukup/Rugi).

Tools: calculate_actual_financials.

Aturan Klasifikasi:

Jika Actual ROAS > Target ROAS (asumsikan target = 5.0) = Bagus.

Jika Actual ROAS < Target ROAS TAPI Actual ROAS > Break-Even ROAS = Cukup.

Jika Actual ROAS < Break-Even ROAS = Rugi (Boncos).

Agent 3: Ads Optimization Agent
Role: PPC Strategist.

Goal: Menganalisis laporan finansial dan mengeluarkan rekomendasi tindakan untuk mengoptimasi iklan.

Aturan Rekomendasi:

Jika "Rugi": Rekomendasikan "Turunkan Bid ke angka Max CPC atau Pause".

Jika "Cukup": Rekomendasikan "Pertahankan Bid".

Jika "Bagus": Rekomendasikan "Naikkan Bid 5%".

4. Output Terakhir (Orkestrasi)
Tolong pastikan Process dalam Crew berjalan berurutan (Sequential). Output akhir dari Crew harus berupa tabel Markdown ringkasan yang mencantumkan nama produk, ROAS Aktual, Break-Even ROAS, status performa, dan rekomendasi perubahan Bid.

Tolong berikan saya update kodenya sekarang, pisahkan antara fungsi Custom Tools dan kode utama CrewAI-nya.

---

## ✅ IMPLEMENTATION COMPLETED

Semua fitur telah diimplementasikan:

### Files Created:
1. `tools/shopee_tools.py` - Custom tools untuk Shopee
2. `crews/shopee_crew.py` - Shopee Crew dengan sequential process
3. `config/shopee_agents.yaml` - Agent definitions
4. `config/shopee_tasks.yaml` - Task definitions

### Files Modified:
1. `services/crew_executor.py` - Added `execute_shopee_ads_task()` method
2. `ui/main_window.py` - Added 📢 Shopee Ads button
3. `CHANGELOG.md` - Updated with new features
4. `requirement.md` - Updated with new features

---

## 🔐 Session Persistence (Implemented)

Fitur session persistence telah ditambahkan untuk menghindari login ulang setiap kali:

1. **File Session**: `.shopee_session` (JSON format)
2. **Storage State**: Camoufox menggunakan `storage_state` dari Playwright
3. **SaveSessionTool**: Agent bisa menyimpan session via tool

### Cara Kerja:
- **Run Pertama**: Browser terbuka tanpa session → User login manual → Session disimpan otomatis
- **Run Berikutnya**: Browser terbuka dengan session tersimpan → Langsung logged in

### Penting:
- Jangan re-login setiap run → Shopee akan trigger OTP atau block akun
- Session tersimpan di `.shopee_session` file
- Hapus file `.shopee_session` untuk reset session