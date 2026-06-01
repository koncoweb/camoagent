# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-05-16

### Added
- **ShopeeAgent Branding**: Full rebrand from CamoAgent to ShopeeAgent
  - Shopee orange (#EE4D2D) and white color theme
  - Redesigned UI with Shopee brand colors
  - Updated window title and branding

- **Shopee Ads Management**
  - Shopee Ads Analysis feature with dedicated 📢 icon button
  - 3 specialized AI agents: Navigator, Financial Analyst, Ads Optimizer
  - Custom tools: ExtractShopeeAdsMetricsTool, CalculateActualFinancialsTool, GenerateAdsRecommendationTool
  - Financial calculations: PPN 11%, Actual ROAS, Break-Even ROAS, Max CPC, Net Profit
  - Performance classification: Bagus (>Target ROAS), Cukup (Between), Rugi (<Break-Even)
  - Sequential process for Shopee Crew with proper task chaining
  - Automatic pagination support: extracts data from ALL pages of Shopee ads table

- **Browser Features**
  - Camoufox browser with stealth fingerprinting
  - Fixed window size 1280x760 pixels
  - Session persistence using Playwright storage_state to avoid re-login
  - SaveSessionTool for agents to save cookies after manual login
  - Auto-navigate to https://seller.shopee.co.id on launch
  - humanize=True for human-like mouse movements

- **AI & CrewAI**
  - CrewAI integration with custom browser tools
  - Dynamic LLM Provider selection (SumoPod AI vs Official OpenAI)
  - Multiple SumoPod models: deepseek-v4-pro, MiniMax-M2.7-highspeed, MiniMax-Text-01, etc.
  - Sequential process for Shopee ads workflow
  - Thread-safe command queue for Playwright

- **Custom Tools**
  - GetCurrentPageInfoTool: Get current URL and title
  - NavigateToUrlTool: Navigate to specific URL
  - GetPageContentTool: Get raw HTML content
  - GetPageTextTool: Get clean innerText
  - ScrollDownTool: Scroll page for lazy-loaded content
  - ClickElementTool: Click element by CSS selector
  - TypeTextTool: Type text into input fields
  - PressKeyTool: Send keyboard keys
  - EvaluateJSTool: Execute custom JavaScript
  - DismissDialogTool: Multi-strategy modal closer
  - SaveSessionTool: Save browser session

- **UI Panels**
  - Chat Widget with Markdown rendering
  - Crew Panel: Agent hierarchy & status
  - Analytics Panel: Metrics & task history
  - Settings Panel: LLM & browser configuration
  - API key input fields for SumoPod and OpenAI

- **Distribution**
  - NSIS installer (ShopeeAgent-Setup.exe)
  - Portable version (dist/ShopeeAgent/)
  - Build scripts: build.bat, build-installer.bat
  - NSIS installer script (installer.nsi)
  - Installer guide documentation

### Changed
- Window size: 800x600 for better Shopee content viewing
- Browser viewport: 1280x760 for optimal viewing
- Chat bubbles: Dynamic height calculation using document size
- User bubbles: QLabel with auto-wrap instead of QTextEdit
- LLM: max_tokens=4096 for comprehensive responses
- Memory & Planning: Disabled by default to prevent API errors
- Fixed browser launch race condition with proper thread locking

### Fixed
- Cross-threading errors with Playwright using asyncio.Queue
- Silent application crashes with robust exception catching
- Internal scrollbars in chat bubbles with custom height calculation
- TargetClosedError with proper thread state management

## [0.1.0] - 2024-XX-XX

### Added
- Initial CamoAgent project
- Basic CrewAI browser automation
- PyQt6 desktop interface
