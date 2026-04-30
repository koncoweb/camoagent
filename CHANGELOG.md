# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Added `GetPageTextTool` to extract clean `innerText` from pages, preventing LLM context bloat from raw HTML.
- Added `ScrollDownTool` to allow agents to trigger lazy-loading mechanisms on E-commerce sites like Shopee.
- Added `humanize=True` flag to Camoufox initialization to simulate human mouse movements and bypass advanced anti-bot systems.
- Added `deepseek-v4-pro` support via SumoPod AI to prevent agent hanging.
- Added asynchronous thread-safe Command Queue (`asyncio.Queue`) in `BrowserManager` to fix Playwright cross-threading errors.
- Added native Markdown rendering in the UI (`Qt.TextFormat.MarkdownText`) to display rich-text formatted AI responses (Headers, Bold, Lists).

### Changed
- Disabled CrewAI `memory` and `planning` features by default to prevent `/embeddings` 400 errors from SumoPod AI.
- Updated `BrowserCrew` to utilize dynamic tasks from `tasks.yaml` instead of hardcoded strings.
- Refactored `browser_tool.py` using `BaseTool` structure based on official CrewAI documentation.
- Improved `ChatWidget` to use word wrapping, dynamic sizing, and external links for better UX.
- Updated agent `tasks.yaml` to enforce beautiful, structured Markdown formatting with emojis and bullet points.

### Fixed
- Fixed issue where the agent returned truncated outputs (hardcoded `[:500]` slicing removed).
- Fixed Playwright threading violation (Cannot access from different thread) when tools were invoked.
- Fixed layout clipping in `main_window.py` where long text was hidden.
