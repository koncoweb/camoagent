from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.shopee_tools import (
    ExtractShopeeAdsMetricsTool,
    CalculateActualFinancialsTool,
    GenerateAdsRecommendationTool,
    get_shopee_tools
)
from tools.browser_tool import get_all_tools as get_browser_tools
import os


@CrewBase
class ShopeeCrew:
    """ShopeeCrew untuk analisis dan optimasi iklan Shopee"""

    agents_config = '../config/shopee_agents.yaml'
    tasks_config = '../config/shopee_tasks.yaml'

    def __init__(self, provider="SumoPod AI", memory=False, planning=False, model="deepseek-v4-pro", max_iter=10, sumpod_api_key=None, openai_api_key=None):
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

        all_tools = get_browser_tools() + get_shopee_tools()
        self._all_tools = all_tools

    @agent
    def shopee_navigator(self) -> Agent:
        return Agent(
            config=self.agents_config['shopee_navigator'],
            tools=self._all_tools,
            llm=self._llm,
            verbose=True,
            allow_delegation=False,
            max_iter=self.max_iter,
            max_execution_time=180
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            tools=get_shopee_tools(),
            llm=self._llm,
            verbose=True,
            allow_delegation=False,
            max_iter=self.max_iter,
            max_execution_time=120
        )

    @agent
    def ads_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['ads_optimizer'],
            tools=get_shopee_tools(),
            llm=self._llm,
            verbose=True,
            allow_delegation=True,
            max_iter=self.max_iter,
            max_execution_time=120
        )

    @task
    def extract_ads_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_ads_task'],
            agent=self.shopee_navigator()
        )

    @task
    def calculate_financials_task(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_financials_task'],
            agent=self.financial_analyst()
        )

    @task
    def generate_recommendations_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_recommendations_task'],
            agent=self.ads_optimizer()
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
            override_task = Task(
                description=task_override,
                expected_output="Complete analysis with actionable recommendations"
            )
            return crew.kickoff(inputs={'task': task_override})
        
        return crew.kickoff()
