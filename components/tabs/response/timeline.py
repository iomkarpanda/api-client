from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import DataTable, Static


class ResponseTimeline(Widget):

    DEFAULT_CSS = """
        ResponseTimeline {
            width: 100%;
            height: 100%;
        }

        #response-timeline-info {
            height: 1;
            margin-bottom: 1;
        }

        #response-history {
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

    class Selected(Message):
        def __init__(self, response_id: int) -> None:
            super().__init__()
            self.response_id = response_id

    def compose(self) -> ComposeResult:
        yield Static("", id="response-timeline-info")
        yield DataTable(id="response-history")

    def on_mount(self) -> None:
        table = self.query_one("#response-history", DataTable)
        table.add_columns("Time", "Status", "Delay", "Size")
        table.cursor_type = "row"

    def set_message(self, text: str) -> None:
        self.query_one("#response-timeline-info", Static).update(text)

    def set_info(self, status_code: int, reason: str, delay_ms: int, size_bytes: int) -> None:
        status = f"{status_code} {reason}".strip()
        self.set_message(f"{status} · {delay_ms} ms · {self._format_size(size_bytes)}")

    def set_history(self, rows) -> None:
        table = self.query_one("#response-history", DataTable)
        table.clear()

        for row in rows:
            response_id = row[0]
            status_code = row[2]
            delay = row[3]
            body = row[5]
            created_at = row[7]
            table.add_row(
                str(created_at),
                str(status_code if status_code is not None else ""),
                f"{delay or 0} ms",
                self._format_size(len(body or "")),
                key=str(response_id),
            )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        event.stop()
        self.post_message(self.Selected(int(event.row_key.value)))

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes >= 1024:
            return f"{size_bytes / 1024:.1f} KB"
        return f"{size_bytes} B"
