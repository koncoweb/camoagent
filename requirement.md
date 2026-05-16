# ShopeeAgent - Project Requirements

## Overview
**ShopeeAgent** is a Desktop GUI application built with PyQt6 that integrates a stealth browser (Camoufox/Playwright) with a multi-agent AI system (CrewAI) specifically designed for Shopee store management and ads optimization.

## Core Dependencies
| Package | Purpose |
|---------|---------|
| **PyQt6** | Desktop graphical user interface |
| **CrewAI** | Multi-agent AI orchestration |
| **Camoufox** | Stealth browser automation with anti-bot evasion |
| **OpenAI SDK** | API interaction with SumoPod AI or OpenAI |
| **Markdown** | Parse markdown to HTML for chat interface |

## Core Features

### 1. Shopee Browser Automation
- **Camoufox** with `humanize=True` for human-like mouse movements
- **BrowserForge fingerprinting** for anti-detect capabilities
- **Session Persistence** using Playwright storage_state to avoid re-login
- **Thread-safe Command Queue** pattern for cross-thread communication
- **Fixed 1280x760 viewport** for optimal Shopee viewing

### 2. AI Agent Orchestration
- **Sequential Process**: Manager agent coordinates sub-agents
- **Three Specialized Agents**:
  - ShopeeNavigator - Data extraction from Shopee pages
  - FinancialAnalyst - Financial calculations (ROAS, Break-Even, Max CPC)
  - AdsOptimizer - Bid optimization recommendations
- **Custom Tools**: GetPageTextTool, ScrollDownTool, ClickElementTool, etc.
- **LLM**: Configurable (default: MiniMax-M2.7-highspeed via SumoPod AI)

### 3. Shopee Ads Management
- Extract advertising metrics from Shopee Seller Center
- Calculate financial metrics:
  - Actual Cost = Shopee Cost × 1.11 (PPN 11%)
  - Actual ROAS = GMV / Actual Cost
  - Net Profit = Selling Price - HPP - Admin Fee - Operational
  - Break-Even ROAS = Selling Price / Net Profit
  - Max CPC = Net Profit × Conversion Rate
- Performance classification:
  - 🎯 **Bagus**: ROAS > 5.0
  - ⏸️ **Cukup**: Break-Even < ROAS < 5.0
  - 🛑 **Rugi**: ROAS < Break-Even
- Generate bid optimization recommendations

### 4. Shopee-Themed UI/UX
- **Sidebar Navigation**: Browser, Ads, Crew, Analytics, Settings panels
- **Chat Interface**: Markdown-rendered responses with dynamic height
- **Status Panel**: Real-time logging and agent activity tracking
- **Settings Panel**: LLM configuration and API key management
- **Shopee Branding**: Orange (#EE4D2D) and white color scheme

## Custom Tools

| Tool | Function |
|------|----------|
| `GetCurrentPageInfoTool` | Get current URL and title |
| `NavigateToUrlTool` | Navigate to a specific URL |
| `GetPageContentTool` | Get raw HTML content |
| `GetPageTextTool` | Get clean innerText (preferred) |
| `ScrollDownTool` | Scroll page for lazy-loaded content |
| `ClickElementTool` | Click element by CSS selector |
| `TypeTextTool` | Type text into input fields |
| `PressKeyTool` | Send specific keyboard keys |
| `EvaluateJSTool` | Execute custom JavaScript on the page |
| `DismissDialogTool` | Multi-strategy modal closer |
| `SaveSessionTool` | Save browser session to file |
| `ExtractShopeeAdsMetricsTool` | Extract ads metrics from Shopee |
| `CalculateActualFinancialsTool` | Calculate financial metrics |
| `GenerateAdsRecommendationTool` | Generate bid recommendations |

## Shopee Crew Agents

### ShopeeNavigator Agent
- **Role**: Shopee Dashboard Navigator
- **Goal**: Navigate to Shopee Seller Center ads dashboard and extract clean metrics data in JSON format
- **Tools**: All browser tools

### FinancialAnalyst Agent
- **Role**: E-commerce Financial Analyst
- **Goal**: Calculate actual financial metrics including PPN 11%, Break-Even ROAS, Net Profit, and classify performance
- **Tools**: CalculateActualFinancialsTool

### AdsOptimizer Agent
- **Role**: PPC Strategist & Ads Optimizer
- **Goal**: Analyze financial reports and generate actionable bid optimization recommendations
- **Tools**: GenerateAdsRecommendationTool

## Architectural Requirements
1. **Thread Safety**: Playwright runs in isolated background thread; all interactions routed through `asyncio.Queue`.
2. **AI Provider**: SumoPod AI or Official OpenAI, configurable via Settings
3. **UI/UX**: Non-blocking interface with proper text expansion in chat bubbles
4. **Session Persistence**: storage_state JSON file for Shopee login
5. **Configuration**: Declarative agent/tasks in YAML files

## Configuration Files
- `.env` / `.env.example`: API keys and endpoint configuration
- `config/agents.yaml`: Browser crew agent definitions
- `config/tasks.yaml`: Browser crew task definitions
- `config/shopee_agents.yaml`: Shopee ads crew agent definitions
- `config/shopee_tasks.yaml`: Shopee ads task definitions

## Installation & Build

### Requirements
- Windows 10/11
- Python 3.10+
- Internet connection (for first run - downloads Camoufox browser)
- API key (SumoPod AI or OpenAI)

### Build Options
1. **NSIS Installer**: `ShopeeAgent-Setup.exe` (232 MB)
2. **Portable ZIP**: `dist/ShopeeAgent/`
3. **From Source**: `build.bat`

## Recent Updates

### v1.0.0 (2025-05-16)
- Full rebrand from CamoAgent to ShopeeAgent
- Shopee orange (#EE4D2D) themed UI
- Shopee Ads Management with 3 AI agents
- Session persistence with storage_state
- NSIS installer distribution
- API key input in Settings panel
- Multiple SumoPod model support

### v0.1.0
- Initial CamoAgent project
- Basic CrewAI browser automation
- PyQt6 desktop interface
