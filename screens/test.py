from textual.widgets import Button, Input, Static
from textual.app import ComposeResult
from textual.screen import Screen
from services.request import make_request, parse_response

class TestScreen(Screen):

    def compose(self) -> ComposeResult:

        yield Input(placeholder="Enter url",id="input-field")
        yield Button("Send")

        yield Static("", id="response", markup=False)


    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#input-field", Input)

        response_widget = self.query_one("#response", Static)

        try:
            response = make_request(input_widget.value)
            response_widget.update(parse_response(response))
        except Exception as error:
            response_widget.update(f"Request failed: {error}")