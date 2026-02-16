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
    """Textual TUI app to optimize drawer space for cutting boards."""

    # App styling

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

    # App wide keybinds
    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+s", "save_config", "Save Config"),
        ("ctrl+o", "load_config", "Open Config"),
        ("c", 'show_tab("cutting_boards")', "Cutting Boards"),
        ("d", 'show_tab("drawers")', "Drawers"),
    ]

    # Initialize application state
    def __init__(self) -> None:
        super().__init__()
        self._state = State()
        self._last_path: str | None = None

    def compose(self) -> ComposeResult:
        """
        Application widget composition. (UI Composition)
        Is a generator function that yields widgets.
        """
        self.title = "Cutting Board Drawers Optimizer"

        yield Header(show_clock=True, icon="🔪")

        with TabbedContent(id="tabs"):
            with TabPane("Cutting Boards", id="cutting_boards"):
                yield CuttingBoardManager()
            with TabPane("Drawers", id="drawers"):
                yield DrawerManager()

        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        """Switch to a specific tab via a keyboard shortcut."""
        self.query_one("#tabs", TabbedContent).active = tab

    def action_save_config(self) -> None:
        """Save the current state to a file."""

        def _after(result: str | None) -> None:
            """
            Callback for when the user presses OK in the SaveDialog
            essentially our "Save" action
            """
            if not result:
                return

            try:
                # Sync UI data to state before saving
                cb_manager = self.query_one(CuttingBoardManager)
                dr_manager = self.query_one(DrawerManager)

                # Update state with current UI data
                self._state.set_data(
                    drawers=dr_manager.get_current_data(), cutting_boards=cb_manager.get_current_data()
                )

                # Remove the file if it already exists
                if os.path.exists(result):
                    os.remove(result)

                # Save the state to disk
                self._state.save(result)

                # Update the last path used
                self._last_path = result

                # Write to the application log
                self.log(f"Config saved to {result}")

            except (OSError, SavingDataFailedError) as e:
                # If an error occurs, write a message to the log
                self.log(f"Save failed: {e}")

        # Show the SaveDialog
        self.push_screen(SaveDialog(self._last_path), _after)

    def action_load_config(self) -> None:
        """Load the current state to a file."""

        def _after(result: str | None) -> None:
            """
            Callback for when the user presses OK in the LoadDialog
            essentially our "Load" action
            """
            if not result:
                return

            try:
                # Load data from the disk into the state
                self._state.load(result)
                self._last_path = result

                # Write to the application log
                self.log(f"Config loaded from {result}")

                # Get the UI components
                cb_manager = self.query_one(CuttingBoardManager)
                dr_manager = self.query_one(DrawerManager)

                # Update the UI components with the loaded data
                cb_manager.update_from_data(self._state.get_cutting_boards())
                dr_manager.update_from_data(self._state.get_drawers())

            except (FileNotFoundError, LoadingDataFailedError) as e:
                # If an error occurs, write a message to the log
                self.log(f"Load failed: {e}")

        # Set the start directory for the LoadDialog if we have a last path set
        start_dir = os.path.dirname(self._last_path) if self._last_path else None
        # Show the LoadDialog
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
