from textual.widgets import TabbedContent, TabPane
from textual.widget import Widget
from textual.app import ComposeResult
from components.tabs.response.body import ResponseBody
from components.tabs.response.preview import ResponsePreview
from components.tabs.response.headers import ResponseHeaders
from components.tabs.response.cookies import ResponseCookies
from components.tabs.response.tests import ResponseTests

class Response(Widget):

    BORDER_TITLE = "Response"

    DEFAULT_CSS = """
        Response{
            width: 100%;
            height: 60%;
            border: round white;
            background: black;
        }

        TabbedContent{
            padding: 1;
        }
    """

    def compose(self) -> ComposeResult:
        with TabbedContent(
            "Body",
            "Preview",
            "Headers",
            "Cookies",
            "Tests",
            initial="body",
        ):
            yield TabPane("Body", ResponseBody(), id="body")
            yield TabPane("Preview", ResponsePreview(), id="preview")
            yield TabPane("Headers", ResponseHeaders(), id="headers")
            yield TabPane("Cookies", ResponseCookies(), id="cookies")
            yield TabPane("Tests", ResponseTests(), id="tests")