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


class DrawerManager(Widget):
    """Manager widget for Drawers.

    Provides two tabs:
    - A table view populated from ROWS
    - A form to add new drawers
    """

    ROWS: ClassVar[list[tuple[str | int, str, str, str | float]]] = [
        ("Name", "Length", "Width", "Maximum Load"),
        (4, "Joseph Schooling", "Singapore", 50.39),
        (2, "Michael Phelps", "United States", 51.14),
        (5, "Chad le Clos", "South Africa", 51.14),
        (6, "László Cseh", "Hungary", 51.14),
        (3, "Li Zhuhao", "China", 51.26),
        (8, "Mehdy Metella", "France", 51.58),
        (7, "Tom Shields", "United States", 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 51.84),
        (10, "Darren Burns", "Scotland", 51.84),
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
