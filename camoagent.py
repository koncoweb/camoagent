import sys
import asyncio
import threading
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon

from ui.main_window import MainWindow
from services.browser_manager import BrowserManager
from services.crew_executor import CrewExecutor


class CamoAgentApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("CamoAgent")
        self.setApplicationVersion("0.1.0")

        self.browser_manager = BrowserManager()
        self.crew_executor = CrewExecutor()

        self.main_window = MainWindow(
            browser_manager=self.browser_manager,
            crew_executor=self.crew_executor
        )

    def run(self):
        self.main_window.show()
        sys.exit(self.exec())


def main():
    app = CamoAgentApp(sys.argv)
    app.run()


if __name__ == "__main__":
    main()
