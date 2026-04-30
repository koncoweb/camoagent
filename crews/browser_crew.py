from crewai import Agent, Task, Crew, Process, LLM
from tools.browser_tool import get_current_page_info, navigate_to_url, get_page_content, click_element, type_text
import os


class BrowserCrew:
    def __init__(self):
        # Explicitly set the LLM to use SumoPod AI
        sumopod_api_key = os.environ.get("SUMOPOD_API_KEY")
        sumopod_base_url = os.environ.get("SUMOPOD_BASE_URL", "https://ai.sumopod.com/v1")
        
        self._llm = LLM(
            model="gpt-4o-mini",
            api_key=sumopod_api_key,
            base_url=sumopod_base_url
        )
        
        # Define the set of tools our agents can use
        self._tools = [get_current_page_info, navigate_to_url, get_page_content, click_element, type_text]

    def get_navigator_agent(self) -> Agent:
        return Agent(
            role="Browser Navigator",
            goal="Navigate and interact with web pages accurately",
            backstory="""You are an expert web navigator with deep knowledge of HTML structure,
            CSS selectors, and web interaction patterns. You excel at finding the right elements
            on complex web pages and performing actions like clicking, typing, and scrolling.""",
            tools=self._tools,
            verbose=True,
            allow_delegation=True,
            llm=self._llm
        )

    def get_scraper_agent(self) -> Agent:
        return Agent(
            role="Data Scraper",
            goal="Extract structured data from web pages accurately",
            backstory="""You are a skilled data scraper who can identify and extract
            relevant information from HTML pages. You understand table structures, list items,
            and how to parse dynamic web content. You take screenshots when visual data is needed.""",
            tools=self._tools,
            verbose=True,
            allow_delegation=True,
            llm=self._llm
        )

    def get_analyst_agent(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data and provide actionable insights",
            backstory="""You are an experienced data analyst who can interpret numerical data,
            calculate metrics, and generate meaningful insights. You're skilled at ROI calculations,
            statistical analysis, and presenting findings in a clear format.""",
            tools=[],
            verbose=True,
            allow_delegation=False,
            llm=self._llm
        )

    def get_reporter_agent(self) -> Agent:
        return Agent(
            role="Report Generator",
            goal="Format and present analysis results clearly",
            backstory="""You are an expert at presenting data in clear, actionable formats.
            You can create markdown reports, summaries, and visual descriptions that make
            complex data easy to understand.""",
            tools=[],
            verbose=True,
            allow_delegation=False,
            llm=self._llm
        )

    def get_crew(self) -> Crew:
        navigator = self.get_navigator_agent()
        scraper = self.get_scraper_agent()

        # We create a single dynamic task that adapts to user input
        dynamic_task = Task(
            description="""You are a Super Browser Agent. 
            The user wants you to do this: {task}
            
            Use the browser tool available to you to accomplish this request. You MUST use the tool to interact with the browser.
            - If they ask what page is open or what the URL/title is, ALWAYS use the 'get_info' action.
            - If they ask to navigate, use the 'goto' action.
            - If they ask for analysis, gather the data first using 'get_content' or 'get_element' then analyze it.
            
            Do not hallucinate data. Only report what you find using the tools.
            If the user's request is simple (like asking the current page), just answer simply.
            """,
            expected_output="A direct, helpful, and accurate response fulfilling the user's exact request based on the actual browser state.",
            agent=navigator
        )

        return Crew(
            agents=[navigator, scraper],
            tasks=[dynamic_task],
            process=Process.sequential,
            verbose=True
        )
