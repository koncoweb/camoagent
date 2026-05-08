import threading
import traceback
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal, QMetaObject, Qt, Q_ARG

from tools.browser_tool import BrowserConfig


class CrewExecutor(QObject):
    status_update = pyqtSignal(str, str)
    message_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._config = BrowserConfig.get_instance()
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._active_threads = []
        self._lock = threading.Lock()

    def set_page(self, page):
        self._config.set_page(page)

    def _safe_emit_status(self, agent: str, status: str):
        try:
            QMetaObject.invokeMethod(
                self, "status_update",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, agent),
                Q_ARG(str, status)
            )
        except Exception:
            pass

    def _safe_emit_message(self, message: str):
        try:
            QMetaObject.invokeMethod(
                self, "message_ready",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, message)
            )
        except Exception:
            pass

    def execute_task(self, task_description: str, page):
        if page is None:
            self.message_ready.emit("Please open the browser first using the 🦊 button.")
            return

        self.set_page(page)

        def run_crew():
            thread_id = threading.current_thread().ident
            try:
                with self._lock:
                    self._active_threads.append(thread_id)

                from crews.browser_crew import BrowserCrew

                self._safe_emit_status("Crew", "working")
                self._safe_emit_message("Starting task execution...")

                crew_instance = BrowserCrew()
                crew = crew_instance.get_crew()

                result = crew.kickoff(inputs={"task": task_description})

                self._safe_emit_status("Crew", "ready")
                self._safe_emit_message(f"Task completed:\n\n{str(result.raw)}")

            except Exception as e:
                error_msg = str(e)
                tb_str = traceback.format_exc()
                
                self._safe_emit_status("Crew", "error")
                
                if "insufficient_quota" in error_msg:
                    friendly_msg = (
                        "Error: Kuota AI Provider Anda habis atau belum diatur (insufficient_quota).\n"
                        "Silakan cek saldo/billing di provider yang Anda gunakan (SumoPod/OpenAI)."
                    )
                    self._safe_emit_message(friendly_msg)
                elif "API key" in error_msg.lower() or "auth" in error_msg.lower():
                    friendly_msg = (
                        "Error: Masalah autentikasi API.\n"
                        "Pastikan SUMOPOD_API_KEY sudah diatur dengan benar di file .env"
                    )
                    self._safe_emit_message(friendly_msg)
                else:
                    self._safe_emit_message(f"Error:\n{error_msg}\n\nDetail:\n{tb_str}")
            finally:
                with self._lock:
                    if thread_id in self._active_threads:
                        self._active_threads.remove(thread_id)

        thread = threading.Thread(target=run_crew, daemon=True)
        thread.start()

    def stop(self):
        with self._lock:
            self._active_threads.clear()
        self._running = False
