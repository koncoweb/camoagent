# ShopeeAgent - AI Shopee Manager

A powerful desktop application that combines CrewAI multi-agent system with Camoufox browser for intelligent Shopee store management.

## Features

- 🛒 **Shopee Browser Integration** - Headful browser with stealth fingerprinting for Shopee
- 🤖 **Multi-Agent CrewAI System** - Navigator, Scraper, Analyst, and Reporter agents
- 💬 **Chat Interface** - Natural language commands for Shopee automation
- 📊 **Analytics Dashboard** - Track Shopee store performance and metrics
- 🧡 **Shopee-Themed UI** - Beautiful orange and white design matching Shopee branding

## Requirements

- Windows 10/11
- Internet connection (for first run - downloads Camoufox browser)
- OpenAI API key (for CrewAI agents)

## Installation

### Option 1: Using Pre-built Executable

1. Download the latest `ShopeeAgent.exe` from releases
2. Copy `.env` file to the same directory as the executable
3. Edit `.env` and add your `OPENAI_API_KEY`
4. Run `ShopeeAgent.exe`

### Option 2: Building from Source

1. Ensure you have Python 3.10+ installed
2. Clone or download this repository
3. Create a `.env` file based on `.env.example`:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Run `build.bat` or execute these commands:
   ```batch
   pip install -r requirements.txt
   pip install pyinstaller
   pyinstaller camoagent.spec --clean
   ```

## Usage

1. **Launch Browser** - Click the 🛒 icon to open Shopee browser
2. **Navigate Manually** - Use the browser as normal (login, navigate to Shopee)
3. **Send Commands** - Type commands in the chat box, e.g.:
   - "Go to Shopee Seller Center and check my orders"
   - "Analyze my product listings and suggest improvements"
   - "Calculate ROI for my Shopee ads campaign"
4. **View Results** - Agents work collaboratively and return results in the chat

## Architecture

```
ShopeeAgent
├── UI Layer (PyQt6)
│   ├── Icon Bar - Navigation icons (Shopee-themed)
│   ├── Chat Widget - Command input and AI responses
│   └── Status Panel - Logs and agent activity
├── Service Layer
│   ├── BrowserManager - Camoufox lifecycle management
│   └── CrewExecutor - CrewAI task execution
├── Agent Layer (CrewAI)
│   ├── Navigator Agent - Shopee web navigation
│   ├── Scraper Agent - Data extraction from pages
│   ├── Analyst Agent - Data analysis and calculations
│   └── Reporter Agent - Results formatting
└── Tools Layer
    └── BrowserTool - Custom CrewAI tool for browser control
```

## Project Structure

```
shopeeagent/
├── camoagent.py          # Main entry point
├── requirements.txt      # Python dependencies
├── camoagent.spec        # PyInstaller specification
├── build.bat            # Build script for Windows
│
├── config/               # Configuration files
│   ├── agents.yaml       # Agent definitions
│   └── tasks.yaml       # Task definitions
│
├── crews/                # CrewAI crew definitions
│   └── browser_crew.py  # Multi-agent crew
│
├── tools/                # Custom CrewAI tools
│   └── browser_tool.py  # Browser control tool
│
├── services/             # Application services
│   ├── browser_manager.py  # Browser lifecycle
│   └── crew_executor.py    # Crew execution
│
└── ui/                  # PyQt6 UI components
    └── main_window.py   # Main window layout
```

## Troubleshooting

### Browser won't launch
- Ensure Camoufox is installed: `pip install camoufox`
- Try running as administrator

### Agents don't respond
- Check your `OPENAI_API_KEY` is valid
- Ensure internet connection

### Build fails
- Ensure Python 3.10+ is installed
- Update pip: `python -m pip install --upgrade pip`
- Install Visual Studio Build Tools (for Windows)

## License

MIT License
