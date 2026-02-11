import os
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, TabbedContent, TabPane

from cutting_board_drawers_optimizer.state.loading_data_failed_error import LoadingDataFailedError
from cutting_board_drawers_optimizer.state.saving_data_failed_error import SavingDataFailedError
from cutting_board_drawers_optimizer.state.state import State
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.load_dialog import LoadDialog
from cutting_board_drawers_optimizer.ui.save_dialog import SaveDialog


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

    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+s", "save_config", "Save Config"),
        ("ctrl+o", "load_config", "Open Config"),
        ("c", 'show_tab("cutting_boards")', "Cutting Boards"),
        ("d", 'show_tab("drawers")', "Drawers"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._state = State()
        self._last_path: str | None = None

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

    def action_save_config(self) -> None:
        def _after(result: str | None) -> None:
            if not result:
                return
            try:
                # Sync UI data to state before saving
                cb_manager = self.query_one(CuttingBoardManager)
                dr_manager = self.query_one(DrawerManager)
                self._state.set_data(
                    drawers=dr_manager.get_current_data(), cutting_boards=cb_manager.get_current_data()
                )

                if os.path.exists(result):
                    os.remove(result)

                self._state.save(result)
                self._last_path = result
                # Feedback in log; tests don't assert it
                self.log(f"Config saved to {result}")
            except (OSError, SavingDataFailedError) as e:
                self.log(f"Save failed: {e}")

        self.push_screen(SaveDialog(self._last_path), _after)

    def action_load_config(self) -> None:
        def _after(result: str | None) -> None:
            if not result:
                return
            try:
                self._state.load(result)
                self._last_path = result
                self.log(f"Config loaded from {result}")

                # After loading, update the UI with the new state
                cb_manager = self.query_one(CuttingBoardManager)
                dr_manager = self.query_one(DrawerManager)
                cb_manager.update_from_data(self._state.get_cutting_boards())
                dr_manager.update_from_data(self._state.get_drawers())
            except (FileNotFoundError, LoadingDataFailedError) as e:
                self.log(f"Load failed: {e}")

        start_dir = os.path.dirname(self._last_path) if self._last_path else None
        self.push_screen(LoadDialog(start_dir), _after)

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Focus the manager widget when a tab is activated."""
        if event.tabbed_content.id == "tabs":
            if event.tab.id == "cutting_boards":
                manager = self.query_one(CuttingBoardManager)
                manager.focus()
            elif event.tab.id == "drawers":
                dr_manager = self.query_one(DrawerManager)
                dr_manager.focus()
