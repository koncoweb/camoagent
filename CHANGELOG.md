# Changelog

All notable changes to this project will be documented in this file.

## [1.3.1] - 2025-06-04

### Fixed
- **Spy agent blocked during ads session**: Ads session guard now allows `"spy"` icon — user can switch from ads to spy agent without restarting
- **Browser not launching after switch**: `BrowserManager.launch_browser()` force-closes previous thread with 4s timeout, sets `_thread = None` before new launch
- **Browser close timeout**: `close()` timeout increased from 2s to 8s, sets `_thread = None` after join

---

## [1.3.0] - 2025-06-04

### Added
- **Version in window title bar**: `ShopeeAgent v1.3.0` displayed in title bar
- **Category picker UI**: 14 Shopee category buttons + custom input before spy agent launch
- **Animated loading indicator**: Spinner (◌○◎◉●) pinned above chat area, visible during agent execution
- **Centralized status handling**: `_on_crew_status()` manages panels + loading UI from one handler
- **Camoufox status card**: Live browser state in Crew panel (Connected/Disconnected, engine, stealth, locale, session)

### Changed
- **Elegant UI**: Dark sidebar (#2B2B2B) + single blue accent (#4A90D9) replacing orange-heavy Shopee theme
- **Sidebar icons**: 🌐 browser, 📢 ads, 🕵️ spy, ⚙️ crews, 📊 analytics, 🔧 settings
- **CrewPanel rebuilt**: 3 crew cards (BrowserCrew, ShopeeCrew, SpyCrew) with process badges and agent tool counts
- **Spy agent timeout**: All 4 agents now `max_execution_time=600` (was 180-300s)
- **Unified icon**: `shopeeagentcrop.ico` for EXE, installer, taskbar, title bar

### Fixed
- **Loading indicator not appearing**: `QMetaObject.invokeMethod()` → `signal.emit()` — cross-thread signal now works
- **Loading indicator scrolls away**: Pinned outside scroll area, always visible
- **Chat bubbles truncated**: `SelfSizingTextEdit` with dynamic `sizeHint()`, proper word-wrap containers
- **Settings dialog invisible**: Parent-less QDialog with manual centering + `.show()`
- **Session-locked navigation**: Crew/Analytics panels blocked during spy/ads sessions
- **Browser stability**: Camoufox launch retry 3x, page load retry, 30s health check

---

## [1.2.0] - 2025-06-04

### Added
- SpyAgent v2.0: Market Intelligence & Competitor Analysis
- Structured DOM extraction (16 fields)
- ReviewMinerTool, StoreProfilerTool, KeywordExtractorTool
- SpyAgent Action Bar UI (4 action buttons)
- Settings dialog + API key persistence to `.env`
- Session-aware navigation

### Changed
- Browser launch with Indonesian locale

### Fixed
- Tooltip/modal text invisible (global stylesheet fix)
- Browser timeout on shopee.co.id
- NSIS icon format

---

## [1.1.0] - 2025-06-01

### Added
- SpyAgent v1.0: Initial market research agent
- Chat separation with context headers

---

## [1.0.0] - 2025-06-01

### Added
- Initial release
- Shopee Browser (Camoufox + Playwright)
- Shopee Ads Management (3 agents + auto-pagination)
- Session persistence
