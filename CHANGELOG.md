# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-06-04

### Added — SpyAgent v2.0: Market Intelligence & Competitor Analysis

- **🕵️ SpyAgent**: New market research agent for Shopee marketplace
  - Dedicated 🕵️ icon button in sidebar
  - Opens Camoufox to `shopee.co.id` (marketplace, guest mode — no login needed)
  - 4 specialized agents: MarketScanner, CompetitorProfiler, TrendDetector, StrategySynthesizer
  - 5 custom tools: MarketScanTool, ReviewMinerTool, StoreProfilerTool, GapAnalyzeTool, KeywordExtractorTool
  - Memory + Planning enabled for smarter analysis
  - Indonesian locale: `locale="id-ID"` in Camoufox config

- **Structured DOM Extraction (MarketScanTool v2)**
  - Replaced raw text extraction with JavaScript-based structured DOM extraction
  - 16 fields per product: name, price, original_price, sold, rating, store, location, is_ad, is_star_seller, discount, free_shipping, voucher, badge, product_url, image_url
  - Multi-selector fallback chain for Shopee DOM changes
  - Automatic pagination across ALL pages via Next button detection

- **ReviewMinerTool**: Extract customer reviews from product pages
  - Pain points from 1-2 star reviews
  - Strengths from 4-5 star reviews
  - Average rating and common complaint themes

- **StoreProfilerTool**: Deep store analysis
  - Store name, rating, followers, product count, joined date
  - Official/Star Seller badge detection
  - Chat performance score

- **SpyAgent Action Bar UI**
  - 4 action buttons above chat: 📡 Scan, 💬 Reviews, 🏪 Store, 🎯 Full Report
  - Color-coded buttons with tooltips
  - Auto-show/hide based on SpyAgent mode

### Changed — UX Improvements

- **Settings as standalone dialog**: No longer a stacked widget panel — opens as modal QDialog, chat preserved behind it
- **API key persistence**: Keys entered in Settings auto-save to `.env` file (survive app restart)
- **Session-aware navigation**: Chat preserved when switching between panels
  - `_spy_session_active` / `_ads_session_active` flags prevent accidental chat clearing
  - Crew/Analytics panels don't clear chat anymore
  - Klik 🕵️ saat spy active = return ke chat (not relaunch)

### Fixed

- **Tooltip text invisible**: Global QApplication stylesheet with `color:#1A1A1A`
- **Modal dialog text invisible**: QMessageBox QLabel stylesheet fix
- **Browser timeout on shopee.co.id**: `domcontentloaded` (60s) → `commit` (30s) fallback
- **CSS `filter:brightness` not supported in Qt**: Replaced with `background-color` hover
- **PowerShell `$_` interpolation errors** in ForEach-Object blocks

### Documentation

- **DEVELOPER_GUIDE.md**: 11 recurring error patterns documented with root causes and permanent fixes
- Full project file map with 20+ key files and their roles
- Build checklist with 9 verification points

---

## [1.1.0] - 2025-06-01

### Added
- **SpyAgent v1.0**: Initial market research agent
  - 🕵️ icon in sidebar
  - Camoufox to shopee.co.id with close-existing-browser prompt
  - 4 agents: MarketScanner, CompetitorProfiler, TrendDetector, StrategySynthesizer
  - MarketScanTool with pagination, GapAnalyzeTool for niche detection

- **Chat separation**: Clear chat + context header when switching agents

### Changed
- Browser launch: `locale="id-ID"` for Indonesian content

### Fixed
- NSIS icon not showing: Switched from `.png` to `.ico` format in spec + installer

---

## [1.0.0] - 2025-06-01

### Added
- **ShopeeAgent Branding**: Full rebrand from CamoAgent to ShopeeAgent
  - Shopee orange (#EE4D2D) and white color theme
  - Redesigned UI with Shopee brand colors

- **Shopee Ads Management**
  - 📢 icon button for Shopee Ads
  - 3 specialized AI agents: Navigator, Financial Analyst, Ads Optimizer
  - Custom tools: ExtractShopeeAdsMetricsTool, CalculateActualFinancialsTool, GenerateAdsRecommendationTool
  - Financial calculations: PPN 11%, Actual ROAS, Break-Even ROAS, Max CPC, Net Profit
  - Performance classification: Bagus (>Target ROAS), Cukup (Between), Rugi (<Break-Even)
  - Automatic pagination: Tool auto-detects and clicks "Next" across ALL pages

- **Browser Features**
  - Camoufox browser with stealth fingerprinting (anti-detection)
  - Session persistence using Playwright storage_state — login once, never again
  - Auto-save session when browser closes
  - Auto-navigate to https://seller.shopee.co.id

- **AI & CrewAI**
  - Dynamic LLM Provider selection (SumoPod AI vs OpenAI)
  - Multiple SumoPod models
  - Thread-safe command queue for Playwright cross-thread communication

- **Custom Tools** (14 tools)
  - Browser: GetCurrentPageInfoTool, NavigateToUrlTool, GetPageContentTool, GetPageTextTool, ScrollDownTool, ClickElementTool, TypeTextTool, PressKeyTool, EvaluateJSTool, DismissDialogTool, SaveSessionTool
  - Ads: ExtractShopeeAdsMetricsTool, CalculateActualFinancialsTool, GenerateAdsRecommendationTool

- **UI Panels**: Chat Widget, Crew Panel, Analytics Panel, Settings Panel

- **Distribution**: NSIS installer, portable version, build scripts

### Fixed
- Cross-threading errors with Playwright using asyncio.Queue
- Silent application crashes with robust exception catching
- Scrollbars in chat bubbles
- TargetClosedError with proper thread state management
- BrowserConfig duplicate class
- PyInstaller missing data files: apify_fingerprint_datapoints, crewai, camoufox, language_tags, playwright

---

## [0.1.0] - 2024

### Added
- Initial CamoAgent project
- Basic CrewAI browser automation
- PyQt6 desktop interface
