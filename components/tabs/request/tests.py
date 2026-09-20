from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class RequestTests(Widget):
    def compose(self) -> ComposeResult:
        yield Static("Request tests")
