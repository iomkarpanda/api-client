from components.sidebar import Sidebar, EndpointItem
from components.request import Request
from components.response import Response
from components.inputbar import InputBar
from textual import work
from textual.containers import Horizontal,Vertical
from textual.theme import Theme
from textual.widgets import Input
from screens.edit_endpoint import EditEndpointScreen
from screens.save_request import SaveRequestScreen
from screens.test import TestScreen
from textual.app import App

from db.endpoints import get_endpoint
from db.requests import get_latest_request, insert_request, update_request
from db.responses import insert_response
from db.tables import create_tables
from services.request import METHODS, response_delay

APP_THEME = Theme(
    name="api-client",
    primary="#4a90e2",
    secondary="#16a085",
    accent="#16a085",
    success="#4ebf71",
    warning="#ffa62b",
    error="#ba3c5b",
    foreground="#e0e0e0",
    background="#000000",
    surface="#000000",
    panel="#000000",
    dark=True,
    variables={
        "border-blurred": "#4a90e2",
        "input-selection-background": "#264f78",
        "block-cursor-background": "#16a085",
        "block-cursor-foreground": "#ffffff",
        "block-cursor-text-style": "bold",
        "block-cursor-blurred-background": "#0e5c4b",
        "block-cursor-blurred-foreground": "#e0e0e0",
        "block-hover-background": "#123a33",
    },
)

class Tui(App):

    BINDINGS = [('ctrl+o','add_screen','Test screen'),
                ('ctrl+s','save_request','Save request'),
                ('f2','edit_endpoint','Edit endpoint'),
                ('escape','close_screen','Close screen')]


    CSS = """
        #app-layout {
            width: 100%;
            height: 100%;
        }

        #input-bar {
            width: 100%;
            height: 3;
            margin-bottom: 1;
        }

        #content {
            width: 100%;
            height: 1fr;
        }

        #panels {
            width: 80%;
            height: 100%;
        }
    """

    def __init__(self) -> None:
        super().__init__()
        self.current_endpoint_id: int | None = None
        self.current_request_id: int | None = None
        self.register_theme(APP_THEME)
        self.theme = "api-client"

    def on_mount(self) -> None:
        create_tables()

    def compose(self):
        yield Vertical(
            InputBar(id="input-bar"),
            Horizontal(
                Sidebar(),
                Vertical(Request(), Response(), id="panels"),
                id="content",
            ),
            id="app-layout",
        )

    def action_add_screen(self):
        self.push_screen(TestScreen())

    def action_save_request(self):
        url = self.query_one("#endpoint", Input).value.strip()
        self.push_screen(SaveRequestScreen(url=url))

    def action_edit_endpoint(self):
        if self.current_endpoint_id is None:
            self.notify("Open an endpoint first, then press F2 to edit it")
            return

        endpoint = get_endpoint(self.current_endpoint_id)
        if endpoint is None:
            return

        self.push_screen(EditEndpointScreen(endpoint[0], endpoint[2], endpoint[3]))

    def action_close_screen(self):
        if len(self.screen_stack) > 1:
            self.pop_screen()

    def on_endpoint_item_selected(self, event: EndpointItem.Selected) -> None:
        event.stop()
        self.load_endpoint_config(event.endpoint_id)

    def load_endpoint_config(self, endpoint_id: int) -> None:
        endpoint = get_endpoint(endpoint_id)
        if endpoint is None:
            return

        latest = get_latest_request(endpoint_id)
        self.current_endpoint_id = endpoint_id
        self.current_request_id = latest[0] if latest else None

        self.query_one(InputBar).set_request(latest[2] if latest else None, endpoint[3])
        self.query_one(Request).load_config(latest)
        self.query_one(Response).load_history(self.current_request_id)
        self.query_one(Sidebar).mark_active(endpoint_id)

    def clear_current_endpoint(self) -> None:
        self.current_endpoint_id = None
        self.current_request_id = None
        self.query_one(InputBar).set_request("get", "")
        self.query_one(Request).load_config(None)
        self.query_one(Response).load_history(None)

    async def send_current_request(self) -> None:
        method, url = self.query_one(InputBar).request_values()
        if not url:
            return

        config = self.query_one(Request).config()
        self._run_request(method, url, config)

    @work(thread=True)
    def _run_request(self, method: str, url: str, config: dict) -> None:
        request_method = METHODS.get(method)
        if request_method is None:
            self.call_from_thread(self._show_send_error, f"Unsupported method: {method}")
            return

        try:
            response = request_method(
                url,
                headers=config["headers"],
                params=config["params"],
                cookies=config["cookies"],
                authorization=config["authorization"],
                body=config["body"],
            )
        except Exception as error:
            self.call_from_thread(self._show_send_error, str(error))
            return

        self.call_from_thread(self._handle_response, method, config, response)

    def _show_send_error(self, message: str) -> None:
        self.query_one(Response).show_error(message)

    def _handle_response(self, method: str, config: dict, response) -> None:
        if self.current_endpoint_id is None:
            self.query_one(Response).show(response, response_delay(response))
            return

        delay = response_delay(response)
        try:
            if self.current_request_id is None:
                self.current_request_id = insert_request(
                    self.current_endpoint_id, method, **config
                )
            else:
                update_request(self.current_request_id, method, **config)

            insert_response(
                self.current_request_id,
                status_code=response.status_code,
                delay=delay,
                headers=dict(response.headers),
                body=response.text,
                cookies=dict(response.cookies),
            )
        except Exception as error:
            self.query_one(Response).show(response, delay)
            self.query_one(Response).show_error(f"could not store response: {error}")
            return

        self.query_one(Response).load_history(self.current_request_id)

if __name__  == "__main__":
    app = Tui()
    app.run()
