import threading
import time
import traceback
import os
from typing import Optional, Any
from PyQt6.QtCore import QObject, pyqtSignal, QMetaObject, Qt, Q_ARG


class BrowserManager(QObject):
    browser_ready = pyqtSignal()
    browser_closed = pyqtSignal()
    error_occurred = pyqtSignal(str)
    session_saved = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._browser: Optional[Any] = None
        self._page: Optional[Any] = None
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._command_queue = None
        self._lock = threading.Lock()
        self._session_file = os.path.join(os.path.dirname(__file__), "..", ".shopee_session")

    def get_session_path(self) -> str:
        return os.path.abspath(self._session_file)

    def launch_browser(self, headless: bool = False, headful: bool = True, target_url: str = None):
        with self._lock:
            # If a previous browser thread is still winding down, force-close it
            if self._thread is not None and self._thread.is_alive():
                self._running = False
                self._thread.join(timeout=4)
                self._thread = None
                self._browser = None
                self._page = None
                self._command_queue = None
            
            self._target_url = target_url
            self._thread = threading.Thread(target=self._run_browser, args=(headless, headful), daemon=True)
            self._thread.start()

    def save_session(self):
        if self._page is None:
            return False
        
        try:
            session_path = self.get_session_path()
            self._page.context.storage_state(path=session_path)
            return True
        except Exception as e:
            self._safe_emit_error(f"Failed to save session: {str(e)}")
            return False

    def _safe_emit_ready(self):
        try:
            QMetaObject.invokeMethod(
                self, "browser_ready",
                Qt.ConnectionType.QueuedConnection
            )
        except Exception:
            pass

    def _safe_emit_closed(self):
        try:
            QMetaObject.invokeMethod(
                self, "browser_closed",
                Qt.ConnectionType.QueuedConnection
            )
        except Exception:
            pass

    def _safe_emit_error(self, error: str):
        try:
            QMetaObject.invokeMethod(
                self, "error_occurred",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, error)
            )
        except Exception:
            pass

    def _run_browser(self, headless: bool, headful: bool):
        import asyncio
        from queue import Queue, Empty
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            from camoufox.sync_api import Camoufox
            from tools.browser_tool import BrowserConfig
            import ctypes

            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = ctypes.windll.user32.GetSystemMetrics(1)

            session_path = self.get_session_path()
            has_session = os.path.exists(session_path)
            target_url = getattr(self, '_target_url', None) or "https://seller.shopee.co.id"

            browser_options = {
                "headless": headless,
                "humanize": True,
                "window": (1280, 760),
                "locale": "id-ID",
            }
            
            if has_session and self._target_url is None:
                browser_options["storage_state"] = session_path
            
            fox = None
            retry_count = 0
            max_retries = 3

            while retry_count < max_retries:
                try:
                    fox = Camoufox(**browser_options)
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise RuntimeError(f"Camoufox gagal launch setelah {max_retries}x retry: {e}")
                    time.sleep(2 * retry_count)

            with fox as browser:
                self._browser = browser
                
                self._page = browser.new_page(viewport={"width": 1280, "height": 760})
                
                page_error = None
                for attempt in range(2):
                    try:
                        method = "domcontentloaded" if attempt == 0 else "commit"
                        timeout = 60000 if attempt == 0 else 30000
                        self._page.goto(target_url, wait_until=method, timeout=timeout)
                        page_error = None
                        break
                    except Exception as e:
                        page_error = e
                        time.sleep(1)
                
                if page_error is not None:
                    self._safe_emit_error(f"Page load warning: {page_error} — continuing anyway")
                
                self._running = True

                config = BrowserConfig.get_instance()
                config.set_page(self._page)
                command_queue = Queue()
                config.set_queue(command_queue)
                
                with self._lock:
                    self._command_queue = command_queue

                self._safe_emit_ready()

                # health check timer
                last_health_check = time.time()

                while self._running:
                    try:
                        # periodic health check — verify page is alive
                        now = time.time()
                        if now - last_health_check > 30:
                            try:
                                self._page.evaluate("1 + 1")
                            except Exception:
                                self._safe_emit_error("Browser health check failed — page may have crashed")
                            last_health_check = now

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
                                    for ga in range(2):
                                        try:
                                            self._page.goto(params.get('url'), wait_until="domcontentloaded", timeout=45000)
                                            break
                                        except Exception as ge:
                                            if ga == 1:
                                                raise
                                            time.sleep(1)
                                    result = f"Navigated to {params.get('url')}"
                                elif action == "get_content":
                                    result = self._page.content()
                                elif action == "get_text":
                                    result = self._page.evaluate("document.body.innerText")
                                elif action == "scroll_down":
                                    self._page.evaluate("window.scrollBy(0, window.innerHeight)")
                                    time.sleep(1.5)
                                    result = "Successfully scrolled down the page."
                                elif action == "click":
                                    self._page.click(params.get('selector'))
                                    result = f"Clicked {params.get('selector')}"
                                elif action == "type":
                                    self._page.fill(params.get('selector'), params.get('text'))
                                    result = f"Typed into {params.get('selector')}"
                                elif action == "press_key":
                                    key = params.get('key')
                                    self._page.keyboard.press(key)
                                    result = f"Pressed key: {key}"
                                elif action == "evaluate_js":
                                    script = params.get('script')
                                    js_result = self._page.evaluate(script)
                                    result = f"JavaScript executed. Result: {js_result}"
                                elif action == "dismiss_dialog":
                                    attempts = []
                                    
                                    try:
                                        self._page.keyboard.press("Escape")
                                        attempts.append("1. Pressed Escape key")
                                        time.sleep(0.5)
                                        if "headlessui" not in self._page.content():
                                            result = "Dialog closed successfully using Escape key!"
                                        else:
                                            raise Exception("Dialog still present after Escape")
                                    except Exception as e:
                                        attempts.append(f"1. Escape failed: {str(e)}")
                                    
                                    try:
                                        self._page.evaluate("""
                                            document.querySelectorAll('[data-headlessui-portal]').forEach(el => el.remove());
                                            document.querySelectorAll('[role="dialog"]').forEach(el => el.remove());
                                            document.querySelectorAll('.fixed.inset-0').forEach(el => el.remove());
                                            document.querySelectorAll('.fixed.bottom-0, .fixed.top-0').forEach(el => {
                                                if (el.querySelector('button')) el.remove();
                                            });
                                            document.documentElement.style.overflow = '';
                                        """)
                                        attempts.append("2. Removed portal and overlay elements")
                                        time.sleep(0.3)
                                    except Exception as e:
                                        attempts.append(f"2. Portal removal failed: {str(e)}")
                                    
                                    try:
                                        close_buttons = self._page.query_selector_all("button")
                                        for btn in close_buttons:
                                            try:
                                                text = btn.inner_text()
                                                if "tutup" in text.lower() or "close" in text.lower() or "×" in text:
                                                    btn.click()
                                                    attempts.append("3. Clicked close button")
                                                    break
                                            except:
                                                continue
                                    except Exception as e:
                                        attempts.append(f"3. Close button click failed: {str(e)}")
                                    
                                    result = "Dismiss dialog attempts:\n" + "\n".join(attempts)
                                elif action == "save_session":
                                    try:
                                        session_path = self.get_session_path()
                                        self._page.context.storage_state(path=session_path)
                                        result = f"Session saved successfully to {session_path}"
                                    except Exception as e:
                                        result = f"Failed to save session: {str(e)}"
                                
                                if result_queue:
                                    result_queue.put({"status": "success", "data": result})
                            except Exception as e:
                                if result_queue:
                                    result_queue.put({"status": "error", "message": str(e)})
                        
                        time.sleep(0.05)
                    except Exception:
                        continue

        except Exception as e:
            tb_str = traceback.format_exc()
            self._safe_emit_error(f"{str(e)}\n\n{traceback.format_exc()}")
        finally:
            try:
                if self._page is not None and self._page.context is not None:
                    session_path = self.get_session_path()
                    self._page.context.storage_state(path=session_path)
                    self._safe_emit_ready()
            except Exception:
                pass
            
            with self._lock:
                self._command_queue = None
            self._browser = None
            self._page = None
            self._running = False
            self._safe_emit_closed()

    def get_page(self) -> Optional[Any]:
        return self._page

    def is_ready(self) -> bool:
        return self._page is not None

    def close(self):
        with self._lock:
            self._running = False
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=8)
                self._thread = None
            
            self._browser = None
            self._page = None
            self._command_queue = None
