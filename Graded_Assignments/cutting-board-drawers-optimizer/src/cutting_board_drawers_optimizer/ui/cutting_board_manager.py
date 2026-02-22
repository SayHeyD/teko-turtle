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
    Coordinates the three sub-tabs: Table (View), Create (Add), and Edit.
    """

    # Header row for the table
    ROWS: ClassVar[list[tuple[str, str, str, str, str, str]]] = [
        ("Name", "Length", "Width", "Weight", "Price", "Area"),
    ]

    # Keyboard shortcuts specific to this manager
    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+n", "switch_to_create_tab", "Create"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the layout with three tabs."""
        with TabbedContent(id="cb_tabs"):
            with TabPane("Table", id="table_tab"):
                yield CuttingBoardTable(id="cutting_board_table")
            with TabPane("Create", id="create_tab"):
                yield CreateCuttingBoard()
            with TabPane("Edit", id="edit_tab"):
                yield EditCuttingBoard()

    def on_mount(self) -> None:
        """Populate the table and hide the 'Edit' tab initially."""
        table = self.query_one(CuttingBoardTable)
        table.populate(self.ROWS)
        self.query_one("#cb_tabs", TabbedContent).hide_tab("edit_tab")

    def on_create_cutting_board_created(self, message: CreateCuttingBoard.Created) -> None:
        """
        Catches the 'Created' message from the CreateCuttingBoard form
        and adds a new row to the table.
        """
        table = self.query_one(CuttingBoardTable)
        area = int(message.length) * int(message.width)
        price_val = float(message.price)
        table.add_row(
            message.name,
            f"{message.length} cm",
            f"{message.width} cm",
            f"{message.weight} g",
            f"{price_val:.2f} CHF",
            f"{area} cm²",
        )
        # Switch back to the table view to show the new entry
        self.action_switch_to_table()

    def on_cutting_board_table_edit_requested(self, message: CuttingBoardTable.EditRequested) -> None:
        """
        Catches the 'EditRequested' message from the table (Ctrl+E),
        populates the edit form, and shows the 'Edit' tab.
        """
        edit_form = self.query_one(EditCuttingBoard)
        edit_form.set_values(message.name, message.length, message.width, message.weight, message.price)

        tabbed_content = self.query_one("#cb_tabs", TabbedContent)
        tabbed_content.show_tab("edit_tab")
        tabbed_content.active = "edit_tab"

    def on_edit_cutting_board_saved(self, message: EditCuttingBoard.Saved) -> None:
        """
        Catches the 'Saved' message from the edit form,
        updates the selected row in the table, and hides the 'Edit' tab.
        """
        table = self.query_one(CuttingBoardTable)
        if table.cursor_row is not None:
            column_keys = [col.key for col in table.columns.values()]
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            # Update cells manually
            table.update_cell(row_key, column_keys[0], message.name)
            table.update_cell(row_key, column_keys[1], message.length)
            table.update_cell(row_key, column_keys[2], message.width)
            table.update_cell(row_key, column_keys[3], message.weight)
            table.update_cell(row_key, column_keys[4], message.price)

            # Re-calculating area and refreshing table formatting
            current_boards = table.get_current_data()
            table.update_from_data(current_boards)

        tabs = self.query_one("#cb_tabs", TabbedContent)
        tabs.active = "table_tab"
        table.focus()
        # Hide the edit tab after saving
        self.call_after_refresh(self._hide_edit_tab)

    def _hide_edit_tab(self) -> None:
        tabs = self.query_one("#cb_tabs", TabbedContent)
        tabs.hide_tab("edit_tab")

    def action_switch_to_table(self) -> None:
        """Activates the table tab and gives it focus."""
        tabs = self.query_one("#cb_tabs", TabbedContent)
        tabs.active = "table_tab"
        self.query_one(CuttingBoardTable).focus()

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Ensures the correct widget (table or first input field) is focused when switching tabs."""
        if event.tabbed_content.id == "cb_tabs":
            if event.tab.id == "table_tab":
                self.query_one(CuttingBoardTable).focus()
            elif event.tab.id == "create_tab":
                self.query_one("#cb_name", Input).focus()
            elif event.tab.id == "edit_tab":
                self.query_one("#cbe_name", Input).focus()

    def action_switch_to_create_tab(self) -> None:
        """Shortcut action for Ctrl+N."""
        tabbed_content = self.query_one("#cb_tabs", TabbedContent)
        tabbed_content.active = "create_tab"

    def get_current_data(self) -> list[CuttingBoard]:
        """Returns the list of CuttingBoard objects from the table."""
        table = self.query_one(CuttingBoardTable)
        return table.get_current_data()

    def update_from_data(self, cutting_boards: list[CuttingBoard]) -> None:
        """Updates the table content from a list of CuttingBoard objects."""
        table = self.query_one(CuttingBoardTable)
        table.update_from_data(cutting_boards)
