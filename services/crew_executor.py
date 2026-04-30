import threading
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

from tools.browser_tool import BrowserConfig


class CrewExecutor(QObject):
    status_update = pyqtSignal(str, str)
    message_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._config = BrowserConfig()
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
                self.message_ready.emit(f"Task completed: {str(result.raw)[:500]}")

            except Exception as e:
                error_msg = str(e)
                self.status_update.emit("Crew", "error")
                
                # Make OpenAI quota errors more user-friendly
                if "insufficient_quota" in error_msg:
                    friendly_msg = (
                        "Error: Kuota OpenAI API Anda habis atau belum diatur (insufficient_quota).\n"
                        "Catatan: API Key berbeda dengan langganan ChatGPT Plus. "
                        "Silakan cek platform.openai.com/account/billing untuk menambahkan saldo prabayar."
                    )
                    self.message_ready.emit(friendly_msg)
                else:
                    self.message_ready.emit(f"Error: {error_msg[:500]}")

        threading.Thread(target=run_crew, daemon=True).start()

    def stop(self):
        pass
