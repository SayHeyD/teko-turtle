from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import (
    Input,
    TabbedContent,
    TabPane,
)

from cutting_board_drawers_optimizer.optimizer import Drawer
from cutting_board_drawers_optimizer.ui.create_drawer import CreateDrawer
from cutting_board_drawers_optimizer.ui.drawer_table import DrawerTable
from cutting_board_drawers_optimizer.ui.edit_drawer import EditDrawer


class DrawerManager(Widget):
    """
    Manager widget for Drawers.
    Coordinates the three sub-tabs: Table (View), Create (Add), and Edit.
    """

    # Header row for the table
    ROWS: ClassVar[list[tuple[str, str, str, str, str, str]]] = [
        ("Name", "Length", "Width", "Maximum Load", "Max Boards", "Area"),
    ]

    # Keyboard shortcuts specific to this manager
    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+n", "switch_to_create_tab", "Create"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the layout with three tabs."""
        with TabbedContent(id="drawer_tabs"):
            with TabPane("Table", id="table_tab"):
                yield DrawerTable(id="drawer_table")
            with TabPane("Create", id="create_tab"):
                yield CreateDrawer()
            with TabPane("Edit", id="edit_tab"):
                yield EditDrawer()

    def on_mount(self) -> None:
        """Populate the table and hide the 'Edit' tab initially."""
        table = self.query_one(DrawerTable)
        table.populate(self.ROWS)
        self.query_one("#drawer_tabs", TabbedContent).hide_tab("edit_tab")

    def on_create_drawer_created(self, message: CreateDrawer.Created) -> None:
        """
        Catches the 'Created' message from the CreateDrawer form
        and adds a new row to the table.
        """
        table = self.query_one(DrawerTable)
        area = int(message.length) * int(message.width)
        table.add_row(
            message.name,
            f"{message.length} cm",
            f"{message.width} cm",
            f"{message.max_load} g",
            message.max_boards,
            f"{area} cm²",
        )
        # Switch back to the table view to show the new entry
        self.call_after_refresh(self.action_switch_to_table)

    def on_drawer_table_edit_requested(self, message: DrawerTable.EditRequested) -> None:
        """
        Catches the 'EditRequested' message from the table (Ctrl+E),
        populates the edit form, and shows the 'Edit' tab.
        """
        edit_form = self.query_one(EditDrawer)
        edit_form.set_values(message.name, message.length, message.width, message.max_load, message.max_boards)

        tabbed_content = self.query_one("#drawer_tabs", TabbedContent)
        tabbed_content.show_tab("edit_tab")
        tabbed_content.active = "edit_tab"

    def on_edit_drawer_saved(self, message: EditDrawer.Saved) -> None:
        """
        Catches the 'Saved' message from the edit form,
        updates the selected row in the table, and hides the 'Edit' tab.
        """
        table = self.query_one(DrawerTable)
        if table.cursor_row is not None:
            column_keys = [col.key for col in table.columns.values()]
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            # Update cells manually
            table.update_cell(row_key, column_keys[0], message.name)
            table.update_cell(row_key, column_keys[1], message.length)
            table.update_cell(row_key, column_keys[2], message.width)
            table.update_cell(row_key, column_keys[3], message.max_load)
            table.update_cell(row_key, column_keys[4], message.max_boards)

            # Re-calculating area and refreshing table formatting
            current_drawers = table.get_current_data()
            table.update_from_data(current_drawers)

        tabbed_content = self.query_one("#drawer_tabs", TabbedContent)
        tabbed_content.hide_tab("edit_tab")
        tabbed_content.active = "table_tab"
        table.focus()

    def action_switch_to_table(self) -> None:
        """Activates the table tab and gives it focus."""
        tabs = self.query_one("#drawer_tabs", TabbedContent)
        tabs.active = "table_tab"
        self.query_one(DrawerTable).focus()

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Ensures the correct widget (table or first input field) is focused when switching tabs."""
        if event.tabbed_content.id == "drawer_tabs":
            if event.tab.id == "table_tab":
                self.query_one(DrawerTable).focus()
            elif event.tab.id == "create_tab":
                self.query_one("#d_name", Input).focus()
            elif event.tab.id == "edit_tab":
                self.query_one("#de_name", Input).focus()

    def action_switch_to_create_tab(self) -> None:
        """Shortcut action for Ctrl+N."""
        tabbed_content = self.query_one("#drawer_tabs", TabbedContent)
        tabbed_content.active = "create_tab"

    def get_current_data(self) -> list[Drawer]:
        """Returns the list of Drawer objects from the table."""
        table = self.query_one(DrawerTable)
        return table.get_current_data()

    def update_from_data(self, drawers: list[Drawer]) -> None:
        """Updates the table content from a list of Drawer objects."""
        table = self.query_one(DrawerTable)
        table.update_from_data(drawers)
