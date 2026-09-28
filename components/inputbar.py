from rich.text import Text
from textual.widgets import Select,Input,Button
from textual.widget import Widget
from textual.containers import Horizontal

from screens.save_request import SaveRequestScreen

class InputBar(Widget):

    METHODS = {"get", "post", "put", "delete", "patch", "options"}

    METHOD_COLORS = {
        "GET": "#00ff00",
        "POST": "#ffff00",
        "PUT": "#5555ff",
        "PATCH": "#ff55ff",
        "DELETE": "#ff5555",
        "OPTIONS": "#55ffff",
    }

    DEFAULT_CSS = """

        InputBar{
            width: 100%;
        }

        Horizontal {
            width: 100%;
            height: 3;
        }

        #method {
            width: 15% !important;
            min-width: 0;
            height: 3;
            margin-right: 1;
            background: black;
        }

        #method SelectCurrent {
            border: tall white;
            background: black;
        }

        #endpoint {
            width: 63%;
            min-width: 0;
            border: tall white;
            background: black;
        }

        #send,
        #save {
            width: 10%;
            min-width: 0;
            border: none;
            height: 3;
            background: black;
        }

        #send:hover,
        #save:hover,
        #send:focus,
        #save:focus,
        #send.-active,
        #save.-active {
            border: none;
            background: black;
            color: white;
            text-style: bold;
        }


    """

    def compose(self):

        select = Select((
            (self._method_prompt("GET"), "get"),
            (self._method_prompt("POST"), "post"),
            (self._method_prompt("PUT"), "put"),
            (self._method_prompt("DELETE"), "delete"),
            (self._method_prompt("PATCH"), "patch"),
            (self._method_prompt("OPTIONS"), "options"),
        ), allow_blank=False, id="method")
        inp = Input(placeholder="Enter endpoint", id="endpoint")
        yield Horizontal(select, inp, Button('Send', id="send"), Button('Save', id="save"))

    def _method_prompt(self, method: str) -> Text:
        return Text(method, style=f"bold {self.METHOD_COLORS[method]}")

    def set_request(self, method: str | None, url: str) -> None:
        select = self.query_one("#method", Select)
        select.value = method if method in self.METHODS else "get"
        self.query_one("#endpoint", Input).value = url

    def request_values(self) -> tuple[str, str]:
        method = self.query_one("#method", Select).value
        if method is Select.BLANK:
            method = "get"
        url = self.query_one("#endpoint", Input).value.strip()
        return str(method).lower(), url

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            url = self.query_one("#endpoint", Input).value.strip()
            self.app.push_screen(SaveRequestScreen(url=url))
        elif event.button.id == "send":
            await self.app.send_current_request()
