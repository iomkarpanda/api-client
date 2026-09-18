from textual.screen import Screen
from components.inputbar import InputBar
class TestScreen(Screen):

    def compose(self):
        yield InputBar()