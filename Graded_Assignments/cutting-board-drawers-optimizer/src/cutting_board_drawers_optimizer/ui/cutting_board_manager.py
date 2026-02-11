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

from cutting_board_drawers_optimizer.optimizer import CuttingBoard
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable


class CuttingBoardManager(Widget):
    """Manager widget for Cutting Boards.

    Provides two tabs:
    - A table view populated from ROWS
    - A form to add new cutting boards
    """

    ROWS: ClassVar[list[tuple[str | int, int, int, int, float]]] = [
        ("Name", "Length", "Width", "Weight", "Price"),
        ("Large Oak", 40, 30, 2000, 50.39),
        ("Medium Beech", 30, 20, 1500, 35.50),
        ("Small Plastic", 20, 15, 500, 12.00),
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

    def get_current_data(self) -> list[CuttingBoard]:
        """Extract CuttingBoard objects from the DataTable."""
        table = self.query_one("#cutting_board_table", DataTable)
        cutting_boards = []
        # Skip header row (index 0 is name, 1 length, 2 width, 3 weight, 4 price)
        # Note: In Textual DataTable, rows are accessed by key.
        # But we can iterate over rows.
        for row_index in range(table.row_count):
            row = table.get_row_at(row_index)
            try:
                # We expect: name, length, width, weight, price
                name = str(row[0])
                # We need to convert back to appropriate types for CuttingBoard
                length = int(float(row[1]))
                width = int(float(row[2]))
                weight = int(float(row[3]))
                # Price is displayed as float/str, but constructor needs cents (int)
                price_val = float(row[4])
                price_cents = round(price_val * 100)
                cutting_boards.append(CuttingBoard(name, length, width, weight, price_cents))
            except (ValueError, IndexError):
                continue
        return cutting_boards

    def update_from_data(self, cutting_boards: list[CuttingBoard]) -> None:
        """Update the DataTable with the provided CuttingBoard objects."""
        table = self.query_one("#cutting_board_table", DataTable)
        table.clear()
        for cb in cutting_boards:
            table.add_row(
                cb.get_name(),
                str(cb.get_length_in_centimeters()),
                str(cb.get_width_in_centimeters()),
                str(cb.get_weight_in_grams()),
                cb.get_price_in_chf(),
            )
