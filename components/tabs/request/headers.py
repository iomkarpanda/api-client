from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input


class RequestHeader(Widget):

    BINDINGS = [
        ("delete", "delete_header", "Delete selected header"),
        ("a", "show_add_form", "Add header"),
    ]

    DEFAULT_CSS = """
        RequestHeader {
            width: 100%;
            height: 100%;
        }

        RequestHeader DataTable {
            width: 100%;
            height: 1fr;
            background: black;
            color: white;
            scrollbar-size-vertical: 1;

            & > .datatable--header {
                background: #4a90e2;
                color: white;
            }

            & > .datatable--odd-row,
            & > .datatable--even-row {
                background: black !important;
                color: white;
            }
        }

        #header-controls {
            width: 100%;
            height: 3;
            margin-bottom: 1;
        }

        #header-controls Button {
            width: 5;
            min-width: 5;
            height: 3;
            min-height: 3;
            padding: 0;
        }

        #header-form {
            width: 100%;
            height: 3;
            margin-bottom: 1;
            display: none;
        }

        #header-form.-visible {
            display: block;
        }

        #header-form Input {
            width: 1fr;
            margin-right: 1;
        }

        #header-form Button {
            width: 10;
            margin-left: 1;
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="header-controls"):
            yield Button("+", id="show-add-header")
        with Horizontal(id="header-form"):
            yield Input(placeholder="Key", id="header-key")
            yield Input(placeholder="Value", id="header-value")
            yield Button("Add", id="add-header")
            yield Button("Cancel", id="cancel-add-header")
        yield DataTable(id="request-headers")

    def on_mount(self) -> None:
        table = self.query_one("#request-headers", DataTable)
        table.add_columns("Key", "Value")
        table.add_rows(
            [
                ("Accept", "application/json"),
                ("Content-Type", "application/json"),
                ("Authorization", "Bearer sample-token"),
                ("Cache-Control", "no-cache"),
                ("Connection", "keep-alive"),
                ("Host", "api.example.com"),
                ("User-Agent", "API Client/1.0"),
                ("X-Request-ID", "request-12345"),
                ("X-Client-Version", "1.0.0"),
                ("Accept-Encoding", "gzip, deflate"),
                ("Accept-Language", "en-US"),
                ("Origin", "https://app.example.com"),
            ]
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        table = self.query_one("#request-headers", DataTable)

        if event.button.id == "show-add-header":
            self.action_show_add_form()

        elif event.button.id == "cancel-add-header":
            self.action_hide_add_form()

        elif event.button.id == "add-header":
            key_input = self.query_one("#header-key", Input)
            value_input = self.query_one("#header-value", Input)
            key = key_input.value.strip()
            value = value_input.value.strip()

            if key:
                table.add_row(key, value)
                key_input.value = ""
                value_input.value = ""
                self.action_hide_add_form()

    def action_show_add_form(self) -> None:
        form = self.query_one("#header-form")
        form.add_class("-visible")
        self.query_one("#header-key", Input).focus()

    def action_hide_add_form(self) -> None:
        self.query_one("#header-form").remove_class("-visible")

    def action_delete_header(self) -> None:
        table = self.query_one("#request-headers", DataTable)
        if table.row_count:
            row_key = table.ordered_rows[table.cursor_row].key
            table.remove_row(row_key)