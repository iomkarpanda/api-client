from textual.widgets import TabPane
from textual.widget import Widget
from textual.app import ComposeResult
from components.tabbed import HelpTabbedContent
from components.tabs.response.body import ResponseBody
from components.tabs.response.preview import ResponsePreview
from components.tabs.response.headers import ResponseHeaders
from components.tabs.response.cookies import ResponseCookies
from components.tabs.response.tests import ResponseTests
from components.tabs.response.timeline import ResponseTimeline

class Response(Widget):

    BORDER_TITLE = "Response"

    DEFAULT_CSS = """
        Response{
            width: 100%;
            height: 50%;
            border: round white;
            background: black;
        }

        TabbedContent{
            height: 100%;
            padding: 1;
        }

        TabbedContent TabPane {
            height: 1fr;
        }
    """

    def compose(self) -> ComposeResult:
        with HelpTabbedContent(
            "Body",
            "Preview",
            "Headers",
            "Cookies",
            "Tests",
            "Timeline",
            initial="body",
        ):
            yield TabPane("Body", ResponseBody(), id="body")
            yield TabPane("Preview", ResponsePreview(), id="preview")
            yield TabPane("Headers", ResponseHeaders(), id="headers")
            yield TabPane("Cookies", ResponseCookies(), id="cookies")
            yield TabPane("Tests", ResponseTests(), id="tests")
            yield TabPane("Timeline", ResponseTimeline(), id="timeline")