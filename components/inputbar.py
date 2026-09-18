from textual.widgets import Select,Input,Button
from textual.widget import Widget
from textual.containers import Horizontal

class InputBar(Widget):

    DEFAULT_CSS = """

        InputBar{
            width: 100%;
        }

        Horizontal {
            width: 100%;
            height: 3;
        }

        #method {
            width: 20% !important;
            min-width: 0;
            max-height: 3;
            background: black;
        }

        #endpoint {
            width: 70%;
            min-width: 0;
            border: tall white;
            background: black;
        }

        #send {
            width: 10%;
            min-width: 0;
            border: none;
            height: 3;
            background: black;
        }

        #send:hover,
        #send:focus,
        #send.-active {
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
        yield Horizontal(select, inp, Button('Send', id="send"))



    
