from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class ResponseTests(Widget):
    def compose(self) -> ComposeResult:
        yield Static("Response tests")
