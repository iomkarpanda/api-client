from textual.widgets import Button, Input, Static
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from services.request import make_request, parse_response

class TestScreen(Screen):

    CSS = """
        TestScreen {
            align: center middle;
            background: black;
        }

        #test-form {
            width: 80;
            height: 80%;
            padding: 1 2;
            border: round white;
            background: black;
        }

        #test-form Input {
            border: tall white;
            background: black;
            margin-bottom: 1;
        }

        #test-form Button {
            width: 1fr;
            height: 3;
            border: none;
            background: black;
        }

        #test-form Button:hover,
        #test-form Button:focus,
        #test-form Button.-active {
            border: none;
            background: black;
            color: white;
            text-style: bold;
        }

        #response {
            height: 1fr;
            margin-top: 1;
            padding: 0 1;
            border: round white;
            overflow-y: auto;
        }
    """

    def compose(self) -> ComposeResult:
        form = Vertical(
            Input(placeholder="Enter URL", id="input-field"),
            Button("Send"),
            Static("", id="response", markup=False),
            id="test-form",
        )
        form.border_title = "Test screen"
        yield form

    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#input-field", Input)

        response_widget = self.query_one("#response", Static)

        try:
            response = make_request(input_widget.value)
            response_widget.update(parse_response(response))
        except Exception as error:
            response_widget.update(f"Request failed: {error}")
