from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Static


class ResponseHeaders(Widget):

    DEFAULT_CSS = """
        ResponseHeaders {
            width: 100%;
            height: 100%;
        }

        ResponseHeaders Static {
            height: 1;
            padding: 0 1;
            color: #808080;
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
        yield Static("No headers yet", id="response-headers-hint")
        yield DataTable(id="response-headers")

    def on_mount(self) -> None:
        self.query_one("#response-headers", DataTable).add_columns("Key", "Value")

    def set_rows(self, rows) -> None:
        table = self.query_one("#response-headers", DataTable)
        table.clear()
        for key, value in rows:
            table.add_row(str(key), str(value))

        self.query_one("#response-headers-hint", Static).display = not table.row_count
