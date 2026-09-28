from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Collapsible, Static

from db.collections import delete_collection, get_collections
from db.endpoints import get_endpoint, get_endpoints
from screens.confirm import ConfirmScreen


class SidebarHelp(Static):
    """Key binding hints for the sidebar."""

    DEFAULT_CSS = """
        SidebarHelp {
            width: 100%;
            height: 1;
            padding: 0 1;
            background: #4a90e2;
            color: #cde4ff;
        }
    """


class EndpointItem(Static):

    class Selected(Message):
        def __init__(self, endpoint_id: int) -> None:
            super().__init__()
            self.endpoint_id = endpoint_id

    def __init__(self, endpoint_id: int, label: str, **kwargs) -> None:
        super().__init__(label, **kwargs)
        self.endpoint_id = endpoint_id

    def on_click(self) -> None:
        self.post_message(self.Selected(self.endpoint_id))


class Sidebar(Widget):

    BORDER_TITLE = "Collections"

    BINDINGS = [
        ("delete", "delete_collection", "Delete collection"),
    ]

    DEFAULT_CSS = """
        Sidebar {
            width: 20%;
            height: 100%;
            background: black;
            border: round white;
        }

        #collections-list {
            width: 100%;
            height: 1fr;
            overflow-y: auto;
            scrollbar-visibility: hidden;
        }

        Sidebar Collapsible {
            height: auto;
            padding: 1;
            background: black;
        }

        Sidebar Collapsible Static {
            background: black;
        }

        Sidebar EndpointItem {
            padding: 0 1;
        }

        Sidebar EndpointItem:hover {
            background: #16a085;
            color: white;
        }

        Sidebar EndpointItem.-active {
            background: #4a90e2;
            color: white;
            text-style: bold;
        }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Loading collections...", id="collections-loading"),
            id="collections-list",
        )
        yield SidebarHelp("[bold white]F2[/] Edit endpoint", id="sidebar-help")

    async def on_mount(self) -> None:
        await self.refresh_collections()

    async def refresh_collections(self) -> None:
        container = self.query_one("#collections-list", Vertical)
        await container.remove_children()

        try:
            collections = get_collections()
        except Exception as error:
            await container.mount(Static(f"Unable to load collections: {error}"))
            return

        collapsibles = []
        for collection_id, name, _, _ in collections:
            try:
                endpoints = get_endpoints(collection_id)
            except Exception:
                endpoints = []

            if endpoints:
                content = [
                    EndpointItem(endpoint[0], endpoint[2], id=f"endpoint-{endpoint[0]}")
                    for endpoint in endpoints
                ]
            else:
                content = [Static("No requests yet")]

            collapsibles.append(
                Collapsible(
                    *content,
                    title=name,
                    collapsed=True,
                    id=f"collection-{collection_id}",
                )
            )

        if collapsibles:
            await container.mount(*collapsibles)

    def mark_active(self, endpoint_id: int) -> None:
        for item in self.query(EndpointItem):
            item.set_class(item.endpoint_id == endpoint_id, "-active")

    def action_delete_collection(self) -> None:
        collapsible = self._focused_collection()
        if collapsible is None:
            self.notify("Focus a collection first (tab to it), then press delete")
            return

        collection_id = int(collapsible.id.split("-", 1)[1])

        try:
            collections = get_collections()
            endpoints = get_endpoints(collection_id)
        except Exception as error:
            self.notify(f"Could not load collection: {error}", severity="error")
            return

        name = next((n for cid, n, _, _ in collections if cid == collection_id), None)
        if name is None:
            return

        self._confirm_delete(name, len(endpoints))

    @work(exclusive=True)
    async def _confirm_delete(self, name: str, endpoint_count: int) -> None:
        confirmed = await self.app.push_screen_wait(
            ConfirmScreen(
                f"Delete '{name}'? Its {endpoint_count} endpoints and their "
                "stored responses will also be deleted.",
                confirm_label="Delete",
            )
        )
        if not confirmed:
            return

        try:
            delete_collection(name)
        except Exception as error:
            self.notify(f"Could not delete collection: {error}", severity="error")
            return

        app = self.app
        if (
            app.current_endpoint_id is not None
            and get_endpoint(app.current_endpoint_id) is None
        ):
            app.clear_current_endpoint()

        await self.refresh_collections()

        if app.current_endpoint_id is not None:
            self.mark_active(app.current_endpoint_id)

    def _focused_collection(self) -> Collapsible | None:
        widget = self.app.focused
        while widget is not None:
            if isinstance(widget, Collapsible) and widget.id:
                return widget
            widget = widget.parent
        return None
