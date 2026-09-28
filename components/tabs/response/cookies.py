from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Static


class ResponseCookies(Widget):

    DEFAULT_CSS = """
        ResponseCookies {
            width: 100%;
            height: 100%;
        }

        ResponseCookies Static {
            height: 1;
            padding: 0 1;
            color: #808080;
        }

        ResponseCookies DataTable {
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
        yield Static("No cookies yet", id="response-cookies-hint")
        yield DataTable(id="response-cookies")

    def on_mount(self) -> None:
        self.query_one("#response-cookies", DataTable).add_columns("Key", "Value")

    def set_rows(self, rows) -> None:
        table = self.query_one("#response-cookies", DataTable)
        table.clear()
        for key, value in rows:
            table.add_row(str(key), str(value))

        self.query_one("#response-cookies-hint", Static).display = not table.row_count
