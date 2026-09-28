from textual.widgets import Select,Input,Button
from textual.widget import Widget
from textual.containers import Horizontal

from screens.save_request import SaveRequestScreen

class InputBar(Widget):

    METHODS = {"get", "post", "put", "delete", "patch", "options"}

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
            max-height: 3;
            background: black;
        }

        #endpoint {
            width: 65%;
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
            ('GET','get'),
            ('POST','post'),
            ('PUT','put'),
            ('DELETE','delete'),
            ('PATCH','patch'),
            ('OPTIONS','options')
        ), id="method")
        inp = Input(placeholder="Enter endpoint", id="endpoint")
        yield Horizontal(select, inp, Button('Send', id="send"), Button('Save', id="save"))

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
