from components.sidebar import Sidebar
from components.request import Request
from components.response import Response
from components.inputbar import InputBar
from textual.containers import Horizontal,Vertical
from screens.test import TestScreen
from textual.app import App

class Tui(App):

    BINDINGS = [('ctrl+o','add_screen','Test Screen'),
                ('escape','close_screen','Close Test Screen')]


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
        
    def action_close_screen(self):
        self.pop_screen()

if __name__  == "__main__":
    app = Tui()
    app.run()
