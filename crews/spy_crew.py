from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.spy_tools import MarketScanTool, ReviewMinerTool, StoreProfilerTool, GapAnalyzeTool, KeywordExtractorTool
from tools.browser_tool import get_all_tools as get_browser_tools
import os


@CrewBase
class SpyCrew:
    """SpyCrew v2.0 — Market Intelligence & Competitor Analysis untuk Shopee Indonesia"""

    agents_config = '../config/spy_agents.yaml'
    tasks_config = '../config/spy_tasks.yaml'

    def __init__(self, provider="SumoPod AI", memory=True, planning=True, model="MiniMax-M2.7-highspeed", max_iter=20, sumpod_api_key=None, openai_api_key=None):
        self.memory = memory
        self.planning = planning
        self.max_iter = max_iter

        if provider == "Official OpenAI":
            api_key = openai_api_key if openai_api_key else os.environ.get("OPENAI_API_KEY")
            base_url = None
        else:
            api_key = sumpod_api_key if sumpod_api_key else os.environ.get("SUMOPOD_API_KEY")
            base_url = os.environ.get("SUMOPOD_BASE_URL", "https://ai.sumopod.com/v1")

        self._llm = LLM(
            model=model,
            api_key=api_key,
            base_url=base_url,
            max_tokens=4096
        )

        self._browser_tools = get_browser_tools()
        self._spy_tools = [MarketScanTool(), ReviewMinerTool(), StoreProfilerTool(), GapAnalyzeTool(), KeywordExtractorTool()]
        self._all_tools = self._browser_tools + self._spy_tools

    @agent
    def market_scanner(self) -> Agent:
        return Agent(
            config=self.agents_config['market_scanner'],
            tools=self._all_tools,
            llm=self._llm,
            verbose=True,
            allow_delegation=True,
            max_iter=self.max_iter,
            max_execution_time=300
        )

    @agent
    def competitor_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['competitor_profiler'],
            tools=self._spy_tools,
            llm=self._llm,
            verbose=True,
            allow_delegation=False,
            max_iter=self.max_iter,
            max_execution_time=180
        )

    @agent
    def trend_detector(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_detector'],
            tools=self._all_tools,
            llm=self._llm,
            verbose=True,
            allow_delegation=False,
            max_iter=self.max_iter,
            max_execution_time=180
        )

    @agent
    def strategy_synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config['strategy_synthesizer'],
            tools=[],
            llm=self._llm,
            verbose=True,
            allow_delegation=False,
            max_iter=self.max_iter,
            max_execution_time=240
        )

    @task
    def scan_market_task(self) -> Task:
        return Task(
            config=self.tasks_config['scan_market_task'],
            agent=self.market_scanner()
        )

    @task
    def profile_competitors_task(self) -> Task:
        return Task(
            config=self.tasks_config['profile_competitors_task'],
            agent=self.competitor_profiler()
        )

    @task
    def detect_trends_task(self) -> Task:
        return Task(
            config=self.tasks_config['detect_trends_task'],
            agent=self.trend_detector()
        )

    @task
    def synthesize_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesize_strategy_task'],
            agent=self.strategy_synthesizer()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=self.memory,
            planning=self.planning,
            verbose=True
        )

    def get_crew(self) -> Crew:
        return self.crew()

    def kickoff(self, task_override: str = None):
        crew = self.get_crew()
        if task_override:
            return crew.kickoff(inputs={'task': task_override})
        return crew.kickoff()
