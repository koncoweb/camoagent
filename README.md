# ShopeeAgent v1.3.1 — AI Shopee Manager

A powerful desktop application combining CrewAI multi-agent intelligence with Camoufox stealth browser for Shopee store management, ads optimization, and market intelligence.

![Version](https://img.shields.io/badge/Version-1.3.1-4A90D9?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)

## 🎯 Features

### 🛒 Browser Features
- **Camoufox** stealth browser — undetectable by Shopee anti-bot
- **Session auto-save** — login once, never again
- **Dual mode**: Seller Center (login) or Marketplace (guest)
- Indonesian locale (`id-ID`) for Bahasa Indonesia content
- Timeout-resilient navigation for heavy pages

### 📢 Shopee Ads Management
- 3 AI agents: Navigator → Financial Analyst → Ads Optimizer
- ROAS, Break-Even, Max CPC, Net Profit calculations with PPN 11%
- Performance classification: Bagus / Cukup / Rugi
- Auto-pagination across ALL pages

### 🕵️ SpyAgent — Market Intelligence (v1.3.0)
- 4 AI agents + 5 custom tools for competitor analysis
- **Structured DOM extraction** — 16 data fields per product in clean JSON
- **Review mining** — extract customer pain points & strengths
- **Store profiling** — rating, followers, product count, badges
- **Gap analysis** — find underserved niches with data justification
- Action bar UI with 4 color-coded buttons

### 🤖 AI Agents (7 total)
| Agent | Role | Crew |
|-------|------|------|
| 🛒 Navigator | Data extraction | Ads |
| 📊 Financial Analyst | ROAS/BE/Max CPC | Ads |
| 🎯 Ads Optimizer | Bid recommendations | Ads |
| 📡 Market Scanner | DOM extraction | Spy |
| 📈 Trend Detector | Bestsellers + reviews | Spy |
| 📊 Competitor Profiler | Store + price analysis | Spy |
| 🎯 Strategy Synthesizer | Full report | Spy |

### 🛠️ 19 Custom Tools
- **Browser tools** (11): navigate, scroll, click, type, JS, etc.
- **Ads tools** (3): extract metrics, calculate financials, generate recommendations
- **Spy tools** (5): market scan, review mine, store profile, gap analyze, keyword extract

### 🎨 UI/UX
- **Settings as standalone dialog** — never blocks your chat
- **Session-aware navigation** — switching panels preserves conversation
- **API key persistence** — saved to `.env`, survives restart
- Dark tooltip text on light background (readable!)
- Color-coded SpyAgent action bar
- Markdown-rendered chat with dynamic bubble height

## 📥 Installation

### NSIS Installer (Recommended)
```
1. Download ShopeeAgent-Setup.exe (~204 MB)
2. Run as Administrator
3. Launch from Desktop shortcut
```

### Portable Version
```
1. Extract dist/ShopeeAgent/ folder
2. Run ShopeeAgent.exe
3. No installation needed
```

## 🚀 Quick Start

### Ads Analysis
```
1. Click 🛒 → browser opens seller.shopee.co.id
2. Login to Shopee manually (auto-saved)
3. Navigate to Ads dashboard
4. Click 📢 → agents analyze your ads
```

### Market Research (SpyAgent)
```
1. Click 🕵️ → browser opens shopee.co.id (guest mode)
2. Search any product or browse a category
3. Click 📡 Scan or 🎯 Full Report in action bar
4. Receive comprehensive market intelligence report
```

### Settings
```
1. Click ⚙️ → dialog opens (chat preserved behind it)
2. Enter API key, select model
3. Click Apply → saved to .env permanently
4. Close dialog → back to your work
```

## 🏗️ Build from Source

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build executable
python -m PyInstaller shopeeagent.spec --noconfirm

# 3. Copy ALL data files (535+ files from 7 packages)
powershell -ExecutionPolicy Bypass -File copy_all_data.ps1

# 4. Build NSIS installer
& "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

| Output | Size |
|--------|------|
| `ShopeeAgent-Setup.exe` | ~204 MB |
| `dist/ShopeeAgent/` | ~580 MB |

> ⚠️ See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for common errors and build checklist.

## 🏗️ Architecture

```
ShopeeAgent
├── UI Layer (PyQt6)
│   ├── Icon Bar — Navigation (Browser, Ads, Spy, Crew, Analytics, Settings)
│   ├── Chat Widget — Command input & AI responses with action bar
│   ├── Status Panel — Real-time logs
│   └── Settings Dialog — Standalone modal window
│
├── Service Layer
│   ├── BrowserManager — Camoufox lifecycle & Playwright commands
│   └── CrewExecutor — Thread-safe agent execution
│
├── AI Layer (CrewAI)
│   ├── ShopeeCrew — 3 agents for ads analysis
│   └── SpyCrew — 4 agents for market intelligence
│
├── Tools Layer
│   ├── Browser tools (11) — Page interaction
│   ├── Ads tools (3) — Metrics & financials
│   └── Spy tools (5) — DOM extraction, reviews, store profiling
│
└── Config Layer
    ├── shopee_agents.yaml / shopee_tasks.yaml
    └── spy_agents.yaml / spy_tasks.yaml
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Error patterns & build guide |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [requirement.md](requirement.md) | Full requirements |
| [ShopeeAgent-Setup-README.txt](ShopeeAgent-Setup-README.txt) | End-user guide |
