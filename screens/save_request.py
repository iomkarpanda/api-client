from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Select, Static

from components.sidebar import Sidebar
from db.collections import get_collections, insert_collection
from db.endpoints import insert_endpoint


class SaveRequestScreen(Screen):
    CSS = """
        SaveRequestScreen {
            align: center middle;
            background: black;
        }

        #save-request-form {
            width: 60;
            height: auto;
            padding: 1 2;
            border: round white;
            background: black;
        }

        #save-request-form Select {
            width: 100%;
            margin-bottom: 1;
            background: black;
        }

        #save-request-form SelectCurrent {
            border: tall white;
            background: black;
        }

        #save-request-form Input {
            border: tall white;
            background: black;
            margin-bottom: 1;
        }

        #save-request-form Button {
            width: 1fr;
            height: 3;
            border: none;
            background: black;
        }

        #save-request-form Button:hover,
        #save-request-form Button:focus,
        #save-request-form Button.-active {
            border: none;
            background: black;
            color: white;
            text-style: bold;
        }

        #save-status {
            height: auto;
            margin-top: 1;
        }
    """

    def __init__(self, url: str = "") -> None:
        super().__init__()
        self.url = url

    def compose(self) -> ComposeResult:
        form = Vertical(
            Select([], prompt="Save in collection", id="collection-select"),
            Input(placeholder="New collection name (optional)", id="new-collection-name"),
            Input(placeholder="Endpoint name", id="endpoint-name"),
            Input(placeholder="URL", id="endpoint-url", value=self.url),
            Button("Save", id="save-request"),
            Static("", id="save-status"),
            id="save-request-form",
        )
        form.border_title = "Save Request"
        yield form

    def on_mount(self) -> None:
        select = self.query_one("#collection-select", Select)
        status = self.query_one("#save-status", Static)

        try:
            collections = get_collections()
        except Exception as error:
            status.update(f"Could not load collections: {error}")
            return

        if collections:
            select.set_options(
                [(name, collection_id) for collection_id, name, _, _ in collections]
            )
        else:
            status.update("No collections yet. Enter a new collection name.")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "save-request":
            return

        status = self.query_one("#save-status", Static)
        select = self.query_one("#collection-select", Select)
        new_collection = self.query_one("#new-collection-name", Input).value.strip()
        endpoint_name = self.query_one("#endpoint-name", Input).value.strip()
        url = self.query_one("#endpoint-url", Input).value.strip()

        collection_id = None if select.value is Select.BLANK else select.value
        saving_endpoint = bool(endpoint_name or url)

        if saving_endpoint:
            if not endpoint_name:
                status.update("Enter an endpoint name.")
                return
            if not url:
                status.update("Enter a URL.")
                return
            if collection_id is None and not new_collection:
                status.update("Pick a collection or enter a new name.")
                return
        elif not new_collection:
            status.update("Enter an endpoint name.")
            return

        if new_collection:
            try:
                collections = get_collections()
                collection_id = next(
                    (cid for cid, name, _, _ in collections if name == new_collection),
                    None,
                )
                if collection_id is None:
                    insert_collection(new_collection)
                    collections = get_collections()
                    collection_id = next(
                        cid for cid, name, _, _ in collections if name == new_collection
                    )
            except Exception as error:
                status.update(f"Could not create collection: {error}")
                return

        if saving_endpoint:
            try:
                insert_endpoint(collection_id, endpoint_name, url)
            except Exception as error:
                status.update(f"Could not save endpoint: {error}")
                return

        await self.app.query_one(Sidebar).refresh_collections()
        self.app.pop_screen()
