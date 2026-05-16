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
        self.crew_settings = {
            "provider": "SumoPod AI",
            "memory": False,
            "planning": False,
            "model": "deepseek-v4-pro",
            "max_iter": 10
        }

    def update_settings(self, settings: dict):
        with self._lock:
            self.crew_settings.update(settings)

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

    def execute_shopee_ads_task(self, task_description: str = None, page=None):
        self.set_page(page)

        def run_shopee_crew():
            thread_id = threading.current_thread().ident
            try:
                with self._lock:
                    self._active_threads.append(thread_id)
                    current_settings = self.crew_settings.copy()

                from crews.shopee_crew import ShopeeCrew

                self._safe_emit_status("Shopee Crew", "working")
                self._safe_emit_message("Starting Shopee Ads Analysis...\n\nExtracting metrics from Shopee Seller Center...")

                crew_instance = ShopeeCrew(
                    provider=current_settings.get("provider", "SumoPod AI"),
                    memory=current_settings.get("memory", False),
                    planning=current_settings.get("planning", False),
                    model=current_settings.get("model", "MiniMax-M2.7-highspeed"),
                    max_iter=current_settings.get("max_iter", 10),
                    sumpod_api_key=current_settings.get("sumpod_api_key"),
                    openai_api_key=current_settings.get("openai_api_key")
                )
                
                if task_description:
                    result = crew_instance.kickoff(task_override=task_description)
                else:
                    result = crew_instance.kickoff()

                self._safe_emit_status("Shopee Crew", "ready")
                self._safe_emit_message(f"## ✅ Shopee Ads Analysis Complete\n\n{str(result.raw)}")

            except Exception as e:
                error_msg = str(e)
                tb_str = traceback.format_exc()
                
                self._safe_emit_status("Shopee Crew", "error")
                
                if "insufficient_quota" in error_msg:
                    friendly_msg = "Error: Kuota AI Provider habis. Silakan cek saldo di SumoPod/OpenAI."
                elif "API key" in error_msg.lower() or "auth" in error_msg.lower():
                    friendly_msg = "Error: Masalah autentikasi API. Pastikan SUMOPOD_API_KEY sudah diatur di .env"
                else:
                    friendly_msg = f"Error:\n{error_msg}"
                self._safe_emit_message(friendly_msg)
            finally:
                with self._lock:
                    if thread_id in self._active_threads:
                        self._active_threads.remove(thread_id)

        thread = threading.Thread(target=run_shopee_crew, daemon=True)
        thread.start()

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
                    current_settings = self.crew_settings.copy()

                from crews.browser_crew import BrowserCrew

                self._safe_emit_status("Crew", "working")
                self._safe_emit_message("Starting task execution...")

                crew_instance = BrowserCrew(
                    provider=current_settings.get("provider", "SumoPod AI"),
                    memory=current_settings.get("memory", False),
                    planning=current_settings.get("planning", False),
                    model=current_settings.get("model", "MiniMax-M2.7-highspeed"),
                    max_iter=current_settings.get("max_iter", 10),
                    sumpod_api_key=current_settings.get("sumpod_api_key"),
                    openai_api_key=current_settings.get("openai_api_key")
                )
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
