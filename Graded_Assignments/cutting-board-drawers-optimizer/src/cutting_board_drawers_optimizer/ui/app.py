from typing import ClassVar

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager


class CuttingBoardDrawersOptimizerApp(App):
    """An app to optimize drawer space for cutting boards."""

    CSS = """
    /* General button spacing */
    Button {
        margin: 1 2;
    }

    /* Make the top-level tabs fill the available space between Header and Footer */
    #tabs {
        height: 1fr;
    }

    /* Ensure each TabPane inside the top-level tabs expands */
    #tabs TabPane {
        height: 1fr;
    }

    /* Make manager widgets fill their parent tab */
    CuttingBoardManager, DrawerManager {
        height: 1fr;
    }

    /* Inside each manager, make their inner TabbedContent and tables fill space */
    CuttingBoardManager TabbedContent, DrawerManager TabbedContent {
        height: 1fr;
    }

    /* Make DataTable fill the full screen */
    DataTable {
        height: 1fr;
    }
    """

    BINDINGS: ClassVar[list[tuple[str, str, str]]] = [
        ("c", 'show_tab("cutting_boards")', "Cutting Boards"),
        ("d", 'show_tab("drawers")', "Drawers"),
    ]

    def compose(self) -> ComposeResult:
        """Application widget composition."""
        self.title = "Cutting Board Drawers Optimizer"

        yield Header(show_clock=True, icon="🔪")

        with TabbedContent(id="tabs"):
            with TabPane("Cutting Boards", id="cutting_boards"):
                yield CuttingBoardManager()
            with TabPane("Drawers", id="drawers"):
                yield DrawerManager()

        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        """Switch to specific tab via keyboard shortcut."""
        self.query_one("#tabs", TabbedContent).active = tab

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Focus the manager widget when a tab is activated."""
        if event.tabbed_content.id == "tabs":
            if event.tab.id == "cutting_boards":
                manager = self.query_one(CuttingBoardManager)
                manager.focus()
            elif event.tab.id == "drawers":
                manager = self.query_one(DrawerManager)
                manager.focus()
