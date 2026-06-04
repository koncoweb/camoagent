# ShopeeAgent — Developer Guide

## Recurring Error Patterns & Fixes

**Purpose:** This document captures ALL recurring errors encountered during development.  
**Rule:** Check this guide FIRST before attempting any fix. Never repeat the same debugging cycle twice.

---

## ⚡ QUICK REFERENCE — Build Command

```powershell
# FULL BUILD - always run these 4 commands in EXACT order
Remove-Item -Path "dist","build" -Recurse -Force -ErrorAction SilentlyContinue
python -m PyInstaller shopeeagent.spec --noconfirm
powershell -ExecutionPolicy Bypass -File copy_all_data.ps1
& "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

| Rule | Why |
|------|-----|
| DON'T pipe PyInstaller to `Select-Object` | It makes the command appear "stuck" — causes repeated CheckCommandStatus calls |
| DON'T chain `Remove-Item` + `PyInstaller` + `makensis` in one `&&` | NSIS hangs in chained commands |
| DO run `copy_all_data.ps1` AFTER every PyInstaller build | 535+ data files from 7 packages are needed |
| DO use `--noconfirm` not `--clean --noconfirm` | `--clean` is slow, only use if cache is corrupted |

---

## 🔴 ERROR 1: PyInstaller — Missing Data Files

### Symptom
```
FileNotFoundError: No such file or directory: '...\\_internal\\crewai\\translations\\en.json'
FileNotFoundError: No such file or directory: '...\\_internal\\apify_fingerprint_datapoints\\data\\input-network-definition.zip'
FileNotFoundError: No such file or directory: '...\\_internal\\camoufox\\browserforge.yml'
FileNotFoundError: No such file or directory: '...\\_internal\\language_tags\\data\\json\\index.json'
```

### Root Cause
PyInstaller only bundles `.py`/`.pyc` files. Non-code data files (`.json`, `.zip`, `.yml`) are NOT auto-collected.

### Fix (PERMANENT)
**RUN `copy_all_data.ps1` after EVERY PyInstaller build.** This copies ALL non-Python files from 7 packages:

| Package | Files | Type |
|---------|-------|------|
| camoufox | 8 | `.yml`, config |
| browserforge | 2 | data files |
| apify_fingerprint_datapoints | 8 | `.zip`, `.json` |
| language_tags | 14 | `.json` data |
| crewai | 31 | translations, configs |
| click | 1 | config |
| playwright | 471 | drivers, assets |
| **TOTAL** | **535** | |

### DO NOT
- Try to fix this by adding individual files to `shopeeagent.spec` one by one
- Manually copy single files when you see the error
- Use `collect_data_files()` in the spec — it's unreliable for complex packages

---

## 🔴 ERROR 2: Browser Timeout — shopee.co.id

### Symptom
```
playwright._impl._errors.TimeoutError: Page.goto: Timeout 30000ms exceeded.
  - navigating to "https://shopee.co.id/", waiting until "load"
```

### Root Cause
Shopee.co.id is heavy (many scripts, images, CDN). Default Playwright timeout is 30 seconds with `wait_until="load"` which waits for ALL resources.

### Fix (in `services/browser_manager.py` line 112)
```python
# ✅ CORRECT - dual fallback
try:
    self._page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
except Exception:
    self._page.goto(target_url, wait_until="commit", timeout=30000)
```

### DO NOT
- Use `goto(url)` without `wait_until` parameter
- Set `timeout=0` (infinite — will hang forever)
- Set `wait_until="load"` for Shopee

---

## 🔴 ERROR 3: PyInstaller Icon — .ico vs .png on Windows

### Symptom
App EXE and desktop shortcut show default icon, not custom `logoicon.png`.

### Root Cause
PyInstaller on Windows **requires `.ico` format** for the `icon=` parameter. `.png` is silently ignored.

### Fix
```python
# shopeeagent.spec — ✅ CORRECT
exe = EXE(
    ...,
    icon='shopeeagentcrop.ico',  # .ico NOT .png
)

# installer.nsi — ✅ CORRECT
!define MUI_ICON "shopeeagentcrop.ico"
!define MUI_UNICON "shopeeagentcrop.ico"
```

### DO NOT
- Use `.png` in the `icon=` parameter
- Forget to update BOTH the spec AND the NSIS script

---

## 🔴 ERROR 4: Qt Stylesheet "Unknown property filter"

### Symptom
Console shows 30+ lines of:
```
Unknown property filter
Unknown property filter
...
```

### Root Cause
CSS `filter: brightness(...)` is not supported in Qt Stylesheets (it's a web CSS property, not Qt CSS).

### Fix
Replace `filter: brightness(1.2)` with a valid Qt alternative:
```python
# ❌ WRONG
"QPushButton:hover { filter: brightness(1.2); }"

# ✅ CORRECT
"QPushButton:hover { background-color: #333333; }"
```

---

## 🔴 ERROR 5: PowerShell Variable Interpolation

### Symptom
```
Variable reference is not valid. ':' was not followed by a valid variable name character.
```

### Root Cause
PowerShell treats `$_` in double-quoted strings as variable interpolation. When followed by `:` (e.g., `"$_:"`) it breaks.

### Fix
```powershell
# ❌ WRONG
Write-Host "$_: $count files"

# ✅ CORRECT
Write-Host "${_}: ${count} files"
# OR use string concatenation
Write-Host ($_ + ": " + $count + " files")
```

### Affected Contexts
- `ForEach-Object` blocks using `Write-Host`
- Any string with `$_` followed by `:`
- Pipe output inside string templates

---

## 🔴 ERROR 6: NSIS `makensis` Hanging

### Symptom
`makensis.exe` appears to hang — no output for minutes.

### Root Cause
NSIS is actually running but output is buffered. When chained after other commands in PowerShell, it sometimes gets stuck waiting for stdin.

### Fix
```powershell
# ✅ CORRECT — run NSIS as standalone command
& "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi

# ❌ WRONG — chained commands may hang
powershell -File copy.ps1; makensis installer.nsi; Get-ChildItem ...
```

### DO NOT
- Chain NSIS after other commands using `;`
- Use `Select-Object -Last` on makensis output
- Run makensis inside `powershell -File` scripts

---

## 🔴 ERROR 7: Chat Session Mixing (Spy vs Ads Agent)

### Symptom
User clicks Spy Agent after Ads Agent — chat shows old Ads messages mixed with new Spy messages.

### Root Cause
Both agents share the same ChatWidget without session state management.

### Fix (in `ui/main_window.py`)
```python
# Add session flags
self._spy_session_active = False
self._ads_session_active = False

# In on_icon_clicked():
# Settings → dialog (not stacked widget)
if icon_name == "settings":
    self._open_settings_dialog()
    return

# Crew/Analytics → panels without clearing chat
if icon_name in ("crew", "analytics"):
    self.stacked_widget.setCurrentWidget(self.crew_panel)  # or analytics_panel
    return

# Spy/Ads active → clicking other icons = return to chat (not clear)
if self._spy_session_active and icon_name != "spy":
    self.stacked_widget.setCurrentWidget(self.chat_widget)
    return
```

### Navigation Rules:
| Current State | Click | Result |
|---------------|-------|--------|
| Spy active | Settings | Settings dialog OVER chat (chat preserved) |
| Spy active | Crew/Analytics | Show panel (chat preserved) |
| Spy active | Ads/Browser | **BLOCKED** — return to spy chat |
| Ads active | Spy | Switch to Spy (clear ads state) |
| Any state | Browser | Clear all, fresh start |

---

## 🔴 ERROR 8: Settings / API Key Not Persisting

### Symptom
API key entered in Settings → disappears after app restart.

### Root Cause
`os.environ["KEY"] = value` only sets for current process. Does NOT write to `.env` file.

### Fix (in `ui/panels.py`)
```python
def _save_to_env_file(self, sumpod_key, openai_key):
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    
    # Read existing lines
    env_lines = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    env_lines[k.strip()] = v.strip()
    
    # Update keys
    if sumpod_key:
        env_lines["SUMOPOD_API_KEY"] = sumpod_key
    if openai_key:
        env_lines["OPENAI_API_KEY"] = openai_key
    
    # Write back
    with open(env_path, "w") as f:
        for k, v in env_lines.items():
            f.write(f"{k}={v}\n")
```

---

## 🔴 ERROR 9: PyInstaller Terminal Appears Stuck

### Symptom
`python -m PyInstaller ... | Select-Object -Last 3` shows no output for minutes.

### Root Cause
PyInstaller produces many log lines. `Select-Object -Last 3` buffers ALL output and only shows the last 3 — making the build appear stuck.

### Fix
```powershell
# ✅ CORRECT — let PyInstaller produce full output
python -m PyInstaller shopeeagent.spec --noconfirm

# ❌ WRONG — hides progress, triggers repeated CheckCommandStatus
python -m PyInstaller ... | Select-Object -Last 3
```

### Build Wait Strategy
- PyInstaller takes ~150 seconds on this project
- Don't poll with `CheckCommandStatus` every 2 seconds
- Wait 300 seconds (5 min) before first check
- Then wait 600 seconds (10 min) increments

---

## 🔴 ERROR 10: SettingsPanel Not Closable Without Losing Chat

### Symptom
Settings was a QFrame in QStackedWidget. Switching to Settings = chat panel disappeared.

### Fix
```python
# ❌ WRONG — SettingsPanel as QFrame in stacked widget
class SettingsPanel(QFrame):
    ...

# ✅ CORRECT — SettingsPanel as standalone QDialog
from PyQt6.QtWidgets import QDialog
class SettingsPanel(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
```

In `main_window.py`:
```python
def _open_settings_dialog(self):
    dialog = SettingsPanel(self)
    dialog.settings_changed.connect(self.on_settings_changed)
    dialog.exec()  # modal — blocks until user closes
```

---

## 🔴 ERROR 11: Tooltip Text Color (White on Light)

### Symptom
Tooltip text is invisible — white text on light yellow background.

### Root Cause
System default QToolTip style uses light text. Need global app stylesheet override.

### Fix (in `camoagent.py`, QApplication subclass)
```python
app.setStyleSheet("""
    QToolTip {
        color: #1A1A1A;
        background-color: #FFF8E1;
        border: 1px solid #EE4D2D;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 12px;
    }
    QMessageBox QLabel {
        color: #1A1A1A;
        font-size: 13px;
    }
""")
```

---

## ✅ BUILD CHECKLIST

Before declaring "build complete", verify:

- [ ] `dist\ShopeeAgent\ShopeeAgent.exe` exists
- [ ] `dist\ShopeeAgent\_internal\crewai\translations\en.json` exists
- [ ] `dist\ShopeeAgent\_internal\apify_fingerprint_datapoints\data\` has 5 files
- [ ] `dist\ShopeeAgent\_internal\camoufox\browserforge.yml` exists
- [ ] `dist\ShopeeAgent\_internal\language_tags\data\json\index.json` exists
- [ ] `dist\ShopeeAgent\_internal\playwright\` folder exists with files
- [ ] `copy_all_data.ps1` was run after PyInstaller
- [ ] NSIS `makensis` ran with exit code 0
- [ ] `ShopeeAgent-Setup.exe` timestamp is newer than `dist\ShopeeAgent\ShopeeAgent.exe`

---

## 📁 PROJECT FILE MAP

| File | Purpose | Key Functions |
|------|---------|---------------|
| `camoagent.py` | Entry point, QApplication subclass | `ShopeeAgentApp`, global stylesheet |
| `shopeeagent.spec` | PyInstaller build config | `datas=`, `icon=`, `hiddenimports=`, `EXE()`, `COLLECT()` |
| `installer.nsi` | NSIS installer script | Registry keys, shortcuts, uninstaller |
| `copy_all_data.ps1` | Post-build data copier | Copies 535+ files from 7 packages |
| `ui/main_window.py` | Main window UI | `MainWindow`, `ChatWidget`, `IconBar`, `StatusPanel` |
| `ui/panels.py` | Side panels + settings dialog | `CrewPanel`, `AnalyticsPanel`, `SettingsPanel` |
| `services/browser_manager.py` | Camoufox browser lifecycle | `launch_browser()`, `_run_browser()`, locale config |
| `services/crew_executor.py` | Crew execution threads | `execute_spy_task()`, `execute_shopee_ads_task()` |
| `crews/spy_crew.py` | SpyAgent crew definition | `SpyCrew` with 4 agents, 4 tasks |
| `crews/shopee_crew.py` | Ads crew definition | `ShopeeCrew` with 3 agents, 3 tasks |
| `tools/spy_tools.py` | SpyAgent tools | `MarketScanTool`, `ReviewMinerTool`, `StoreProfilerTool`, `GapAnalyzeTool` |
| `tools/shopee_tools.py` | Ads tools | `ExtractShopeeAdsMetricsTool`, `CalculateActualFinancialsTool` |
| `tools/browser_tool.py` | Browser command tools | `BrowserConfig`, command queue, all browser actions |
| `config/spy_agents.yaml` | SpyAgent agent definitions | 4 agents |
| `config/spy_tasks.yaml` | SpyAgent task definitions | 4 tasks |
| `config/shopee_agents.yaml` | Ads agent definitions | 3 agents |
| `config/shopee_tasks.yaml` | Ads task definitions | 3 tasks |
| `copy_all_data.ps1` | Post-build data copier | 535 files from 7 packages |
| `shopeeagent.md` | Developer changelog (ID) | 7 critical lessons, architecture, navigation |
| `DEVELOPER_GUIDE.md` | This file | 17 error patterns + build checklist |
| `CHANGELOG.md` | Release changelog (EN) | Structured by version |
| `requirement.md` | Project requirements | Full feature specification |
| `README.md` | User-facing README | Features, quick start |

---

## 🚀 VERSIONING

Current version: **v1.3.2**

Files to update when bumping version:
1. `camoagent.py` → `self.setApplicationVersion("X.Y.Z")`
2. `installer.nsi` → `VIAddVersionKey "FileVersion" "X.Y.Z"`
3. `installer.nsi` → `VIAddVersionKey "ProductVersion" "X.Y.Z"`
4. `installer.nsi` → `WriteRegStr ... "DisplayVersion" "X.Y.Z"`
5. `ui/main_window.py` → `self.setWindowTitle("ShopeeAgent vX.Y.Z")`
6. `README.md` → `# ShopeeAgent vX.Y.Z`
7. `requirement.md` → `**ShopeeAgent vX.Y.Z**`
8. `CHANGELOG.md` → `## [X.Y.Z] - YYYY-MM-DD`
9. `DEVELOPER_GUIDE.md` → `Current version: **vX.Y.Z**`
10. `shopeeagent.md` → `# ShopeeAgent vX.Y.Z`
11. `ShopeeAgent-Setup-README.txt` → `SHOPEAGENT vX.Y.Z`

---

## 📦 DISTRIBUTION

Single-file distribution: **`ShopeeAgent-Setup.exe`** (~213 MB) is all you need.

- NSIS compiles ALL files (EXE, DLLs, 535+ data files, icon) into one self-contained installer
- No external dependencies — user does NOT need Python, pip, or any runtime
- Installer creates `.env` template and `README_FIRST.txt` at install location
- Uninstaller included and registered in Windows Control Panel

---

## 🔴 ERROR 12: Chat Bubbles — Text Always Truncated

### Symptom
Agent messages selalu terpotong. User hanya melihat 2-3 baris pertama, sisanya hilang.

### Root Cause
```python
# ❌ WRONG — height dihitung SEBELUM widget dirender
doc = msg_widget.document()
doc.setTextWidth(410)
height = int(doc.size().height()) + 28  # doc.size() return 0 atau nilai stale
msg_widget.setFixedHeight(height)
```

`QTextEdit.document().size().height()` tidak akurat sebelum widget dirender oleh layout manager Qt. Hasilnya: tinggi 28px (margin saja) atau wildly inaccurate → teks terpotong.

### Fix
```python
# ✅ CORRECT — SelfSizingTextEdit subclass
class SelfSizingTextEdit(QTextEdit):
    def sizeHint(self) -> QSize:
        doc = self.document()
        doc.setTextWidth(self._text_width)
        width = max(self._text_width + 20, int(doc.idealWidth()) + 10)
        height = int(doc.size().height()) + self._margin
        return QSize(width, height)
    
    def _on_content(self):
        self.updateGeometry()  # trigger re-layout setiap konten berubah
```

`sizeHint()` dipanggil Qt saat layout perlu ukuran — nilainya selalu dinamis dari `document.size()` terbaru.

### Also Fixed (same bug, user bubbles)
```python
# ❌ WRONG — QLabel langsung di chat_layout dengan AlignRight
# Tidak ada konteks lebar → word wrap tidak bekerja
chat_layout.addWidget(bubble, 0, Qt.AlignmentFlag.AlignRight)

# ✅ CORRECT — container dengan stretch
container_layout.addStretch()  # dorong bubble ke kanan
container_layout.addWidget(bubble)  # bubble dapat lebar penuh dari chat_layout
```

---

## 🔴 ERROR 13: Loading Indicator Never Appears

### Symptom
Log menunjukkan "Spy Crew working" tapi loading spinner tidak muncul di chat. Tidak ada error.

### Root Cause
```python
# ❌ WRONG — QMetaObject.invokeMethod CANNOT emit pyqtSignal
def _safe_emit_status(self, agent: str, status: str):
    QMetaObject.invokeMethod(
        self, "status_update",        # ← ini nama signal, bukan method
        Qt.ConnectionType.QueuedConnection,
        Q_ARG(str, agent),
        Q_ARG(str, status)
    )
```

`QMetaObject.invokeMethod()` hanya bisa memanggil **method** / **slot**. Signal bukan method — signal di PyQt6 hanya bisa di-emit via `.emit()`. Exception dari invokeMethod di-swallow oleh `except Exception: pass` → silent failure.

### Fix
```python
# ✅ CORRECT — signal.emit() dari worker thread
# PyQt auto-queues cross-thread signals (Qt.QueuedConnection is default for signals)
def _safe_emit_status(self, agent: str, status: str):
    try:
        self.status_update.emit(agent, status)
    except Exception:
        pass
```

### Related: Loading Indicator Scrolls Away
`LoadingWidget` sebelumnya di dalam `chat_layout` (scrollable). Saat chat baru muncul dan auto-scroll ke bawah, indicator ikut ter-scroll keluar viewport → user tidak lihat.

**Fix**: Pindahkan `LoadingWidget` ke LAYOUT UTAMA `ChatWidget` — antara action bar dan QScrollArea. Posisinya tetap, tidak terpengaruh scroll.

---

## 🔴 ERROR 14: Spy Browser Not Launching After Ads Session

### Symptom
Sequence: Browser 🌐 → Ads 📢 agent running → click Spy 🕵️ → **browser tidak terbuka**. Tidak ada error log.

### Root Cause #1 — Session Guard Blocking
```python
# ❌ WRONG — spy tidak diizinkan saat ads session
if self._ads_session_active and icon_name not in ("ads", "browser"):
    return  # ← "spy" diblokir, tidak pernah sampai ke _handle_spy_agent_click
```

### Root Cause #2 — Thread Deadlock
```python
# ❌ WRONG — launch_browser silent return
def launch_browser(self, ...):
    if self._thread is not None and self._thread.is_alive():
        return  # ← thread lama masih winding down → tidak launch apapun
```

Camoufox cleanup (context manager exit + session save) bisa lebih dari 2 detik. `close()` hanya join 2 detik → thread lama masih `is_alive()` → `launch_browser()` return tanpa action.

### Fix
```python
# main_window.py — ✅ CORRECT
if self._ads_session_active and icon_name not in ("ads", "browser", "spy"):
    return  # spy diizinkan

# browser_manager.py — ✅ CORRECT
def launch_browser(self, ...):
    with self._lock:
        # Force-close thread lama SEBELUM launch baru
        if self._thread is not None and self._thread.is_alive():
            self._running = False
            self._thread.join(timeout=4)
            self._thread = None
            self._browser = None
            self._page = None
            self._command_queue = None
        # Now launch fresh
        self._target_url = target_url
        self._thread = threading.Thread(target=self._run_browser, ...)
        self._thread.start()

def close(self):
    with self._lock:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=8)  # naik dari 2
            self._thread = None           # penting: null-kan referensi
```

---

## 🔴 ERROR 15: QDialog Invisible on QFrame Parent

### Symptom
Settings dialog tidak muncul sama sekali. `dialog.show()` dipanggil, tidak ada error.

### Root Cause
`MainWindow` extends `QFrame`, bukan `QMainWindow`. QDialog dengan parent QFrame tidak bisa dijamin muncul sebagai foreground window.

Selain itu, `setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)` di constructor adalah **PyQt6 bug yang terdokumentasi** — memodifikasi window flags SEBELUM `show()` bisa membuat dialog invisible di Windows.

### Fix
```python
# ✅ CORRECT — 3 langkah
# 1. Parent = None (top-level window, tidak bergantung pada QFrame)
dialog = SettingsPanel(None)

# 2. setWindowFlags SETELAH constructor (bukan di dalam constructor)
dialog.setWindowFlags(
    Qt.WindowType.Dialog |
    Qt.WindowType.WindowCloseButtonHint |
    Qt.WindowType.WindowTitleHint
)

# 3. Manual centering
main_geo = self.geometry()
dw, dh = dialog.width(), dialog.height()
x = main_geo.x() + (main_geo.width() - dw) // 2
y = main_geo.y() + (main_geo.height() - dh) // 2
dialog.move(max(0, x), max(0, y))
dialog.show()
```

---

## 🔴 ERROR 16: Chat Bubble Width Collapsed (60px)

### Symptom
Agent bubble lebar 60px — teks sangat sempit, wrap berlebihan, tidak terbaca.

### Root Cause
```python
# ❌ WRONG — setAlignment forces widget to sizeHint width
container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
```

`setAlignment(AlignLeft)` di QHBoxLayout membuat widget berada tepat di ukuran `sizeHint()`-nya — tidak ada stretch ke kanan. Jika `sizeHint().width()` = 60px (dari `doc.idealWidth()` untuk teks pendek) → bubble = 60px.

```python
# ❌ ALSO WRONG — sizeHint width terlalu kecil
def sizeHint(self):
    ideal = int(doc.idealWidth()) + 10  # doc.idealWidth() bisa 50px untuk teks pendek
    return QSize(min(ideal, 500), height)  # hasil: 60px
```

### Fix
```python
# ✅ CORRECT — addStretch untuk alignment, bukan setAlignment
clayout.addWidget(msg_widget)
clayout.addStretch()  # widget di kiri, stretch isi ruang kanan

# ✅ CORRECT — sizeHint width diklamp ke minimum yang masuk akal
def sizeHint(self):
    width = max(self._text_width + 20, int(doc.idealWidth()) + 10)  # tidak < 430px
    return QSize(width, height)
```

| Pattern | Hasil |
|---|---|
| `setAlignment(AlignLeft)` | Widget fixed di ukuran `sizeHint()` — sempit |
| `addStretch()` | Widget di kiri, stretch mengisi ruang — lebar sesuai `sizeHint` |

---

## 🔴 ERROR 17: `parent_layout.count()` AttributeError on QWidget

### Symptom
```
AttributeError: 'ChatWidget' object has no attribute 'count'
```

### Root Cause
`self.message_input.parent()` returns the `QWidget` (parent widget), not the `QLayout`. `QWidget` doesn't have `.count()` — only `QLayout` does.

### Fix
```python
# ❌ WRONG
parent_layout = self.message_input.parent()  # returns QWidget, not layout
parent_layout.count()  # AttributeError

# ✅ CORRECT — simpan layout reference sebagai class attr
self._input_layout = input_layout  # simpan saat setup_ui
...
if hasattr(self, '_input_layout') and self._input_layout:
    input_layout = self._input_layout
    input_layout.count()  # QLayout.count() — benar
```
