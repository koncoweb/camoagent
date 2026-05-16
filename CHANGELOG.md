# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Rebranded application from **CamoAgent** to **ShopeeAgent** with Shopee orange (#EE4D2D) and white color theme
- Redesigned UI with Shopee brand colors: orange primary, white backgrounds, warm cream accents

### Changed
- Set Camoufox browser window to fixed size 1280x760 pixels using `window=(1280, 760)` parameter for consistent viewport.
- Window size increased to 900x650 for better Shopee content viewing

### Added
- Added dynamic LLM Provider selection (SumoPod AI vs Official OpenAI) in Settings panel, with safety guardrails that disable unsupported features (Memory, Planning) on third-party providers.
- Added `PressKeyTool` for keyboard automation (essential for closing modals via 'Escape').
- Added `EvaluateJSTool` for executing custom JavaScript directly in the browser context.
- Added `DismissDialogTool` which uses a multi-strategy approach (Escape key, portal removal via JS, button clicking) to close complex Headless UI/React popups.
- Added `markdown` library dependency to reliably convert rich-text Markdown to HTML with custom CSS for the chat interface.
- Added robust thread-safe PyQt6 signal emissions (`QMetaObject.invokeMethod` with `QueuedConnection`) in `BrowserManager` and `CrewExecutor`.
- Added comprehensive exception catching and traceback logging for background daemon threads to prevent silent application crashes.
- Added `GetPageTextTool` to extract clean `innerText` from pages, preventing LLM context bloat from raw HTML.
- Added `ScrollDownTool` to allow agents to trigger lazy-loading mechanisms on E-commerce sites like Shopee.
- Added `humanize=True` flag to Camoufox initialization to simulate human mouse movements and bypass advanced anti-bot systems.
- Added `deepseek-v4-pro` support via SumoPod AI to prevent agent hanging.
- Added asynchronous thread-safe Command Queue (`asyncio.Queue`) in `BrowserManager` to fix Playwright cross-threading errors.
- Added `max_tokens=4096` to LLM configuration to allow comprehensive, non-truncated responses.
- Added functional panel sidebar: **Crew Panel** (agent hierarchy & status), **Analytics Panel** (metrics & task history), **Settings Panel** (LLM & browser config).

### Changed
- Changed main application window size to a responsive fixed layout (`800x600`) and browser viewport to `1280x600` for optimal visibility on smaller laptops.
- Reverted problematic `QTextBrowser` back to `QTextEdit` and built a custom HTML rendering system using the `markdown` package.
- Chat bubbles now calculate their exact height dynamically using `document().size().height()` to eliminate internal vertical and horizontal scrollbars.
- Changed user chat bubbles to use `QLabel` with auto-wrap instead of `QTextEdit` to ensure perfectly accurate height calculation without layout overflow.
- Disabled CrewAI `memory` and `planning` features by default to prevent `/embeddings` 400 errors from SumoPod AI.
- Updated `BrowserCrew` to utilize dynamic tasks from `tasks.yaml` instead of hardcoded strings.
- Refactored `browser_tool.py` using `BaseTool` structure based on official CrewAI documentation.
- Updated agent `tasks.yaml` to enforce beautiful, structured Markdown formatting with emojis and bullet points.

### Fixed
- Fixed application crashes caused by unhandled exceptions in `CrewExecutor` daemon threads interacting with PyQt6 main thread.
- Fixed UI layout "chaos" by preventing `QTextEdit` from generating internal scrollbars while retaining rich text features.
- Fixed inability of the AI agent to close React/Headless UI modals (z-index 500001) by providing aggressive JS removal fallback tools.
- Fixed issue where the agent returned truncated outputs (hardcoded `[:500]` slicing removed).
- Fixed Playwright threading violation (Cannot access from different thread) when tools were invoked.
- Fixed layout clipping in `main_window.py` where long text was hidden.

## [v0.1.0] - Initial Release
- Basic PyQt6 GUI with Camoufox browser integration.
- Simple CrewAI agent orchestration.
- Hardcoded ROI calculation tasks.
