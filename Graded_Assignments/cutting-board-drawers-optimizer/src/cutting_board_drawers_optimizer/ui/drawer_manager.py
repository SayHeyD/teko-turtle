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


class DrawerManager(Widget):
    """Manager widget for Drawers.

    Provides two tabs:
    - A table view populated from ROWS
    - A form to add new drawers
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

    def on_mount(self) -> None:
        """Populate the table after the component is mounted."""
        table = self.query_one(DrawerTable)
        table.populate(self.ROWS)

    def on_create_drawer_created(self, message: CreateDrawer.Created) -> None:
        """Handle the creation of a new drawer."""
        table = self.query_one(DrawerTable)
        table.add_row(message.name, message.length, message.width, message.max_load)
        self.call_after_refresh(self.action_switch_to_table)

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
