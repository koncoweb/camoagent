# ShopeeAgent - Project Requirements

## Overview
**ShopeeAgent v1.3.2** is a Desktop GUI application built with PyQt6 that integrates a stealth browser (Camoufox/Playwright) with a multi-agent AI system (CrewAI) for Shopee store management, ads optimization, and **market intelligence & competitor analysis**.

## Core Dependencies
| Package | Purpose |
|---------|---------|
| **PyQt6** | Desktop graphical user interface |
| **CrewAI** | Multi-agent AI orchestration with Memory & Planning |
| **Camoufox** | Stealth browser automation with anti-bot evasion |
| **BrowserForge** | Anti-detect fingerprinting data |
| **OpenAI SDK** | API interaction with SumoPod AI or OpenAI |
| **Markdown** | Parse markdown to HTML for chat interface |
| **Playwright** | Browser automation (bundled with Camoufox) |

## Core Features

### 1. Shopee Browser Automation
- **Camoufox** with `humanize=True` for human-like mouse movements
- **BrowserForge fingerprinting** for anti-detect capabilities
- **Session Persistence** using Playwright storage_state to avoid re-login
- **Auto-save** session when browser closes
- **Thread-safe Command Queue** for cross-thread communication
- **Dual URL support**: `seller.shopee.co.id` (Ads) or `shopee.co.id` (Spy — guest mode)
- **Indonesian locale**: `locale="id-ID"` for Bahasa Indonesia content
- **Timeout resilience**: `domcontentloaded` (60s) → `commit` (30s) fallback

### 2. Shopee Ads Management (📢)
- **3 specialized agents**: Navigator, Financial Analyst, Ads Optimizer
- Extract advertising metrics from Shopee Seller Center
- Financial calculations: PPN 11%, Actual ROAS, Break-Even ROAS, Max CPC, Net Profit
- Performance classification: Bagus (>Target ROAS), Cukup (Between), Rugi (<Break-Even)
- Bid optimization recommendations
- Automatic pagination across ALL pages

### 3. SpyAgent — Market Intelligence (🕵️) v1.3.0
- **4 specialized agents with 5 custom tools**:
  - MarketScanner — Structured DOM extraction
  - CompetitorProfiler — Store & price analysis
  - TrendDetector — Bestsellers & review mining
  - StrategySynthesizer — Full market intelligence report
- **5 Spy Tools**:
  - `MarketScanTool` — 16-field structured JSON per product
  - `ReviewMinerTool` — Pain points (1-2★) & strengths (4-5★)
  - `StoreProfilerTool` — Name, rating, followers, badges
  - `GapAnalyzeTool` — Underserved niches + price gaps
  - `KeywordExtractorTool` — Competitor listing keywords
- **Memory + Planning**: Enabled for deeper analysis
- **Guest mode**: No login needed, scans as regular buyer

### 4. Shopee-Themed UI/UX
- **Sidebar Navigation**: Browser, Ads, Spy, Crew, Analytics, Settings
- **Spy Agent category selection**: Before launching, user picks a Shopee category from 14 popular buttons (Handphone, Fashion, Kecantikan, dll) or types a custom category. Category context injected into all agent tasks for focused analysis.
- **Loading indicator**: Animated spinner widget (◌○◎◉●) appears when any CrewAI agent is "working" — hides automatically on "ready" or "error". Works for both spy and ads workflows.
- **Settings as top-level dialog**: Parent-less QDialog with manual centering — works reliably with QFrame-based main window. Uses `.show()` so agent execution continues undisturbed.
- **Session-locked navigation**: During spy/ads sessions, sidebar clicks (Crew, Analytics) redirect to chat instead of switching panels — prevents accidental session disruption
- **Crew Management panel**: Displays all 3 CrewAI crews (BrowserCrew, ShopeeCrew, SpyCrew) with process type badges, Memory/Planning status, per-agent role with tool counts
- **Camoufox status card**: Real-time browser state (Connected/Disconnected), engine info, stealth config, locale, session path — updated via browser_manager signals
- **Unified dark labels (`#1A1A1A`)**: All panel labels, form labels, and group box titles use standard dark text — no more faded grays
- **Card-style Analytics**: 3 metric cards (Tasks/Errors/Est. Tokens) with large bold numbers and accent colors — never overlap
- **Clean QGroupBox**: Single-pixel border (`#D0D0D0`), proper `subcontrol-position: top left` — titles never overlap content
- **SpyAgent Action Bar**: 4 color-coded buttons above chat
- **Chat Interface**: Markdown rendering with dynamic height
- **Status Panel**: Real-time logging and agent activity tracking
- **Global stylesheet**: Tooltips & modals use dark text on light background

## Settings & Persistence (v1.2.1)
- API keys saved to `.env` file (survive app restart)
- Settings dialog as standalone non-modal QDialog (`.show()` not `.exec()`)
- Settings re-opens existing dialog if already open (singleton pattern)
- 100% non-blocking: Settings never interrupts spy/ads agent execution

## Full Tool Inventory

### Browser Tools (11 tools)
| Tool | Function |
|------|----------|
| `GetCurrentPageInfoTool` | Get current URL and title |
| `NavigateToUrlTool` | Navigate to a specific URL |
| `GetPageContentTool` | Get raw HTML content |
| `GetPageTextTool` | Get clean innerText |
| `ScrollDownTool` | Scroll for lazy-loaded content |
| `ClickElementTool` | Click element by CSS selector |
| `TypeTextTool` | Type text into input fields |
| `PressKeyTool` | Send keyboard keys |
| `EvaluateJSTool` | Execute custom JavaScript |
| `DismissDialogTool` | Multi-strategy modal closer |
| `SaveSessionTool` | Save browser session |

### Ads Tools (3 tools)
| `ExtractShopeeAdsMetricsTool` | Extract ads metrics + auto-pagination |
| `CalculateActualFinancialsTool` | ROAS, Break-Even, Max CPC, Net Profit |
| `GenerateAdsRecommendationTool` | Bid optimization recommendations |

### SpyAgent Tools (5 tools) NEW
| `MarketScanTool` | Structured DOM extraction, 16 fields, auto-pagination |
| `ReviewMinerTool` | Customer review sentiment analysis |
| `StoreProfilerTool` | Store metrics, badges, followers |
| `GapAnalyzeTool` | Niche opportunity detection |
| `KeywordExtractorTool` | Competitor keyword intelligence |

## Crew Agents

### Shopee Ads Crew (3 agents)
- **ShopeeNavigator**: Extracts data from Shopee pages
- **FinancialAnalyst**: Calculates ROAS, Break-Even, Max CPC
- **AdsOptimizer**: Generates bid recommendations

### Spy Crew (4 agents) NEW
- **MarketScanner**: DOM extraction + browser navigation
- **CompetitorProfiler**: Gap analysis + keyword intelligence
- **TrendDetector**: Bestsellers + review mining
- **StrategySynthesizer**: Full market intelligence report

## Configuration Files
- `.env`: API keys and endpoint (auto-saved from Settings)
- `config/shopee_agents.yaml`: Ads agent definitions
- `config/shopee_tasks.yaml`: Ads task definitions
- `config/spy_agents.yaml`: SpyAgent agent definitions NEW
- `config/spy_tasks.yaml`: SpyAgent task definitions NEW

## Installation & Build

### Requirements
- Windows 10/11
- Python 3.10+
- Internet connection (first run downloads Camoufox browser)
- API key (SumoPod AI or OpenAI)

### Build Process
```batch
pip install -r requirements.txt
python -m PyInstaller shopeeagent.spec --noconfirm
powershell -ExecutionPolicy Bypass -File copy_all_data.ps1
makensis installer.nsi
```

### Build Output
| File | Size | Purpose |
|------|------|---------|
| `ShopeeAgent-Setup.exe` | ~204 MB | NSIS Installer |
| `dist/ShopeeAgent/` | ~580 MB | Portable folder |

## Recent Updates

### v1.3.1 (2025-06-04) — Bug Fixes & Stability
- Session guard: `"spy"` icon diizinkan saat ads session aktif
- BrowserManager: `launch_browser()` force-close thread lama, `close()` timeout 2→8 detik
- 17 error patterns terdokumentasi di DEVELOPER_GUIDE.md
- Distribusi: single-file `ShopeeAgent-Setup.exe` (213 MB)

### v1.3.0 (2025-06-04)
- Category picker: 14 Shopee category buttons + custom input sebelum spy agent
- Loading indicator: spinner animasi saat agent working (spy & ads)
- Crew Management panel: 3 crew cards + Camoufox status card
- Elegant UI: dark sidebar + single blue accent (#4A90D9)
- Chat bubbles auto-sizing fix (SelfSizingTextEdit)
- Session-locked navigation (Crew/Analytics blocked during spy/ads)
- Non-modal Settings dialog
- Spy agent timeout: 600s all agents
- Signal fix: QMetaObject.invokeMethod → signal.emit()
- Browser: Camoufox launch retry (3x) + health check (30s)
- Icon: shopeeagentcrop.ico (unified everywhere)
- Version in window title bar

### v1.2.0 (2025-06-04)
- SpyAgent v2.0: Market Intelligence & Competitor Analysis
- Structured DOM extraction (16 fields, no LLM parsing)
- ReviewMinerTool, StoreProfilerTool, KeywordExtractorTool
- Settings as standalone dialog — preserves chat state
- API key persistence to .env file
- Session-aware navigation (chat never cleared accidentally)
- Indonesian locale (locale="id-ID")
- Tooltip/modal text visibility fix
- DEVELOPER_GUIDE.md with 11 error patterns

### v1.1.0 (2025-06-01)
- SpyAgent v1.0 initial release
- Chat separation between agents
- Browser locale fix

### v1.0.0 (2025-06-01)
- Initial ShopeeAgent release
- Ads Management with 3 agents
- NSIS installer distribution
