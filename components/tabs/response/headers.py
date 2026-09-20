from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable


class ResponseHeaders(Widget):

    DEFAULT_CSS = """
        ResponseHeaders {
            width: 100%;
            height: 100%;
        }

        ResponseHeaders DataTable {
            width: 100%;
            height: 1fr;
            background: black;
            color: white;
            scrollbar-size-vertical: 1;

            & > .datatable--header {
                background: #16a085;
                color: white;
            }

            & > .datatable--odd-row,
            & > .datatable--even-row {
                background: black !important;
                color: white;
            }
        }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="response-headers")

    def on_mount(self) -> None:
        table = self.query_one("#response-headers", DataTable)
        table.add_columns("Key", "Value")
        table.add_rows(
            [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", "482"),
                ("Server", "nginx/1.24.0"),
                ("Cache-Control", "no-store"),
                ("Connection", "keep-alive"),
                ("Date", "20 Sep 2026 10:15:30 GMT"),
                ("X-Request-ID", "request-12345"),
                ("X-RateLimit-Limit", "100"),
                ("X-RateLimit-Remaining", "97"),
                ("Strict-Transport-Security", "max-age=31536000"),
            ]
        )
