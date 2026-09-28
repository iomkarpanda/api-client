from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Static

from components.sidebar import Sidebar
from db.endpoints import update_endpoint


class EditEndpointScreen(Screen):
    CSS = """
        EditEndpointScreen {
            align: center middle;
            background: black;
        }

        #edit-endpoint-form {
            width: 60;
            height: auto;
            padding: 1 2;
            border: round white;
            background: black;
        }

        #edit-endpoint-form Input {
            border: tall white;
            background: black;
            margin-bottom: 1;
        }

        #edit-endpoint-form Button {
            width: 100%;
            border: none;
            background: black;
        }

        #edit-endpoint-form Button:hover,
        #edit-endpoint-form Button:focus,
        #edit-endpoint-form Button.-active {
            border: none;
            background: black;
            color: white;
            text-style: bold;
        }

        #edit-status {
            height: auto;
            margin-top: 1;
        }
    """

    def __init__(self, endpoint_id: int, name: str, url: str) -> None:
        super().__init__()
        self.endpoint_id = endpoint_id
        self.endpoint_name = name
        self.endpoint_url = url

    def compose(self) -> ComposeResult:
        form = Vertical(
            Input(value=self.endpoint_name, placeholder="Endpoint name", id="endpoint-name"),
            Input(value=self.endpoint_url, placeholder="URL", id="endpoint-url"),
            Button("Save", id="save-endpoint"),
            Static("", id="edit-status"),
            id="edit-endpoint-form",
        )
        form.border_title = "Edit Endpoint"
        yield form

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "save-endpoint":
            return

        status = self.query_one("#edit-status", Static)
        name = self.query_one("#endpoint-name", Input).value.strip()
        url = self.query_one("#endpoint-url", Input).value.strip()

        if not name:
            status.update("Enter an endpoint name.")
            return

        if not url:
            status.update("Enter a URL.")
            return

        try:
            update_endpoint(self.endpoint_id, name, url)
        except Exception as error:
            status.update(f"Could not update endpoint: {error}")
            return

        await self.app.query_one(Sidebar).refresh_collections()
        self.app.load_endpoint_config(self.endpoint_id)
        self.app.pop_screen()
