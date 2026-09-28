from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable


class ResponseCookies(Widget):

    DEFAULT_CSS = """
        ResponseCookies {
            width: 100%;
            height: 100%;
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
        yield DataTable(id="response-cookies")

    def on_mount(self) -> None:
        self.query_one("#response-cookies", DataTable).add_columns("Key", "Value")

    def set_rows(self, rows) -> None:
        table = self.query_one("#response-cookies", DataTable)
        table.clear()
        for key, value in rows:
            table.add_row(str(key), str(value))
