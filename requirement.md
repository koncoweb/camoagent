# Project Requirements: CamoAgent

## Overview
CamoAgent is a Desktop GUI application built with PyQt6 that integrates a stealth browser (Camoufox/Playwright) with a multi-agent AI system (CrewAI). It acts as an automated web assistant that can navigate, scrape, and analyze web data safely without being easily detected as a bot.

## Core Dependencies
- **PyQt6**: For the desktop graphical user interface.
- **CrewAI**: For orchestration of multiple AI agents (Navigator, Scraper, Analyst).
- **Camoufox (Playwright-based)**: For stealth browser automation.
- **OpenAI (Python SDK)**: For API interaction with SumoPod AI (compatible endpoint).

## Architectural Requirements
1. **Thread Safety**: The Playwright instance must be isolated in a single background thread. All interactions with the browser from the AI agents (running in separate threads) must be routed through a thread-safe Command Queue (`asyncio.Queue`).
2. **AI Provider**: Uses `SumoPod AI` (`deepseek-v4-pro`) configured via `.env` files.
3. **UI/UX**: 
   - Non-blocking interface (GUI runs on main thread, AI tasks on worker threads).
   - Chat bubbles should natively render Markdown formats, support word-wrap, and provide readable, beautiful outputs.
   - Status tracking panel to view background agent activities.
4. **Configuration**: Agent roles, goals, and tasks should be defined declaratively in `agents.yaml` and `tasks.yaml`.

## Recent Updates
- Enabled Camoufox `humanize=True` to simulate human mouse movements and improve anti-bot evasion.
- Added `GetPageTextTool` and `ScrollDownTool` to optimize scraping on modern lazy-loaded E-commerce platforms (like Shopee).
- Integrated `MarkdownText` format rendering for Chat Bubbles.
- AI is instructed to output well-formatted Markdown with Headers, Lists, Bold Text, and Emojis.
- Embeddings-dependent features (`memory`, `planning`) are disabled by default to maintain compatibility with custom LLM endpoints.