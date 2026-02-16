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
from cutting_board_drawers_optimizer.ui.edit_drawer import EditDrawer
from cutting_board_drawers_optimizer.ui.drawer_table import DrawerTable


class DrawerManager(Widget):
    """Manager widget for Drawers.

    Provides three tabs:
    - A table view populated from ROWS
    - A form to add new drawers
    - A form to edit existing drawers
    """

    ROWS: ClassVar[list[tuple[str, str, str, str]]] = [
        ("Name", "Length", "Width", "Maximum Load"),
        ("Main Kitchen Drawer", "60", "50", "10000"),
        ("Small Side Drawer", "40", "30", "5000"),
    ]

    # Keybinds specific to the Drawer Manager
    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+n", "switch_to_create_tab", "Create"),
    ]

    def compose(self) -> ComposeResult:
        """Composition of the DrawerManager UI."""
        with TabbedContent(id="drawer_tabs"):
            with TabPane("Table", id="table_tab"):
                yield DrawerTable(id="drawer_table")
            with TabPane("Create", id="create_tab"):
                yield CreateDrawer()
            with TabPane("Edit", id="edit_tab"):
                yield EditDrawer()

    def on_mount(self) -> None:
        """Populate the table after the component is mounted."""
        table = self.query_one(DrawerTable)
        table.populate(self.ROWS)
        self.query_one("#drawer_tabs", TabbedContent).hide_tab("edit_tab")

    def on_create_drawer_created(self, message: CreateDrawer.Created) -> None:
        """Handle the creation of a new drawer."""
        table = self.query_one(DrawerTable)
        table.add_row(message.name, message.length, message.width, message.max_load)
        self.call_after_refresh(self.action_switch_to_table)

    def on_drawer_table_edit_requested(self, message: DrawerTable.EditRequested) -> None:
        """Handle the edit request from the table."""
        edit_form = self.query_one(EditDrawer)
        edit_form.set_values(message.name, message.length, message.width, message.max_load)
        
        tabbed_content = self.query_one("#drawer_tabs", TabbedContent)
        tabbed_content.show_tab("edit_tab")
        tabbed_content.active = "edit_tab"

    def on_edit_drawer_saved(self, message: EditDrawer.Saved) -> None:
        """Handle the saving of an edited drawer."""
        table = self.query_one(DrawerTable)
        if table.cursor_row is not None:
            column_keys = [col.key for col in table.columns.values()]
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            table.update_cell(row_key, column_keys[0], message.name)
            table.update_cell(row_key, column_keys[1], message.length)
            table.update_cell(row_key, column_keys[2], message.width)
            table.update_cell(row_key, column_keys[3], message.max_load)
        
        tabbed_content = self.query_one("#drawer_tabs", TabbedContent)
        tabbed_content.hide_tab("edit_tab")
        tabbed_content.active = "table_tab"
        table.focus()

    def action_switch_to_table(self) -> None:
        tabs = self.query_one("#drawer_tabs", TabbedContent)
        tabs.active = "table_tab"
        self.query_one(DrawerTable).focus()

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Handle tab activation within DrawerManager."""
        if event.tabbed_content.id == "drawer_tabs":
            if event.tab.id == "table_tab":
                self.query_one(DrawerTable).focus()
            elif event.tab.id == "create_tab":
                self.query_one("#d_name", Input).focus()
            elif event.tab.id == "edit_tab":
                self.query_one("#de_name", Input).focus()

    def action_switch_to_create_tab(self) -> None:
        """Switch to the create tab when ctrl+n is pressed."""
        tabbed_content = self.query_one("#drawer_tabs", TabbedContent)
        tabbed_content.active = "create_tab"

    def get_current_data(self) -> list[Drawer]:
        """Extract Drawer objects from the DataTable."""
        table = self.query_one(DrawerTable)
        return table.get_current_data()

    def update_from_data(self, drawers: list[Drawer]) -> None:
        """Update the DataTable with the provided Drawer objects."""
        table = self.query_one(DrawerTable)
        table.update_from_data(drawers)
