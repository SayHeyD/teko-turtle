from typing import ClassVar

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import (
    Button,
    DataTable,
    Input,
    Label,
    TabbedContent,
    TabPane,
)

from cutting_board_drawers_optimizer.optimizer import Drawer


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

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Table", id="table_tab"):
                yield DataTable(id="drawer_table")
            with TabPane("Create", id="create_tab"), Vertical(id="drawer_form"):
                yield Label("Create Drawer")
                yield Input(placeholder="Name", id="d_name")
                yield Input(placeholder="Length", id="d_length")
                yield Input(placeholder="Width", id="d_width")
                yield Input(placeholder="Maximum Load", id="d_max_load")
                yield Button("Add", id="d_add")

    def on_mount(self) -> None:
        table = self.query_one("#drawer_table", DataTable)
        header, *rows = self.ROWS
        table.add_columns(*[str(h) for h in header])
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        table.show_header = True
        table.zebra_stripes = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "d_add":
            name = self.query_one("#d_name", Input).value or ""
            length = self.query_one("#d_length", Input).value or ""
            width = self.query_one("#d_width", Input).value or ""
            max_load = self.query_one("#d_max_load", Input).value or ""
            self.query_one("#drawer_table", DataTable).add_row(name, length, width, max_load)

    def get_current_data(self) -> list[Drawer]:
        """Extract Drawer objects from the DataTable."""
        table = self.query_one("#drawer_table", DataTable)
        drawers = []
        for row_index in range(table.row_count):
            row = table.get_row_at(row_index)
            try:
                # We expect: name, length, width, max_load
                name = str(row[0])
                length = int(float(row[1]))
                width = int(float(row[2]))
                max_load = int(float(row[3]))
                drawers.append(Drawer(name, length, width, max_load))
            except (ValueError, IndexError):
                continue
        return drawers

    def update_from_data(self, drawers: list[Drawer]) -> None:
        """Update the DataTable with the provided Drawer objects."""
        table = self.query_one("#drawer_table", DataTable)
        table.clear()
        for drawer in drawers:
            table.add_row(
                drawer.get_name(),
                str(drawer.get_length_in_centimeters()),
                str(drawer.get_width_in_centimeters()),
                str(drawer.get_max_load_in_grams()),
            )
