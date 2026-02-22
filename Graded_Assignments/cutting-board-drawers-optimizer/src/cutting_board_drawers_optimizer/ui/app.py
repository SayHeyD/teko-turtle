import contextlib
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
from cutting_board_drawers_optimizer.ui.optimize_manager import OptimizeManager
from cutting_board_drawers_optimizer.ui.save_dialog import SaveDialog


class CuttingBoardDrawersOptimizerApp(App):
    """
    Main Application class for the Cutting Board Drawers Optimizer.
    Handles the top-level layout, navigation between tabs, and the orchestration
    of saving and loading configurations.
    """

    # App styling using Textual's CSS-like syntax
    CSS = """
    /* General button spacing */
    Button {
        margin: 1 2;
    }

    /* Make the top-level tabs fill the available space between Header and Footer */
    #tabs {
        height: 1fr;
    }

    /* Ensure each TabPane inside the top-level tabs expands to fill its parent */
    #tabs TabPane {
        height: 1fr;
    }

    /* Make manager widgets fill their parent tab completely */
    CuttingBoardManager, DrawerManager, OptimizeManager {
        height: 1fr;
    }

    /* Tree styling in the Optimize tab: green border and full height */
    #opt_result_tree {
        height: 1fr;
        border: solid green;
    }

    /* Inside each manager, make their inner TabbedContent and tables fill space */
    CuttingBoardManager TabbedContent, DrawerManager TabbedContent {
        height: 1fr;
    }

    /* Make DataTable fill the full screen width and height */
    DataTable {
        height: 1fr;
    }

    /* Error message styling: red, bold, with margins */
    .error {
        color: red;
        margin: 0 2;
        text-style: bold;
    }
    """

    # Global keyboard shortcuts available throughout the application
    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+s", "save_config", "Save Config"),
        ("ctrl+o", "load_config", "Open Config"),
        ("c", 'show_tab("cutting_boards")', "Cutting Boards"),
        ("d", 'show_tab("drawers")', "Drawers"),
        ("o", 'show_tab("optimize")', "Optimize"),
    ]

    def __init__(self) -> None:
        """Initialize the application state and track the last used file path."""
        super().__init__()
        self._state = State()
        self._last_path: str | None = None

    def compose(self) -> ComposeResult:
        """
        Builds the UI by yielding widgets in order.
        Textual calls this during the application startup phase.
        """
        self.title = "Cutting Board Drawers Optimizer"

        yield Header(show_clock=True, icon="🔪")

        # Create the top-level navigation tabs
        with TabbedContent(id="tabs"):
            with TabPane("Cutting Boards", id="cutting_boards"):
                yield CuttingBoardManager()
            with TabPane("Drawers", id="drawers"):
                yield DrawerManager()
            with TabPane("Optimize", id="optimize"):
                yield OptimizeManager()

        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        """Action handler for switching tabs via keyboard shortcuts (c, d, o)."""
        self.query_one("#tabs", TabbedContent).active = tab

    def action_save_config(self) -> None:
        """
        Action handler for 'Save Config' (Ctrl+S).
        Opens a SaveDialog and performs the save if the user confirms.
        """

        # Define the callback executed after the SaveDialog is closed
        # Since we define the callback inside the "action_save_config" method,
        # it is only available within the scope of this method
        def _after(result: str | None) -> None:
            """Callback executed after the SaveDialog is closed."""
            if not result:
                return

            try:
                # 1. Collect current data from all UI managers
                cb_manager = self.query_one(CuttingBoardManager)
                dr_manager = self.query_one(DrawerManager)
                opt_manager = self.query_one(OptimizeManager)

                # 2. Extract budget and amount from the Optimize tab
                budget_str, amount_str = opt_manager.get_current_data()

                budget_cents = None
                if budget_str:
                    # Context lib suppresses ValueError if the input is not a number
                    # (e.g., if the user enters a non-numeric string)
                    # We suppress the error here because we want to allow empty strings
                    with contextlib.suppress(ValueError):
                        budget_cents = int(float(budget_str) * 100)

                amount = None
                if amount_str:
                    # We suppress the error here because we want to allow empty strings
                    with contextlib.suppress(ValueError):
                        amount = int(amount_str)

                # 3. Synchronize UI data into the internal state object
                # This is required because the state object is not updated automatically
                self._state.set_data(
                    drawers=dr_manager.get_current_data(),
                    cutting_boards=cb_manager.get_current_data(),
                    budget_cents=budget_cents,
                    cutting_board_amount=amount,
                )

                # 4. Remove the existing file (State.save enforces new file creation)
                # Remove the existing file if it exists
                if os.path.exists(result):
                    os.remove(result)

                # 5. Persist state to disk
                # Save the state object to a file on the disk
                self._state.save(result)
                self._last_path = result
                self.log(f"Config saved to {result}")

            # Catch any errors and display them in the UI
            except (OSError, SavingDataFailedError) as e:
                self.log(f"Save failed: {e}")

        # Push the SaveDialog screen onto the stack
        self.push_screen(SaveDialog(self._last_path), _after)

    def action_load_config(self) -> None:
        """
        Action handler for 'Open Config' (Ctrl+O).
        Opens a LoadDialog and populates the UI if a file is selected.
        """

        # Define the callback executed after the SaveDialog is closed
        # Since we define the callback inside the "action_load_config" method,
        # it is only available within the scope of this method
        def _after(result: str | None) -> None:
            """Callback executed after the LoadDialog is closed."""
            if not result:
                return

            try:
                # 1. Load data from the disk into the state object
                self._state.load(result)
                self._last_path = result
                self.log(f"Config loaded from {result}")

                # 2. Update UI managers with the loaded data
                # This is required because the state object is not updated automatically
                cb_manager = self.query_one(CuttingBoardManager)
                dr_manager = self.query_one(DrawerManager)
                opt_manager = self.query_one(OptimizeManager)

                cb_manager.update_from_data(self._state.get_cutting_boards())
                dr_manager.update_from_data(self._state.get_drawers())
                opt_manager.update_from_data(self._state.get_budget_cents(), self._state.get_cutting_board_amount())

            # Catch errors and display them in the UI
            except (FileNotFoundError, LoadingDataFailedError) as e:
                self.log(f"Load failed: {e}")

        # Determine the starting directory for the file browser,
        # By default, it is the directory of the last loaded file, if any
        # Otherwise it is the current working directory
        start_dir = os.path.dirname(self._last_path) if self._last_path else None
        # Push the LoadDialog screen onto the stack
        self.push_screen(LoadDialog(start_dir), _after)

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """
        Event handler triggered when a top-level tab is activated.
        Ensures the manager widget in the active tab receives focus.
        """
        if event.tabbed_content.id == "tabs":
            if event.tab.id == "cutting_boards":
                self.query_one(CuttingBoardManager).focus()
            elif event.tab.id == "drawers":
                self.query_one(DrawerManager).focus()
            elif event.tab.id == "optimize":
                self.query_one(OptimizeManager).focus()
