from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import TabPane
from components.tabbed import HelpTabbedContent
from components.tabs.request.headers import RequestHeader
from components.tabs.request.authorization import RequestHeader as Authorization
from components.tabs.request.params import RequestParams
from components.tabs.request.body import RequestBody
from components.tabs.request.cookies import RequestCookies
from components.tabs.request.scripts import RequestScripts
from components.tabs.request.tests import RequestTests

class Request(Widget):

    BORDER_TITLE = "Request"

    DEFAULT_CSS = """

        Request{
            width: 100%;
            height: 50%;
            background: black;
            border: round white;
        }

        TabbedContent {
            height: 100%;
            padding: 1 1 0 1;
        }

        TabbedContent TabPane {
            height: 1fr;
        }


    """

    def compose(self) -> ComposeResult:
        with HelpTabbedContent(
            "Params",
            "Headers",
            "Authorization",
            "Body",
            "Cookies",
            "Scripts",
            "Tests",
            initial="params",
        ):
            yield TabPane("Params", RequestParams(), id="params")
            yield TabPane("Headers", RequestHeader(), id="headers")
            yield TabPane("Authorization", Authorization(), id="authorization")
            yield TabPane("Body", RequestBody(), id="body")
            yield TabPane("Cookies", RequestCookies(), id="cookies")
            yield TabPane("Scripts", RequestScripts(), id="scripts")
            yield TabPane("Tests", RequestTests(), id="tests")
