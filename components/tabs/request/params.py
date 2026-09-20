from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input


class RequestParams(Widget):

    BINDINGS = [
        ("delete", "delete_param", "Delete"),
        ("e", "edit_param", "Edit"),
        ("escape", "cancel_edit", "Cancel edit"),
    ]

    _editing_row = None

    DEFAULT_CSS = """
        RequestParams {
            width: 100%;
            height: 100%;
        }

        RequestParams DataTable {
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

        #param-controls {
            width: 100%;
            height: 1;
            margin-top: 1;
        }

        #param-controls Input {
            width: 1fr;
            padding: 0 1;
            background: black;
        }

        #param-controls Button {
            width: auto;
            min-width: 5;
            height: 1;
            padding: 0 1;
            margin-left: 1;
            background: black;
            color: white;
        }

        #param-controls Button:hover,
        #param-controls Button:focus,
        #param-controls Button.-active {
            background: black;
            color: white;
            text-style: bold;
        }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="request-params")
        with Horizontal(id="param-controls"):
            yield Input(placeholder="Key", id="param-key", compact=True)
            yield Input(placeholder="Value", id="param-value", compact=True)
            yield Button("Add", id="add-param", compact=True)

    def on_mount(self) -> None:
        table = self.query_one("#request-params", DataTable)
        table.add_columns("Key", "Value")
        table.add_rows(
            [
                ("page", "1"),
                ("limit", "20"),
                ("search", "widgets"),
                ("sort", "created_at"),
                ("order", "desc"),
                ("status", "active"),
                ("fields", "id,name,email"),
                ("include", "profile,settings"),
                ("api_version", "v2"),
                ("format", "json"),
            ]
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "add-param":
            return

        table = self.query_one("#request-params", DataTable)
        key_input = self.query_one("#param-key", Input)
        value_input = self.query_one("#param-value", Input)
        key = key_input.value.strip()
        value = value_input.value.strip()

        if not key:
            return

        if self._editing_row is not None:
            table.update_cell(self._editing_row, table.ordered_columns[0].key, key)
            table.update_cell(self._editing_row, table.ordered_columns[1].key, value)
        else:
            table.add_row(key, value)

        self._reset_edit()
        key_input.value = ""
        value_input.value = ""
        key_input.focus()

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if action == "cancel_edit":
            return self._editing_row is not None
        return True

    def action_edit_param(self) -> None:
        table = self.query_one("#request-params", DataTable)
        if not table.row_count:
            return

        row_key = table.ordered_rows[table.cursor_row].key
        key, value = table.get_row(row_key)
        self._editing_row = row_key

        self.query_one("#param-key", Input).value = str(key)
        self.query_one("#param-value", Input).value = str(value)
        self.query_one("#add-param", Button).label = "Save"
        self.query_one("#param-key", Input).focus()

    def action_cancel_edit(self) -> None:
        self._reset_edit()
        self.query_one("#param-key", Input).value = ""
        self.query_one("#param-value", Input).value = ""

    def action_delete_param(self) -> None:
        table = self.query_one("#request-params", DataTable)
        if table.row_count:
            row_key = table.ordered_rows[table.cursor_row].key
            table.remove_row(row_key)
            if row_key == self._editing_row:
                self.action_cancel_edit()

    def _reset_edit(self) -> None:
        self._editing_row = None
        self.query_one("#add-param", Button).label = "Add"
