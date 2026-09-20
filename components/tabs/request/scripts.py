from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class RequestScripts(Widget):
    def compose(self) -> ComposeResult:
        yield Static("Pre-request script")
