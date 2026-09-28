from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TextArea


class RequestBody(Widget):

    DEFAULT_CSS = """
        RequestBody {
            width: 100%;
            height: 100%;
        }

        #request-body {
            height: 1fr;
            background: black;
        }

        #request-body .text-area--gutter {
            background: black;
            color: #585858;
        }

        #request-body .text-area--cursor-line {
            background: #151515;
        }
    """

    def compose(self) -> ComposeResult:
        yield TextArea(id="request-body")

    def load(self, text: str) -> None:
        self.query_one("#request-body", TextArea).text = text or ""

    def value(self) -> str:
        return self.query_one("#request-body", TextArea).text
