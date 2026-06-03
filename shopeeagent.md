# ShopeeAgent v1.2.0 — Panduan Developer

## Ringkasan Perubahan Terbaru

### v1.2.0 (2025-06-04): SpyAgent v2.0 + UX Improvements

**SpyAgent v2.0 — Market Intelligence untuk Penjual Indonesia:**
- Structured DOM extraction (16 field, clean JSON — tidak perlu LLM parsing)
- ReviewMinerTool: Baca ulasan pelanggan, deteksi pain points & strengths
- StoreProfilerTool: Profil toko lengkap (rating, followers, badges)
- GapAnalyzeTool: Deteksi niche dengan demand tinggi, supply rendah
- KeywordExtractorTool: Intelijen keyword dari judul produk kompetitor
- SpyAgent Action Bar: 4 tombol aksi di atas chat
- Memory + Planning enabled untuk analisis lebih dalam

**UX Improvements:**
- Settings sebagai dialog terpisah — chat di belakang tetap utuh
- API key auto-save ke .env — persisten antar restart
- Navigasi session-aware — chat tidak pernah clear tidak sengaja
- Tooltip dan modal text hitam — akhirnya terbaca
- Browser timeout fix untuk shopee.co.id

### v1.1.0 (2025-06-01): SpyAgent v1.0 + Chat Separation

- SpyAgent v1.0 initial release
- Chat separation: clear chat + context header saat switch agent
- Browser locale Indonesia (id-ID)

### v1.0.0 (2025-06-01): Initial Release

- Full ShopeeAgent branding
- Ads Management dengan 3 agen
- Session persistence auto-save
- NSIS installer

---

## Arsitektur Agent (7 Agents Total)

### Ads Crew (3 agents — sequential)
```
ShopeeNavigator → FinancialAnalyst → AdsOptimizer
```
Tools: 11 browser tools + 3 ads tools

### Spy Crew (4 agents — sequential, memory+planning enabled)
```
MarketScanner → CompetitorProfiler → TrendDetector → StrategySynthesizer
```
Tools: 11 browser tools + 5 spy tools (MarketScanTool, ReviewMinerTool, StoreProfilerTool, GapAnalyzeTool, KeywordExtractorTool)

---

## SpyAgent Action Bar

4 tombol aksi di atas chat saat spy mode active:

| Tombol | Warna | Aksi | Deskripsi |
|--------|-------|------|-----------|
| 📡 Scan | Hijau | `scan_market` | Scan produk dari halaman saat ini |
| 💬 Reviews | Biru | `review_mine` | Mining ulasan produk |
| 🏪 Store | Ungu | `store_profile` | Profiling toko kompetitor |
| 🎯 Full Report | Merah | `full_report` | Pipeline lengkap: scan → analisis → report |

---

## Navigasi yang Aman

| State Saat Ini | Klik | Hasil |
|---------------|------|-------|
| Spy active | ⚙️ Settings | Dialog muncul di atas — chat preserved |
| Spy active | 🤖 Crew | Panel crew — chat preserved |
| Spy active | 📊 Analytics | Panel analytics — chat preserved |
| Spy active | 🛒 Browser | Diblokir — return ke spy chat |
| Spy active | 📢 Ads | Diblokir — return ke spy chat |
| Ads active | 🕵️ Spy | Switch ke SpyAgent |
| Ads active | ⚙️ Settings | Dialog — chat preserved |
| Browser | 🕵️ Spy | Launch spy browser baru |

---

## Build Process

```powershell
# 1. PyInstaller build
python -m PyInstaller shopeeagent.spec --noconfirm

# 2. Copy data files (535+ files)
powershell -ExecutionPolicy Bypass -File copy_all_data.ps1

# 3. NSIS installer
& "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

Output: `ShopeeAgent-Setup.exe` (~204 MB)

---

## Settings Persistence

API key yang dimasukkan di Settings dialog auto-save ke `.env` file:
- `SUMOPOD_API_KEY`
- `OPENAI_API_KEY`  
- `SUMOPOD_BASE_URL`
- `OPENAI_BASE_URL`

Setting lain (provider, model, max_iter, memory, planning) di-save via signal ke CrewExecutor.

---

## Referensi

- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) — 11 error pattern dengan fix permanen
- [CHANGELOG.md](CHANGELOG.md) — Riwayat perubahan lengkap
- [requirement.md](requirement.md) — Spesifikasi requirement
- [README.md](README.md) — User-facing documentation
