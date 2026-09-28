from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input


class KeyValueEditor(Widget):
    """Editable key/value table (params, headers, cookies, authorization)."""

    BINDINGS = [
        ("delete", "delete_row", "Delete"),
        ("e", "edit_row", "Edit"),
        ("escape", "cancel_edit", "Cancel edit"),
    ]

    _editing_row = None

    DEFAULT_CSS = """
        KeyValueEditor {
            width: 100%;
            height: 100%;
        }

        KeyValueEditor DataTable {
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

        KeyValueEditor Horizontal {
            width: 100%;
            height: 1;
            margin-top: 1;
        }

        KeyValueEditor Horizontal Input {
            width: 1fr;
            padding: 0 1;
            background: black;
        }

        KeyValueEditor Horizontal Button {
            width: auto;
            min-width: 5;
            height: 1;
            padding: 0 1;
            margin-left: 1;
            background: black;
            color: white;
        }

        KeyValueEditor Horizontal Button:hover,
        KeyValueEditor Horizontal Button:focus,
        KeyValueEditor Horizontal Button.-active {
            background: black;
            color: white;
            text-style: bold;
        }
    """

    def __init__(self, prefix: str) -> None:
        super().__init__()
        self.prefix = prefix

    def compose(self) -> ComposeResult:
        yield DataTable(id=self.prefix)
        with Horizontal(id=f"{self.prefix}-controls"):
            yield Input(placeholder="Key", id=f"{self.prefix}-key", compact=True)
            yield Input(placeholder="Value", id=f"{self.prefix}-value", compact=True)
            yield Button("Add", id=f"{self.prefix}-add", compact=True)

    def on_mount(self) -> None:
        self.query_one(f"#{self.prefix}", DataTable).add_columns("Key", "Value")

    def load(self, values: dict | None) -> None:
        table = self.query_one(f"#{self.prefix}", DataTable)
        table.clear()
        for key, value in (values or {}).items():
            table.add_row(str(key), str(value))

    def values(self) -> dict:
        table = self.query_one(f"#{self.prefix}", DataTable)
        return {
            str(key): str(value)
            for key, value in (table.get_row(row.key) for row in table.ordered_rows)
        }

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != f"{self.prefix}-add":
            return

        table = self.query_one(f"#{self.prefix}", DataTable)
        key_input = self.query_one(f"#{self.prefix}-key", Input)
        value_input = self.query_one(f"#{self.prefix}-value", Input)
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

    def action_edit_row(self) -> None:
        table = self.query_one(f"#{self.prefix}", DataTable)
        if not table.row_count:
            return

        row_key = table.ordered_rows[table.cursor_row].key
        key, value = table.get_row(row_key)
        self._editing_row = row_key

        self.query_one(f"#{self.prefix}-key", Input).value = str(key)
        self.query_one(f"#{self.prefix}-value", Input).value = str(value)
        self.query_one(f"#{self.prefix}-add", Button).label = "Save"
        self.query_one(f"#{self.prefix}-key", Input).focus()

    def action_cancel_edit(self) -> None:
        self._reset_edit()
        self.query_one(f"#{self.prefix}-key", Input).value = ""
        self.query_one(f"#{self.prefix}-value", Input).value = ""

    def action_delete_row(self) -> None:
        table = self.query_one(f"#{self.prefix}", DataTable)
        if table.row_count:
            row_key = table.ordered_rows[table.cursor_row].key
            table.remove_row(row_key)
            if row_key == self._editing_row:
                self.action_cancel_edit()

    def _reset_edit(self) -> None:
        self._editing_row = None
        self.query_one(f"#{self.prefix}-add", Button).label = "Add"
