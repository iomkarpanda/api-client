from textual.widget import Widget
from textual.widgets import Static, TabbedContent, TabPane


class TabHelp(Static):
    """Key binding hints for the active tab."""

    DEFAULT_CSS = """
        TabHelp {
            width: 1fr;
            height: 1;
            margin-left: 2;
            padding: 0 1;
            background: #4a90e2;
            color: #cde4ff;
        }
    """


class HelpTabbedContent(TabbedContent):
    """TabbedContent that shows the active tab's key bindings after the tabs."""

    async def on_mount(self) -> None:
        await self.query_one("#tabs-list").mount(TabHelp())
        self._show_bindings(self.active_pane)

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        self._show_bindings(event.pane)

    def _show_bindings(self, pane: TabPane | None) -> None:
        help_widget = next(iter(self.query(TabHelp)), None)
        if help_widget is None:
            return
        text = self._bindings_text(pane)
        help_widget.display = bool(text)
        help_widget.update(text)

    def _bindings_text(self, pane: TabPane | None) -> str:
        if pane is None:
            return ""

        hints = []
        for child in pane.children:
            if not isinstance(child, Widget):
                continue
            for binding in child.BINDINGS:
                if isinstance(binding, tuple):
                    key = binding[0]
                    description = binding[2] if len(binding) > 2 else binding[1]
                    show = binding[3] if len(binding) > 3 else True
                else:
                    key = binding.key
                    description = binding.description
                    show = binding.show
                if show and description:
                    hints.append(f"[bold white]{key}[/] {description}")

        return "  ".join(hints)
