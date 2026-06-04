# ShopeeAgent v1.3.2 — Panduan Developer

## Ringkasan Perubahan Terbaru

### v1.3.2 (2025-06-04): Critical Bug Fix — Browser Signals
- **QMetaObject.invokeMethod → signal.emit()**: BrowserManager juga pakai pattern yang salah — 3 signal browser tidak pernah emit di build. Fixed: `browser_ready.emit()`, `browser_closed.emit()`, `error_occurred.emit()`
- **Browser silent failure fix**: Browser icon sekarang berfungsi penuh — status "Connected", loading indicator, error handling
- **Thread cleanup**: `finally` block sekarang set `_thread = None`, tidak lagi emit `browser_ready` saat shutdown

### v1.3.1 (2025-06-04): Bug Fixes & Stability
- **Spy agent tidak terblokir saat ads session**: `"spy"` ditambahkan ke allowed icons saat `_ads_session_active`
- **Browser tidak gagal launch saat switch agent**: `launch_browser()` sekarang force-close thread lama (4s timeout) sebelum launch baru
- **`close()` timeout**: 2s → 8s, set `_thread = None` setelah join untuk mencegah deadlock
- **Singkatan**: DEVELOPER_GUIDE.md memiliki 17 error pattern terdokumentasi

### v1.3.0 (2025-06-04): Elegant UI + Category Picker + Loading State
- Dark sidebar (#2B2B2B) + single blue accent (#4A90D9) — UI elegan, monokromatik
- Category picker: 14 kategori populer Shopee sebagai tombol + custom input
- Animated loading indicator (◌○◎◉●) saat agent working — pinned di luar scroll area
- Crew Management panel: 3 crew cards + Camoufox status card real-time
- Chat bubbles auto-sizing fix — SelfSizingTextEdit + proper containers
- Signal fix: QMetaObject.invokeMethod() tidak bisa emit pyqtSignal → ganti .emit()
- Versi tampil di window title bar

### v1.2.0 (2025-06-04): SpyAgent v2.0 + UX Improvements
- SpyAgent v2.0 (4 agents, 5 tools, 16-field structured JSON extraction)
- Settings sebagai dialog terpisah
- API key persistence ke .env
- Session-aware navigation

### v1.1.0 (2025-06-01): SpyAgent v1.0 + Chat Separation
### v1.0.0 (2025-06-01): Initial Release

---

## Pelajaran Kritis dari Error (diprioritaskan)

### 🥇 #1: Jangan compile PyInstaller dengan `Select-Object`
**Error**: Build tampak stuck, terminal poll diulang-ulang  
**Fix**: Biarkan PyInstaller output penuh. Wait 5 menit sebelum first check.

### 🥇 #2: SELALU jalankan `copy_all_data.ps1` setelah setiap build
**Error**: 535 data files dari 7 packages tidak ter-copy → runtime FileNotFoundError  
**Fix**: Jangan tambah file satu-satu ke .spec. Gunakan copy_all_data.ps1 secara konsisten.

### 🥇 #3: `signal.emit()` BUKAN `QMetaObject.invokeMethod()`
**Error**: Loading indicator tidak pernah muncul meski log menunjukkan "working"  
**Root**: invokeMethod() tidak bisa memanggil signal. Hanya method/slot. Exception di-swallow oleh try/except.  
**Fix**: `self.status_update.emit(agent, status)` — PyQt auto-queues cross-thread.

### 🥇 #4: `setFixedHeight()` SEBELUM widget dirender = truncated
**Error**: Chat bubble selalu terpotong — hanya 2-3 baris kelihatan  
**Root**: `doc.size().height()` tidak akurat sebelum layout.  
**Fix**: `SelfSizingTextEdit` subclass dengan dynamic `sizeHint()`.

### 🥇 #5: `addStretch()` untuk alignment, BUKAN `setAlignment()`
**Error**: Bubble lebar 60px — hancur  
**Root**: `setAlignment(AlignLeft)` membatasi widget ke `sizeHint()` width  
**Fix**: `clayout.addWidget(w)` + `clayout.addStretch()` — widget mengisi ruang yang tersedia

### 🥇 #6: Thread join timeout harus cukup panjang
**Error**: Browser tidak launch setelah switch agent  
**Root**: `close()` join(2) terlalu pendek untuk Camoufox cleanup → thread masih is_alive() → `launch_browser()` silent return  
**Fix**: close() join(8), launch_browser() force-close thread lama jika masih ada

### 🥇 #7: QDialog + parent QFrame = invisible
**Error**: Settings dialog tidak muncul  
**Root**: `setWindowFlags()` dalam constructor adalah PyQt6 bug; QFrame parent tidak reliable  
**Fix**: Parent=None, `setWindowFlags()` setelah konstruksi, manual centering

---

## Arsitektur Agent (10 Agents Total, 3 Crews)

### BrowserCrew (3 agents — hierarchical)
```
Navigator → Scraper → Analyst
```
Tools: 11 browser tools

### ShopeeCrew (3 agents — sequential)
```
ShopeeNavigator → FinancialAnalyst → AdsOptimizer
```
Tools: 11 browser tools + 3 ads tools

### SpyCrew (4 agents — sequential, memory+planning enabled)
```
MarketScanner → CompetitorProfiler → TrendDetector → StrategySynthesizer
```
Tools: 11 browser tools + 5 spy tools

---

## Navigasi yang Aman (v1.3.1)

| State Saat Ini | Klik | Hasil |
|---------------|------|-------|
| Spy active | ⚙️ Settings | Dialog muncul di atas — chat preserved |
| Spy active | 🤖 Crew / 📊 Analytics | Panel terbuka — chat preserved |
| Spy active | 🌐 Browser / 📢 Ads | Diblokir — return ke spy chat |
| Ads active | 🕵️ Spy | Switch ke SpyAgent ✅ |
| Ads active | 🌐 Browser | Browser kembali |
| Ads active | 🤖 Crew / 📊 Analytics | Diblokir — return ke ads chat |
| Any state | 🔧 Settings | Settings dialog (non-blocking) |

---

## Build Process (3 langkah, jangan di-chain)

```powershell
# 1. PyInstaller build (~150 detik)
python -m PyInstaller shopeeagent.spec --noconfirm

# 2. Copy data files (535+ files dari 7 packages)
powershell -ExecutionPolicy Bypass -File copy_all_data.ps1

# 3. NSIS installer (~60 detik, hasil: 213 MB)
& "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

Output: `ShopeeAgent-Setup.exe` (~213 MB) — single-file, self-contained.

---

## Referensi
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) — 17 error pattern dengan fix permanen
- [CHANGELOG.md](CHANGELOG.md) — Riwayat perubahan lengkap
- [requirement.md](requirement.md) — Spesifikasi requirement
- [README.md](README.md) — User-facing documentation
