from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane
from components.tabs.request.headers import RequestHeader
from components.tabs.request.authorization import RequestHeader as Authorization
from components.tabs.request.params import RequestParams
from components.tabs.request.body import RequestBody

class Request(Widget):

    BORDER_TITLE = "Request"

    DEFAULT_CSS = """

        Request{
            width: 100%;
            height: 40%;
            background: black;
            border: round white;
        }

        TabbedContent {
            height: 100%;
            padding: 1;
        }

        TabbedContent TabPane {
            height: 1fr;
        }


    """

    def compose(self) -> ComposeResult:
        with TabbedContent(
            "Params",
            "Headers",
            "Authorization",
            "Body",
            initial="params",
        ):
            yield TabPane("Params", RequestParams(), id="params")
            yield TabPane("Headers", RequestHeader(), id="headers")
            yield TabPane("Authorization", Authorization(), id="authorization")
            yield TabPane("Body", RequestBody(), id="body")
