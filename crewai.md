# CrewAI Orchestration

Dokumentasi ini menjelaskan konfigurasi dan alur kerja agen kecerdasan buatan dalam proyek menggunakan framework **CrewAI**. Logika utama berada di dalam file `crews/browser_crew.py`.

## Pengaturan Model Bahasa (LLM)
- **Provider:** SumoPod AI (kompatibel dengan OpenAI SDK).
- **Model:** `deepseek-v4-pro`. Dipilih karena kemampuannya yang sangat baik dalam *reasoning* (penalaran) dan menangani tugas kompleks tanpa *hang*.
- **Endpoint Kustom:** Menggunakan `base_url` yang menunjuk ke `https://ai.sumopod.com/v1`.

## Penonaktifan Fitur Spesifik (Workarounds)
Untuk memastikan kompatibilitas dengan SumoPod AI yang tidak menyediakan model bawaan `text-embedding-ada-002`, fitur berikut secara eksplisit dinonaktifkan di `browser_crew.py`:
- `memory=False`: Mencegah CrewAI mencoba mem-vektorisasi percakapan lama menggunakan *embedder*.
- `planning=False`: Mencegah manajer agen mencoba membuat rencana eksekusi menggunakan *embedder*.

## Agen (Agents)
Konfigurasi peran dan tujuan masing-masing agen disimpan di `config/agents.yaml`.
1. **Navigator:** Agen yang ahli dalam navigasi struktur web (URL, elemen klik, input teks). Dilengkapi dengan parameter `max_iter=10` dan `max_execution_time=120` untuk mencegah *infinite loop* saat menghadapi situs rumit.
2. **Scraper:** Agen yang ahli dalam mengekstrak data dari halaman HTML dan mengubahnya menjadi format terstruktur.
3. **Analyst:** Agen yang menafsirkan data yang telah dikumpulkan dan merangkumnya (tidak diizinkan mendelegasikan tugas / `allow_delegation=False`).

## Alat (Tools)
Agen berinteraksi dengan peramban menggunakan *Tools* (berbasis `BaseTool`) yang terdefinisi di `tools/browser_tool.py`:
- `GetCurrentPageInfoTool`
- `NavigateToUrlTool`
- `GetPageContentTool`
- `GetPageTextTool` (Lebih disukai karena mengambil teks bersih `innerText`)
- `ScrollDownTool` (Untuk situs e-commerce yang memakai *lazy loading*)
- `ClickElementTool` & `TypeTextTool`

## Tugas (Tasks)
Instruksi spesifik disimpan di `config/tasks.yaml`. Tugas ini bersifat dinamis berdasarkan *input* dari pengguna dan memiliki aturan pemformatan (*Formatting Rules*) yang ketat untuk memastikan hasil akhir berbentuk Markdown yang terstruktur, lengkap dengan penandaan tebal, *bullet point*, dan emoji.