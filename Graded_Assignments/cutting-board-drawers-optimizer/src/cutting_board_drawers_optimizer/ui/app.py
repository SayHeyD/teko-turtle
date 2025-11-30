from textual.app import App, ComposeResult
from textual.widgets import Header, TabbedContent, TabPane, Footer
from .cutting_board_manager import CuttingBoardManager
from .drawer_manager import DrawerManager


class CuttingBoardDrawersOptimizerApp(App):
    """An app to optimize drawer space for cutting boards."""

    CSS = """
    Button {
        margin: 1 2;
    }
    """

    BINDINGS = [
        ('c', 'show_tab("cutting_boards")', 'Cutting Boards'),
        ('d', 'show_tab("drawers")', 'Drawers'),
    ]

    def compose(self) -> ComposeResult:
        """Application widget composition."""
        self.title = "Cutting Board Drawers Optimizer"

        yield Header(
            show_clock=True,
            icon='🔪'
        )

        with TabbedContent(id='tabs'):
            with TabPane('Cutting Boards', id='cutting_boards'):
                yield CuttingBoardManager()
            with TabPane('Drawers', id='drawers'):
                yield DrawerManager()

        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        """Switch to specific tab via keyboard shortcut."""
        self.query_one('#tabs', TabbedContent).active = tab
