from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Any


class BrowserConfig:
    _instance = None
    _page: Optional[Any] = None
    _queue: Optional[Any] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_page(self, page: Any):
        self._page = page

    def get_page(self) -> Optional[Any]:
        return self._page

    def set_queue(self, queue: Any):
        self._queue = queue

    def execute_command(self, action: str, params: dict = None) -> str:
        if self._queue is None:
            return "Error: Browser command queue not initialized."
        
        from queue import Queue
        result_queue = Queue()
        
        self._queue.put({
            "action": action,
            "params": params or {},
            "result_queue": result_queue
        })
        
        try:
            # Wait for result with timeout
            result = result_queue.get(timeout=30)
            if result["status"] == "success":
                return result["data"]
            else:
                return f"Error: {result['message']}"
        except Exception as e:
            return f"Error: Command timed out or failed: {str(e)}"


class GetCurrentPageInfoInput(BaseModel):
    pass


class GetCurrentPageInfoTool(BaseTool):
    name: str = "get_current_page_info"
    description: str = "Use this tool to get the URL and Title of the webpage that the user is currently viewing. This is the FIRST tool you should use when the user asks about the current page or browser state."
    args_schema: Type[BaseModel] = GetCurrentPageInfoInput

    def _run(self, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("get_info")


class NavigateToUrlInput(BaseModel):
    url: str = Field(..., description="The URL to navigate to")


class NavigateToUrlTool(BaseTool):
    name: str = "navigate_to_url"
    description: str = "Use this tool to navigate the browser to a specific URL. Required: url parameter."
    args_schema: Type[BaseModel] = NavigateToUrlInput

    def _run(self, url: str, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("goto", {"url": url})


class GetPageContentInput(BaseModel):
    pass


class GetPageContentTool(BaseTool):
    name: str = "get_page_content"
    description: str = "Use this tool to get the full HTML content of the current webpage. Only use this if you need raw HTML."
    args_schema: Type[BaseModel] = GetPageContentInput

    def _run(self, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("get_content")


class GetPageTextInput(BaseModel):
    pass

class GetPageTextTool(BaseTool):
    name: str = "get_page_text"
    description: str = "Use this tool to get ONLY the visible text (innerText) of the current webpage. This is HIGHLY PREFERRED over get_page_content for reading articles, data, or scraping Shopee/E-commerce sites."
    args_schema: Type[BaseModel] = GetPageTextInput

    def _run(self, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("get_text")


class ScrollDownInput(BaseModel):
    pass

class ScrollDownTool(BaseTool):
    name: str = "scroll_down"
    description: str = "Use this tool to scroll down the page. Extremely useful for e-commerce sites like Shopee that use lazy-loading to load more products or data."
    args_schema: Type[BaseModel] = ScrollDownInput

    def _run(self, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("scroll_down")


class ClickElementInput(BaseModel):
    selector: str = Field(..., description="CSS selector of the element to click")


class ClickElementTool(BaseTool):
    name: str = "click_element"
    description: str = "Use this tool to click an element on the page using a CSS selector. Example: button.submit, input#username"
    args_schema: Type[BaseModel] = ClickElementInput

    def _run(self, selector: str, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("click", {"selector": selector})


class TypeTextInput(BaseModel):
    selector: str = Field(..., description="CSS selector of the input element")
    text: str = Field(..., description="Text to type into the element")


class TypeTextTool(BaseTool):
    name: str = "type_text"
    description: str = "Use this tool to type text into an input field on the page using a CSS selector."
    args_schema: Type[BaseModel] = TypeTextInput

    def _run(self, selector: str, text: str, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("type", {"selector": selector, "text": text})


class PressKeyInput(BaseModel):
    key: str = Field(..., description="Key to press: 'Escape', 'Enter', 'Tab', 'Backspace', 'ArrowUp', 'ArrowDown', etc.")


class PressKeyTool(BaseTool):
    name: str = "press_key"
    description: str = "Press a keyboard key. CRITICAL for closing React/Headless UI modals - press 'Escape' to close them. Also useful for navigating forms."
    args_schema: Type[BaseModel] = PressKeyInput

    def _run(self, key: str, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("press_key", {"key": key})


class EvaluateJSInput(BaseModel):
    script: str = Field(..., description="JavaScript code to execute. Can return a value.")


class EvaluateJSTool(BaseTool):
    name: str = "evaluate_js"
    description: str = "Execute custom JavaScript code on the page. Use this for complex DOM manipulation like removing React portals, closing modals, or any custom logic that regular tools can't handle."
    args_schema: Type[BaseModel] = EvaluateJSInput

    def _run(self, script: str, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("evaluate_js", {"script": script})


class DismissDialogInput(BaseModel):
    pass


class DismissDialogTool(BaseTool):
    name: str = "dismiss_dialog"
    description: str = "SPECIFICALLY designed to close modal dialogs, popups, and overlays. Tries multiple methods: 1) Press Escape key, 2) Click backdrop/overlay, 3) Click close button, 4) Remove portal elements. Use this FIRST before any other method for closing dialogs."
    args_schema: Type[BaseModel] = DismissDialogInput

    def _run(self, **kwargs) -> str:
        return BrowserConfig.get_instance().execute_command("dismiss_dialog", {})


def get_all_tools():
    return [
        GetCurrentPageInfoTool(),
        NavigateToUrlTool(),
        GetPageContentTool(),
        GetPageTextTool(),
        ScrollDownTool(),
        ClickElementTool(),
        TypeTextTool(),
        PressKeyTool(),
        EvaluateJSTool(),
        DismissDialogTool(),
    ]
