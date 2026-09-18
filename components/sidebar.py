from textual.widgets import Static
from textual.app import ComposeResult
from textual.widget import Widget

class Sidebar(Widget):

    BORDER_TITLE = "Collections"

    DEFAULT_CSS = """
        Sidebar {
            width: 20%;
            height: 100%;
            background: black;
            border: round white;
        }



        
    """

    def compose(self) -> ComposeResult:
        yield Static(id="sidebar")

    