from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import (
    Input,
    TabbedContent,
    TabPane,
)

from cutting_board_drawers_optimizer.optimizer import CuttingBoard
from cutting_board_drawers_optimizer.ui.create_cutting_board import CreateCuttingBoard
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable


class CuttingBoardManager(Widget):
    """
    Manager widget for Cutting Boards.

    Provides two tabs:
    - A table view populated from ROWS
    - A form to add new cutting boards
    """

    ROWS: ClassVar[list[tuple[str, str, str, str, str]]] = [
        ("Name", "Length", "Width", "Weight", "Price"),
        ("Large Oak", "40", "30", "2000", "50.39"),
        ("Medium Beech", "30", "20", "1500", "35.50"),
        ("Small Plastic", "20", "15", "500", "12.00"),
    ]

    # Keybinds specific to the Cutting Board Manager
    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+n", "switch_to_create_tab", "Create"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the CuttingBoardManager UI."""
        with TabbedContent(id="cb_tabs"):
            with TabPane("Table", id="table_tab"):
                yield CuttingBoardTable(id="cutting_board_table")
            with TabPane("Create", id="create_tab"):
                yield CreateCuttingBoard()

    def on_mount(self) -> None:
        """Populate the table after mounting."""
        table = self.query_one(CuttingBoardTable)
        table.populate(self.ROWS)

    def on_create_cutting_board_created(self, message: CreateCuttingBoard.Created) -> None:
        """Handle the creation of a new cutting board."""
        table = self.query_one(CuttingBoardTable)
        table.add_row(message.name, message.length, message.width, message.weight, message.price)
        self.action_switch_to_table()

    def action_switch_to_table(self) -> None:
        tabs = self.query_one("#cb_tabs", TabbedContent)
        tabs.active = "table_tab"
        self.query_one(CuttingBoardTable).focus()

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Handle tab activation within CuttingBoardManager."""
        if event.tabbed_content.id == "cb_tabs":
            if event.tab.id == "table_tab":
                self.query_one(CuttingBoardTable).focus()
            elif event.tab.id == "create_tab":
                self.query_one("#cb_name", Input).focus()

    def action_switch_to_create_tab(self) -> None:
        """Switch to the create tab when ctrl+n is pressed."""
        tabbed_content = self.query_one("#cb_tabs", TabbedContent)
        tabbed_content.active = "create_tab"

    def get_current_data(self) -> list[CuttingBoard]:
        """Extract CuttingBoard objects from the DataTable."""
        table = self.query_one(CuttingBoardTable)
        return table.get_current_data()

    def update_from_data(self, cutting_boards: list[CuttingBoard]) -> None:
        """Update the DataTable with the provided CuttingBoard objects."""
        table = self.query_one(CuttingBoardTable)
        table.update_from_data(cutting_boards)
