import sys
import os
import traceback
import logging
from pathlib import Path

# Setup logging first - use writable location
import tempfile

# Try multiple locations for log file
try:
    appdata_dir = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "ShopeeAgent"
except:
    appdata_dir = Path.home() / "ShopeeAgent"

log_locations = [
    Path(tempfile.gettempdir()) / "ShopeeAgent.log",
    appdata_dir / "ShopeeAgent.log",
    Path.home() / "ShopeeAgent.log",
]

log_file = None
for loc in log_locations:
    try:
        loc.parent.mkdir(parents=True, exist_ok=True)
        loc.touch(exist_ok=True)
        if loc.exists() and os.access(loc, os.W_OK):
            log_file = loc
            break
    except:
        continue

if log_file is None:
    log_file = Path(tempfile.gettempdir()) / "ShopeeAgent.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("ShopeeAgent")

def exception_hook(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.critical(f"Uncaught exception: {error_msg}")
    print(f"ERROR: {exc_type.__name__}: {exc_value}", file=sys.stderr)
    print(f"Check {log_file} for details", file=sys.stderr)

sys.excepthook = exception_hook

logger.info("=" * 50)
logger.info("ShopeeAgent starting...")
logger.info(f"Python: {sys.version}")
logger.info(f"Executable: {sys.executable}")
logger.info(f"CWD: {os.getcwd()}")
logger.info("=" * 50)

try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment loaded")

    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
    logger.info("PyQt6 imported successfully")

    from ui.main_window import MainWindow
    from services.browser_manager import BrowserManager
    from services.crew_executor import CrewExecutor
    logger.info("All modules imported successfully")

    class ShopeeAgentApp(QApplication):
        def __init__(self, argv):
            super().__init__(argv)
            self.setApplicationName("ShopeeAgent")
            self.setApplicationVersion("1.3.1")
            
            logger.info("Initializing ShopeeAgentApp...")
            
            self.setStyleSheet("""
                QToolTip {
                    color: #1A1A1A;
                    background-color: #F5F5F5;
                    border: 1px solid #D0D0D0;
                    padding: 6px 10px;
                    border-radius: 6px;
                    font-size: 12px;
                    font-family: 'Segoe UI';
                }
                QMessageBox {
                    color: #1A1A1A;
                    background-color: #FFFFFF;
                }
                QMessageBox QLabel {
                    color: #1A1A1A;
                    font-size: 13px;
                }
            """)
            
            try:
                self.browser_manager = BrowserManager()
                logger.info("BrowserManager initialized")
            except Exception as e:
                logger.error(f"Failed to initialize BrowserManager: {e}")
                raise
            
            try:
                self.crew_executor = CrewExecutor()
                logger.info("CrewExecutor initialized")
            except Exception as e:
                logger.error(f"Failed to initialize CrewExecutor: {e}")
                raise
            
            try:
                self.main_window = MainWindow(
                    browser_manager=self.browser_manager,
                    crew_executor=self.crew_executor
                )
                logger.info("MainWindow initialized")
                
                # Set window icon for taskbar and title bar
                # PyInstaller bundle path support
                if getattr(sys, 'frozen', False):
                    base_dir = sys._MEIPASS
                else:
                    base_dir = os.path.dirname(__file__)
                icon_path = os.path.join(base_dir, 'shopeeagentcrop.ico')
                if os.path.exists(icon_path):
                    from PyQt6.QtGui import QIcon
                    self.main_window.setWindowIcon(QIcon(icon_path))
                    self.setWindowIcon(QIcon(icon_path))
                    logger.info(f"Window icon set: {icon_path}")
                else:
                    logger.warning(f"Icon not found: {icon_path}")
            except Exception as e:
                logger.error(f"Failed to initialize MainWindow: {e}")
                raise

        def run(self):
            logger.info("Showing main window...")
            self.main_window.show()
            logger.info("Application ready!")
            sys.exit(self.exec())

    def main():
        logger.info("Creating ShopeeAgentApp instance...")
        app = ShopeeAgentApp(sys.argv)
        app.run()

    if __name__ == "__main__":
        main()

except Exception as e:
    logger.critical(f"Startup failed: {e}")
    logger.critical(traceback.format_exc())
    
    # Show error dialog if possible
    try:
        from PyQt6.QtWidgets import QApplication, QMessageBox
        app = QApplication(sys.argv)
        QMessageBox.critical(
            None,
            "ShopeeAgent Error",
            f"Failed to start ShopeeAgent:\n\n{e}\n\nCheck ShopeeAgent.log for details."
        )
    except:
        pass
    
    input("Press Enter to exit...")
    sys.exit(1)
