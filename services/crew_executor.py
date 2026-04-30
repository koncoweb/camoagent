import threading
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

from tools.browser_tool import BrowserConfig


class CrewExecutor(QObject):
    status_update = pyqtSignal(str, str)
    message_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._config = BrowserConfig.get_instance()
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def set_page(self, page):
        self._config.set_page(page)

    def execute_task(self, task_description: str, page):
        if page is None:
            self.message_ready.emit("Please open the browser first using the 🦊 button.")
            return

        self.set_page(page)

        def run_crew():
            try:
                from crews.browser_crew import BrowserCrew

                self.status_update.emit("Crew", "working")
                self.message_ready.emit("Starting task execution...")

                crew_instance = BrowserCrew()
                crew = crew_instance.get_crew()

                result = crew.kickoff(inputs={"task": task_description})

                self.status_update.emit("Crew", "ready")
                self.message_ready.emit(f"Task completed:\n\n{str(result.raw)}")

            except Exception as e:
                error_msg = str(e)
                self.status_update.emit("Crew", "error")
                
                # Make quota errors more user-friendly
                if "insufficient_quota" in error_msg:
                    friendly_msg = (
                        "Error: Kuota AI Provider Anda habis atau belum diatur (insufficient_quota).\n"
                        "Silakan cek saldo/billing di provider yang Anda gunakan (SumoPod/OpenAI)."
                    )
                    self.message_ready.emit(friendly_msg)
                else:
                    self.message_ready.emit(f"Error:\n{error_msg}")

        threading.Thread(target=run_crew, daemon=True).start()

    def stop(self):
        pass
