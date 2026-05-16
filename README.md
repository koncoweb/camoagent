# ShopeeAgent - AI Shopee Manager

A powerful desktop application that combines CrewAI multi-agent system with Camoufox browser for intelligent Shopee store management.

![ShopeeAgent](https://img.shields.io/badge/Version-1.0.0-EE4D2D?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🎯 Features

### 🛒 Shopee Browser Integration
- **Camoufox** stealth browser with anti-bot evasion
- Human-like mouse movements with `humanize=True`
- Session persistence - no re-login required
- Fixed 1280x760 viewport for optimal viewing
- Auto-navigate to Shopee Seller Center

### 📊 Shopee Ads Management
- **AI-Powered Analysis** with 3 specialized agents
- Financial calculations: ROAS, Break-Even, Max CPC, Net Profit
- Performance classification: Bagus / Cukup / Rugi
- Bid optimization recommendations
- Sequential CrewAI workflow

### 🤖 AI Agents
| Agent | Role | Function |
|-------|------|----------|
| 🛒 Navigator | Shopee Dashboard Navigator | Extract data from Shopee pages |
| 📊 Financial Analyst | E-commerce Financial Analyst | Calculate ROAS, Break-Even, Max CPC |
| 🎯 Ads Optimizer | PPC Strategist | Generate bid recommendations |

### 🛠️ Custom Tools
| Tool | Function |
|------|----------|
| `GetCurrentPageInfoTool` | Get current URL and title |
| `NavigateToUrlTool` | Navigate to specific URL |
| `GetPageTextTool` | Get clean innerText |
| `ScrollDownTool` | Scroll for lazy-loaded content |
| `ClickElementTool` | Click element by CSS selector |
| `PressKeyTool` | Send keyboard keys |
| `DismissDialogTool` | Close modals/popups |
| `SaveSessionTool` | Save browser session |

### 🎨 Shopee-Themed UI
- Orange (#EE4D2D) and white color scheme
- Chat interface with Markdown rendering
- Real-time status panel
- Crew configuration panel
- Analytics dashboard
- Settings with API key management

## 📥 Installation

### Option 1: NSIS Installer (Recommended)
```
1. Download ShopeeAgent-Setup.exe
2. Run the installer
3. Launch from Desktop or Start Menu
```

### Option 2: Portable Version
```
1. Download ShopeeAgent-Portable.zip
2. Extract to any folder
3. Run ShopeeAgent.exe
```

### Option 3: Build from Source

```batch
# Clone repository
git clone <repo-url>
cd camoagent

# Create .env file
echo SUMOPOD_API_KEY=your_api_key > .env

# Run build script
build.bat
```

## 🚀 Usage

### First Time Setup
1. Launch ShopeeAgent
2. Click 🛒 to open browser
3. Login to Shopee Seller Center (manual)
4. Session will be saved automatically

### Running Analysis
1. Navigate to Shopee Ads dashboard in browser
2. Click 📢 icon to start analysis
3. View results in chat panel

### Settings
- **Provider**: SumoPod AI (default) or OpenAI
- **Model**: Select from available models
- **API Keys**: Enter your keys directly in Settings

## 🏗️ Architecture

```
ShopeeAgent
├── UI Layer (PyQt6)
│   ├── Icon Bar - Navigation (Browser, Ads, Crew, Settings)
│   ├── Chat Widget - Command input & AI responses
│   ├── Status Panel - Real-time logs
│   └── Settings Panel - Configuration
│
├── Service Layer
│   ├── BrowserManager - Camoufox lifecycle
│   └── CrewExecutor - CrewAI execution
│
├── Agent Layer (CrewAI)
│   ├── ShopeeNavigator - Data extraction
│   ├── FinancialAnalyst - Financial calculations
│   └── AdsOptimizer - Recommendations
│
└── Tools Layer
    └── Custom Browser Tools
```

## 📁 Project Structure

```
shopeeagent/
├── camoagent.py           # Main entry point
├── camoagent.spec        # PyInstaller spec
├── build.bat            # Build script
├── requirements.txt     # Dependencies
│
├── config/              # Configuration
│   ├── agents.yaml
│   ├── tasks.yaml
│   ├── shopee_agents.yaml
│   └── shopee_tasks.yaml
│
├── crews/               # CrewAI crews
│   ├── browser_crew.py
│   └── shopee_crew.py
│
├── tools/               # Custom tools
│   ├── browser_tool.py
│   └── shopee_tools.py
│
├── services/            # Application services
│   ├── browser_manager.py
│   └── crew_executor.py
│
├── ui/                  # PyQt6 UI
│   ├── main_window.py
│   └── panels.py
│
└── docs/               # Documentation
    └── INSTALLER_GUIDE.md
```

## 🔧 Configuration

### Environment Variables (.env)
```env
SUMOPOD_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Available Models

**SumoPod AI:**
- `MiniMax-M2.7-highspeed` (default)
- `deepseek-v4-pro`
- `MiniMax-Text-01`
- `abab6.5s-chat`
- `abab6.5g-chat`

**OpenAI:**
- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`

## 📊 Financial Calculations

| Metric | Formula |
|--------|---------|
| Actual Cost | Shopee Cost × 1.11 (PPN 11%) |
| Actual ROAS | GMV / Actual Cost |
| Net Profit | Selling Price - HPP - Admin Fee - Operational |
| Break-Even ROAS | Selling Price / Net Profit |
| Max CPC | Net Profit × Conversion Rate |

### Performance Classification
- **🎯 Bagus**: ROAS > 5.0 (Target)
- **⏸️ Cukup**: Break-Even < ROAS < 5.0
- **🛑 Rugi**: ROAS < Break-Even

## 🐛 Troubleshooting

### Browser won't launch
```bash
# Re-fetch Camoufox
python -m camoufox fetch
```

### API errors
- Check API key in Settings panel
- Ensure sufficient credits in SumoPod/OpenAI

### Build fails
```bash
# Update dependencies
pip install --upgrade -r requirements.txt
```

## 📄 License

MIT License - see [LICENSE.txt](LICENSE.txt)

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com/) - Multi-agent framework
- [Camoufox](https://camoufox.com/) - Stealth browser
- [PyQt6](https://riverbankcomputing.com/software/pyqt/) - Desktop UI
