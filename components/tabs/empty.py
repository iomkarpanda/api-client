from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class EmptyState(Widget):
    """Centered placeholder for tabs that aren't implemented yet."""

    DEFAULT_CSS = """
        EmptyState {
            width: 100%;
            height: 100%;
            align: center middle;
        }

        EmptyState Static {
            color: #808080;
        }
    """

    def __init__(self, empty_message: str) -> None:
        super().__init__()
        self.empty_message = empty_message

    def compose(self) -> ComposeResult:
        yield Static(self.empty_message)
