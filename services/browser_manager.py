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
        from queue import Queue, Empty
        
        # Setup event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            from camoufox.sync_api import Camoufox
            from tools.browser_tool import BrowserConfig

            # Gunakan parameter humanize=True agar Camoufox mensimulasikan pergerakan mouse & perilaku manusia
            with Camoufox(headless=headless, humanize=True) as browser:
                self._browser = browser
                self._page = browser.new_page(viewport={"width": 1280, "height": 800})
                self._page.goto("about:blank")
                self._running = True

                # Setup the command queue in config
                config = BrowserConfig.get_instance()
                config.set_page(self._page)
                command_queue = Queue()
                config.set_queue(command_queue)

                self.browser_ready.emit()

                # Process commands from queue in the browser thread
                while self._running:
                    try:
                        # Non-blocking check for commands
                        if not command_queue.empty():
                            command = command_queue.get()
                            action = command.get('action')
                            params = command.get('params', {})
                            result_queue = command.get('result_queue')

                            try:
                                result = None
                                if action == "get_info":
                                    result = f"Current URL: {self._page.url}\nCurrent Title: {self._page.title()}"
                                elif action == "goto":
                                    self._page.goto(params.get('url'))
                                    result = f"Navigated to {params.get('url')}"
                                elif action == "get_content":
                                    result = self._page.content()
                                elif action == "get_text":
                                    # Mengambil innerText agar LLM tidak pusing membaca raw HTML (berguna untuk Shopee)
                                    result = self._page.evaluate("document.body.innerText")
                                elif action == "scroll_down":
                                    # Scroll halaman untuk men-trigger lazy loading
                                    self._page.evaluate("window.scrollBy(0, window.innerHeight)")
                                    time.sleep(1.5) # Tunggu lazy load selesai
                                    result = "Successfully scrolled down the page."
                                elif action == "click":
                                    self._page.click(params.get('selector'))
                                    result = f"Clicked {params.get('selector')}"
                                elif action == "type":
                                    self._page.fill(params.get('selector'), params.get('text'))
                                    result = f"Typed into {params.get('selector')}"
                                
                                if result_queue:
                                    result_queue.put({"status": "success", "data": result})
                            except Exception as e:
                                if result_queue:
                                    result_queue.put({"status": "error", "message": str(e)})
                        
                        time.sleep(0.05)
                    except Exception:
                        continue

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
