from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class ResponsePreview(Widget):
    def compose(self) -> ComposeResult:
        yield Static("Response preview")
