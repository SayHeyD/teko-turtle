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
from cutting_board_drawers_optimizer.ui.edit_cutting_board import EditCuttingBoard


class CuttingBoardManager(Widget):
    """
    Manager widget for Cutting Boards.

    Provides three tabs:
    - A table view populated from ROWS
    - A form to add new cutting boards
    - A form to edit existing cutting boards
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
            with TabPane("Edit", id="edit_tab"):
                yield EditCuttingBoard()

    def on_mount(self) -> None:
        """Populate the table after mounting."""
        table = self.query_one(CuttingBoardTable)
        table.populate(self.ROWS)
        self.query_one("#cb_tabs", TabbedContent).hide_tab("edit_tab")

    def on_create_cutting_board_created(self, message: CreateCuttingBoard.Created) -> None:
        """Handle the creation of a new cutting board."""
        table = self.query_one(CuttingBoardTable)
        table.add_row(message.name, message.length, message.width, message.weight, message.price)
        self.action_switch_to_table()

    def on_cutting_board_table_edit_requested(self, message: CuttingBoardTable.EditRequested) -> None:
        """Handle the edit request from the table."""
        edit_form = self.query_one(EditCuttingBoard)
        edit_form.set_values(message.name, message.length, message.width, message.weight, message.price)

        tabbed_content = self.query_one("#cb_tabs", TabbedContent)
        tabbed_content.show_tab("edit_tab")
        tabbed_content.active = "edit_tab"

    def on_edit_cutting_board_saved(self, message: EditCuttingBoard.Saved) -> None:
        """Handle the saving of an edited cutting board."""
        table = self.query_one(CuttingBoardTable)
        if table.cursor_row is not None:
            column_keys = [col.key for col in table.columns.values()]
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            table.update_cell(row_key, column_keys[0], message.name)
            table.update_cell(row_key, column_keys[1], message.length)
            table.update_cell(row_key, column_keys[2], message.width)
            table.update_cell(row_key, column_keys[3], message.weight)
            table.update_cell(row_key, column_keys[4], message.price)

            # Textual's DataTable update_cell doesn't automatically resize columns.
            # We can force a full refresh by re-drawing the table content.
            current_boards = table.get_current_data()
            table.update_from_data(current_boards)

        tabs = self.query_one("#cb_tabs", TabbedContent)
        tabs.active = "table_tab"
        table.focus()
        self.call_after_refresh(self._hide_edit_tab)

    def _hide_edit_tab(self) -> None:
        tabs = self.query_one("#cb_tabs", TabbedContent)
        tabs.hide_tab("edit_tab")

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
            elif event.tab.id == "edit_tab":
                self.query_one("#cbe_name", Input).focus()

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
