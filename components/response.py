from textual.widgets import TabPane
from textual.widget import Widget
from textual.app import ComposeResult
from components.tabbed import HelpTabbedContent
from components.tabs.response.body import ResponseBody
from components.tabs.response.preview import ResponsePreview
from components.tabs.response.headers import ResponseHeaders
from components.tabs.response.cookies import ResponseCookies
from components.tabs.response.tests import ResponseTests
from components.tabs.response.timeline import ResponseTimeline
from db.responses import get_responses

class Response(Widget):

    BORDER_TITLE = "Response"

    DEFAULT_CSS = """
        Response{
            width: 100%;
            height: 50%;
            border: round white;
            background: black;
        }

        TabbedContent{
            height: 100%;
            padding: 1 1 0 1;
        }

        TabbedContent TabPane {
            height: 1fr;
        }
    """

    def __init__(self) -> None:
        super().__init__()
        self.responses: dict[int, tuple] = {}

    def compose(self) -> ComposeResult:
        with HelpTabbedContent(
            "Body",
            "Preview",
            "Headers",
            "Cookies",
            "Tests",
            "Timeline",
            initial="body",
        ):
            yield TabPane("Body", ResponseBody(), id="body")
            yield TabPane("Preview", ResponsePreview(), id="preview")
            yield TabPane("Headers", ResponseHeaders(), id="headers")
            yield TabPane("Cookies", ResponseCookies(), id="cookies")
            yield TabPane("Tests", ResponseTests(), id="tests")
            yield TabPane("Timeline", ResponseTimeline(), id="timeline")

    def load_history(self, request_id: int | None) -> None:
        try:
            rows = get_responses(request_id) if request_id is not None else []
        except Exception:
            rows = []

        self.responses = {row[0]: row for row in rows}
        history = list(reversed(rows))
        self.query_one(ResponseTimeline).set_history(history)

        if history:
            self._show_row(history[0])
        else:
            self._clear()

    def on_response_timeline_selected(self, event: ResponseTimeline.Selected) -> None:
        event.stop()
        row = self.responses.get(event.response_id)
        if row is not None:
            self._show_row(row)

    def show(self, response, delay_ms: int) -> None:
        """Display a live response (no stored row, e.g. ad-hoc sends)."""
        self.query_one(ResponseBody).set_body(response.text or "")
        self.query_one(ResponseHeaders).set_rows(response.headers.items())
        self.query_one(ResponseCookies).set_rows(dict(response.cookies).items())
        self.query_one(ResponseTimeline).set_info(
            response.status_code,
            response.reason or "",
            delay_ms,
            len(response.content or b""),
        )

    def show_error(self, message: str) -> None:
        self.query_one(ResponseTimeline).set_message(f"Request failed: {message}")

    def _show_row(self, row: tuple) -> None:
        status_code, delay, headers, body, cookies = row[2], row[3], row[4], row[5], row[6]
        self.query_one(ResponseBody).set_body(body or "")
        self.query_one(ResponseHeaders).set_rows((headers or {}).items())
        self.query_one(ResponseCookies).set_rows((cookies or {}).items())
        self.query_one(ResponseTimeline).set_info(
            status_code if status_code is not None else 0,
            "",
            delay or 0,
            len(body or ""),
        )

    def _clear(self) -> None:
        self.query_one(ResponseBody).set_body("")
        self.query_one(ResponseHeaders).set_rows([])
        self.query_one(ResponseCookies).set_rows([])
        self.query_one(ResponseTimeline).set_message("")
