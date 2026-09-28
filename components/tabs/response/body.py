import json

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TextArea


class ResponseBody(Widget):

    DEFAULT_CSS = """
        ResponseBody {
            width: 100%;
            height: 100%;
        }

        #response-body {
            height: 1fr;
            background: black;
        }
    """

    def compose(self) -> ComposeResult:
        yield TextArea(id="response-body", read_only=True)

    def set_body(self, text: str) -> None:
        self.query_one("#response-body", TextArea).text = self._format(text)

    @staticmethod
    def _format(text: str) -> str:
        try:
            return json.dumps(json.loads(text), indent=2)
        except (ValueError, TypeError):
            return text or ""
