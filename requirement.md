# Project Requirements: CamoAgent

## Overview
CamoAgent is a Desktop GUI application built with PyQt6 that integrates a stealth browser (Camoufox/Playwright) with a multi-agent AI system (CrewAI). It acts as an automated web assistant that can navigate, scrape, and analyze web data safely without being easily detected as a bot.

## Core Dependencies
- **PyQt6**: For the desktop graphical user interface.
- **CrewAI**: For orchestration of multiple AI agents (Navigator, Scraper, Analyst).
- **Camoufox (Playwright-based)**: For stealth browser automation with anti-bot evasion.
- **OpenAI (Python SDK)**: For API interaction with SumoPod AI (compatible endpoint).
- **Markdown**: For parsing and rendering rich-text markdown directly into HTML for UI chat bubbles.

## Core Features

### 1. Stealth Browser Automation
- **Camoufox** with `humanize=True` for human-like mouse movements
- **BrowserForge fingerprinting** for anti-detect capabilities
- **Thread-safe Command Queue** pattern for cross-thread communication
- Supports e-commerce sites like Shopee with lazy-loading detection

### 2. AI Agent Orchestration
- **Hierarchical Process**: Manager agent coordinates sub-agents
- **Three Specialized Agents**: Navigator, Scraper, Analyst
- **Dynamic Tasks**: YAML-based task configuration
- **Custom Tools**: `GetPageTextTool`, `ScrollDownTool`, `ClickElementTool`, etc.
- **LLM**: `deepseek-v4-pro` via SumoPod AI with `max_tokens=4096`

### 3. Modern UI/UX
- **Sidebar Navigation**: Browser, Crew, Analytics, Settings panels
- **Chat Interface**: Markdown-rendered responses with `QTextEdit` for proper text expansion
- **Status Panel**: Real-time logging and agent activity tracking
- **Dark Theme**: Modern dark mode styling

### 4. CrewAI Tools
| Tool | Function |
|------|----------|
| `GetCurrentPageInfoTool` | Get current URL and title |
| `NavigateToUrlTool` | Navigate to a specific URL |
| `GetPageContentTool` | Get raw HTML content |
| `GetPageTextTool` | Get clean innerText (preferred) |
| `ScrollDownTool` | Scroll page for lazy-loaded content |
| `ClickElementTool` | Click element by CSS selector |
| `TypeTextTool` | Type text into input fields |
| `PressKeyTool` | Send specific keyboard keys (e.g., 'Escape') |
| `EvaluateJSTool` | Execute custom JavaScript on the page |
| `DismissDialogTool` | Multi-strategy tool to close React/Headless UI modals |

## Architectural Requirements
1. **Thread Safety**: Playwright runs in isolated background thread; all interactions routed through `asyncio.Queue`.
2. **AI Provider**: SumoPod AI (`deepseek-v4-pro`) configured via `.env`.
3. **UI/UX**: Non-blocking interface with proper text expansion in chat bubbles.
4. **Configuration**: Declarative agent/tasks in `agents.yaml` and `tasks.yaml`.

## Configuration Files
- `.env` / `.env.example`: API keys and endpoint configuration
- `config/agents.yaml`: Agent roles, goals, and backstories
- `config/tasks.yaml`: Task descriptions and formatting rules

## Recent Updates
- Enabled Camoufox `humanize=True` for anti-bot evasion
- Added `GetPageTextTool` and `ScrollDownTool` for better scraping
- Integrated functional sidebar panels (Crew, Analytics, Settings) via `QStackedWidget`
- Integrated `markdown` library to convert AI markdown output into beautiful HTML
- Chat bubbles now dynamically size themselves via document size calculation to prevent internal scrollbars
- Implemented robust exception handling and thread-safe PyQt6 signal emissions (`QMetaObject.invokeMethod`) to prevent silent crashes
- Added advanced modal-handling tools (`PressKeyTool`, `EvaluateJSTool`, `DismissDialogTool`) to close stubborn React/Headless UI popups
- Added `max_tokens=4096` to prevent response truncation
- Disabled `memory` and `planning` features for SumoPod compatibility
