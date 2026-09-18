from textual.widgets import Static
from textual.widget import Widget

class RequestHeader(Widget):

    def compose(self):
        yield Static("Authorization")