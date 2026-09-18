from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class ResponseCookies(Widget):
    def compose(self) -> ComposeResult:
        yield Static("Response cookies")
