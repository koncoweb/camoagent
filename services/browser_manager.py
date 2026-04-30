import threading
import time
from typing import Optional, Any
from PyQt6.QtCore import QObject, pyqtSignal


class BrowserManager(QObject):
    browser_ready = pyqtSignal()
    browser_closed = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._browser: Optional[Any] = None
        self._page: Optional[Any] = None
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False

    def launch_browser(self, headless: bool = False, headful: bool = True):
        if self._browser is not None:
            return

        self._thread = threading.Thread(target=self._run_browser, args=(headless, headful), daemon=True)
        self._thread.start()

    def _run_browser(self, headless: bool, headful: bool):
        import asyncio
        # Setup event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            from camoufox.sync_api import Camoufox

            # Keep reference to browser context
            # headful param doesn't exist, we just use headless
            # window_width and window_height are not valid launch kwargs
            with Camoufox(headless=headless) as browser:
                self._browser = browser
                self._page = browser.new_page(viewport={"width": 1280, "height": 800})
                self._page.goto("about:blank")
                self._running = True

                self.browser_ready.emit()

                # Keep thread alive while running
                while self._running:
                    time.sleep(0.1)

        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self._browser = None
            self._page = None
            self._running = False
            self.browser_closed.emit()

    def get_page(self) -> Optional[Any]:
        return self._page

    def is_ready(self) -> bool:
        return self._page is not None

    def close(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
            
        self._browser = None
        self._page = None
