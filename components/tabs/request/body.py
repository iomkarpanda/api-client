from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class RequestBody(Widget):
    def compose(self) -> ComposeResult:
        yield Static("Request body")
