from crewai.tools import BaseTool, tool
from pydantic import BaseModel, Field
from typing import Type, Optional, Any


class BrowserConfig:
    _instance = None
    _page: Optional[Any] = None
    _lock = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            import threading
            cls._lock = threading.Lock()
        return cls._instance

    def set_page(self, page: Any):
        with self._lock:
            self._page = page

    def get_page(self) -> Optional[Any]:
        with self._lock:
            return self._page


@tool("get_current_page_info")
def get_current_page_info() -> str:
    """Use this tool to get the URL and Title of the webpage that the user is currently viewing."""
    page = BrowserConfig().get_page()
    if page is None:
        return "Error: Browser not ready."
    try:
        return f"Current URL: {page.url}\nCurrent Title: {page.title()}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool("navigate_to_url")
def navigate_to_url(url: str) -> str:
    """Use this tool to navigate the browser to a specific URL."""
    page = BrowserConfig().get_page()
    if page is None:
        return "Error: Browser not ready."
    try:
        page.goto(url)
        return f"Successfully navigated to {url}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool("get_page_content")
def get_page_content() -> str:
    """Use this tool to get the full HTML content of the current webpage."""
    page = BrowserConfig().get_page()
    if page is None:
        return "Error: Browser not ready."
    try:
        return page.content()
    except Exception as e:
        return f"Error: {str(e)}"

@tool("click_element")
def click_element(selector: str) -> str:
    """Use this tool to click an element on the page using a CSS selector."""
    page = BrowserConfig().get_page()
    if page is None:
        return "Error: Browser not ready."
    try:
        el = page.query_selector(selector)
        if el:
            el.click()
            return f"Successfully clicked element: {selector}"
        return f"Element not found: {selector}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool("type_text")
def type_text(selector: str, text: str) -> str:
    """Use this tool to type text into an input field on the page using a CSS selector."""
    page = BrowserConfig().get_page()
    if page is None:
        return "Error: Browser not ready."
    try:
        el = page.query_selector(selector)
        if el:
            el.fill(text)
            return f"Successfully typed text into: {selector}"
        return f"Element not found: {selector}"
    except Exception as e:
        return f"Error: {str(e)}"

# Keep the old class just in case anything else imports it, but we will use the new tools
class BrowserToolInput(BaseModel):
    action: str = Field(..., description="Action: goto, screenshot, get_content, get_element, click, type_text, get_info")
    value: Optional[str] = Field(default="", description="URL, selector, or 'selector|text' for type_text. Can be empty for get_info and get_content.")


class BrowserTool(BaseTool):
    name: str = "browser"
    description: str = """Browser control tool. Actions:
    - goto: Navigate to URL (value = URL)
    - screenshot: Take screenshot (value = optional file path)
    - get_info: Get current page URL and Title
    - get_content: Get page HTML content
    - get_element: Get element text (value = CSS selector)
    - click: Click element (value = CSS selector)
    - type_text: Type into input (value = 'selector|text')"""
    args_schema: Type[BaseModel] = BrowserToolInput

    def __init__(self):
        super().__init__()
        self._config = BrowserConfig()

    def _run(self, action: str, value: Optional[str] = None) -> str:
        page = self._config.get_page()

        if page is None:
            return "Error: Browser not ready. Please open the browser first."

        try:
            if action == "goto":
                page.goto(value)
                return f"Navigated to {value}"

            elif action == "get_info":
                return f"Current URL: {page.url}\nCurrent Title: {page.title()}"

            elif action == "screenshot":
                path = value if value else "screenshot.png"
                page.screenshot(path=path)
                return f"Screenshot saved to {path}"

            elif action == "get_content":
                return page.content()

            elif action == "get_element":
                el = page.query_selector(value)
                if el:
                    return el.inner_text()
                return f"Element not found: {value}"

            elif action == "click":
                el = page.query_selector(value)
                if el:
                    el.click()
                    return f"Clicked: {value}"
                return f"Element not found: {value}"

            elif action == "type_text":
                if value and "|" in value:
                    selector, text = value.split("|", 1)
                    el = page.query_selector(selector)
                    if el:
                        el.fill(text)
                        return f"Typed '{text}' into {selector}"
                    return f"Element not found: {selector}"
                return "Error: Use format 'selector|text'"

            return f"Unknown action: {action}"

        except Exception as e:
            return f"Error: {str(e)}"
