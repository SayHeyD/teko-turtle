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

from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable


class CuttingBoardManager(Widget):
    """Manager widget for Cutting Boards.

    Provides two tabs:
    - A table view populated from ROWS
    - A form to add new cutting boards
    """

    ROWS: ClassVar[list[tuple[str | int, str, str, str | int, str | float]]] = [
        ("Name", "Length", "Width", "Weight", "Price"),
        (4, "Joseph Schooling", "Singapore", 2000, 50.39),
        (2, "Michael Phelps", "United States", 2000, 51.14),
        (5, "Chad le Clos", "South Africa", 2000, 51.14),
        (6, "László Cseh", "Hungary", 2000, 51.14),
        (3, "Li Zhuhao", "China", 2000, 51.26),
        (8, "Mehdy Metella", "France", 2000, 51.58),
        (7, "Tom Shields", "United States", 2000, 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 2000, 51.84),
        (10, "Darren Burns", "Scotland", 2000, 51.84),
        (5, "Chad le Clos", "South Africa", 2000, 51.14),
        (6, "László Cseh", "Hungary", 2000, 51.14),
        (3, "Li Zhuhao", "China", 2000, 51.26),
        (8, "Mehdy Metella", "France", 2000, 51.58),
        (7, "Tom Shields", "United States", 2000, 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 2000, 51.84),
        (10, "Darren Burns", "Scotland", 2000, 51.84),
        (5, "Chad le Clos", "South Africa", 2000, 51.14),
        (6, "László Cseh", "Hungary", 2000, 51.14),
        (3, "Li Zhuhao", "China", 2000, 51.26),
        (8, "Mehdy Metella", "France", 2000, 51.58),
        (7, "Tom Shields", "United States", 2000, 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 2000, 51.84),
        (10, "Darren Burns", "Scotland", 2000, 51.84),
        (5, "Chad le Clos", "South Africa", 2000, 51.14),
        (6, "László Cseh", "Hungary", 2000, 51.14),
        (3, "Li Zhuhao", "China", 2000, 51.26),
        (8, "Mehdy Metella", "France", 2000, 51.58),
        (7, "Tom Shields", "United States", 2000, 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 2000, 51.84),
        (10, "Darren Burns", "Scotland", 2000, 51.84),
        (5, "Chad le Clos", "South Africa", 2000, 51.14),
        (6, "László Cseh", "Hungary", 2000, 51.14),
        (3, "Li Zhuhao", "China", 2000, 51.26),
        (8, "Mehdy Metella", "France", 2000, 51.58),
        (7, "Tom Shields", "United States", 2000, 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 2000, 51.84),
        (10, "Darren Burns", "Scotland", 2000, 51.84),
        (5, "Chad le Clos", "South Africa", 2000, 51.14),
        (6, "László Cseh", "Hungary", 2000, 51.14),
        (3, "Li Zhuhao", "China", 2000, 51.26),
        (8, "Mehdy Metella", "France", 2000, 51.58),
        (7, "Tom Shields", "United States", 2000, 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 2000, 51.84),
        (10, "Darren Burns", "Scotland", 2000, 51.84),
    ]

    BINDINGS: ClassVar[list[tuple[str, str, str]]] = [
        ("ctrl+n", "switch_to_create_tab", "Create"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Table", id="table_tab"):
                yield CuttingBoardTable(id="cutting_board_table")
            with TabPane("Create", id="create_tab"), Vertical(id="cutting_board_form"):
                yield Label("Create Cutting Board")
                yield Input(placeholder="Name", id="cb_name")
                yield Input(placeholder="Length", id="cb_length")
                yield Input(placeholder="Width", id="cb_width")
                yield Input(placeholder="Weight", id="cb_weight")
                yield Input(placeholder="Price", id="cb_price")
                yield Button("Add", id="cb_add")

    def on_mount(self) -> None:
        """Populate the table after mounting."""
        table = self.query_one("#cutting_board_table", DataTable)
        header, *rows = self.ROWS
        table.add_columns(*[str(h) for h in header])
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        table.show_header = True
        table.zebra_stripes = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cb_add":
            # Read values and append a new row (stringly typed for simplicity)
            name = self.query_one("#cb_name", Input).value or ""
            length = self.query_one("#cb_length", Input).value or ""
            width = self.query_one("#cb_width", Input).value or ""
            weight = self.query_one("#cb_weight", Input).value or ""
            price = self.query_one("#cb_price", Input).value or ""
            self.query_one("#cutting_board_table", DataTable).add_row(name, length, width, weight, price)

    def action_switch_to_create_tab(self) -> None:
        """Switch to the create tab when ctrl+n is pressed."""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "create_tab"
