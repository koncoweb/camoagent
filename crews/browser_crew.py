from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.browser_tool import get_all_tools
import os


@CrewBase
class BrowserCrew:
    """BrowserCrew untuk otomasi browser dan analisis data"""

    agents_config = '../config/agents.yaml'
    tasks_config = '../config/tasks.yaml'

    def __init__(self):
        # Inisialisasi LLM SumoPod AI dengan DeepSeek V4 Pro
        sumopod_api_key = os.environ.get("SUMOPOD_API_KEY")
        sumopod_base_url = os.environ.get("SUMOPOD_BASE_URL", "https://ai.sumopod.com/v1")

        self._llm = LLM(
            model="deepseek-v4-pro",
            api_key=sumopod_api_key,
            base_url=sumopod_base_url
        )

        # Inisialisasi Browser Tools
        self._tools = get_all_tools()

    @agent
    def navigator(self) -> Agent:
        return Agent(
            config=self.agents_config['navigator'],
            tools=self._tools,
            llm=self._llm,
            verbose=True,
            allow_delegation=True,
            max_iter=10, # Batasi iterasi agar tidak hang
            max_execution_time=120 # Timeout 2 menit
        )

    @agent
    def scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['scraper'],
            tools=self._tools,
            llm=self._llm,
            verbose=True,
            allow_delegation=True,
            max_iter=10,
            max_execution_time=120
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            llm=self._llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )

    @task
    def main_task(self) -> Task:
        return Task(
            config=self.tasks_config['main_task']
        )

    @crew
    def crew(self) -> Crew:
        """Membuat instance Crew untuk eksekusi tugas"""
        return Crew(
            agents=self.agents,  # Otomatis diambil dari @agent
            tasks=self.tasks,    # Otomatis diambil dari @task
            process=Process.hierarchical,
            manager_llm=self._llm,
            memory=False, # Disable memory untuk mencegah error embedding dari OpenAI default
            planning=False, # Disable planning karena juga dapat memicu pencarian model embedding
            verbose=True
        )

    def get_crew(self) -> Crew:
        """Method pembantu untuk kompatibilitas dengan kode yang ada"""
        return self.crew()
