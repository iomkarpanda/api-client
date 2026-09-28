from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class ConfirmScreen(ModalScreen[bool]):

    BINDINGS = [("escape", "cancel", "Cancel")]

    CSS = """
        ConfirmScreen {
            align: center middle;
            background: black;
        }

        #confirm-box {
            width: 60;
            height: auto;
            padding: 1 2;
            border: round white;
            background: black;
        }

        #confirm-message {
            height: auto;
            margin-bottom: 1;
        }

        #confirm-buttons {
            width: 100%;
            height: auto;
        }

        #confirm-buttons Button {
            width: 1fr;
            height: 3;
            min-width: 0;
            border: none;
            background: black;
        }

        #confirm-buttons Button:hover,
        #confirm-buttons Button:focus,
        #confirm-buttons Button.-active {
            border: none;
            background: black;
            color: white;
            text-style: bold;
        }
    """

    def __init__(self, message: str, confirm_label: str = "Confirm") -> None:
        super().__init__()
        self.message = message
        self.confirm_label = confirm_label

    def compose(self) -> ComposeResult:
        box = Vertical(
            Static(self.message, id="confirm-message", markup=False),
            Horizontal(
                Button(self.confirm_label, id="confirm-yes"),
                Button("Cancel", id="confirm-no"),
                id="confirm-buttons",
            ),
            id="confirm-box",
        )
        box.border_title = "Confirm"
        yield box

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm-yes")

    def action_cancel(self) -> None:
        self.dismiss(False)
