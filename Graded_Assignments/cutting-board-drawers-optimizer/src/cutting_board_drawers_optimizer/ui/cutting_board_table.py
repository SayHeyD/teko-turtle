from typing import ClassVar

from textual.binding import Binding
from textual.message import Message
from textual.widgets import (
    DataTable,
)

from cutting_board_drawers_optimizer.optimizer import CuttingBoard


class CuttingBoardTable(DataTable):
    """Custom DataTable for cutting boards with delete and edit bindings."""

    class EditRequested(Message):
        """Message sent when an edit is requested for a row."""

        def __init__(self, name: str, length: str, width: str, weight: str, price: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.weight = weight
            self.price = price
            super().__init__()

    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+d", "delete_current_row", "Delete"),
        ("ctrl+e", "edit_current_row", "Edit"),
    ]

    def action_delete_current_row(self) -> None:
        """Delete the currently selected row in the DataTable when ctrl+d is pressed."""
        if self.cursor_row is not None:
            row_key = self.coordinate_to_cell_key(self.cursor_coordinate).row_key
            self.remove_row(row_key)

    def action_edit_current_row(self) -> None:
        """Handle the edit action when ctrl+e is pressed."""
        if self.cursor_row is not None:
            row = self.get_row_at(self.cursor_row)
            self.post_message(
                self.EditRequested(
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3]),
                    str(row[4]),
                )
            )

    def populate(self, rows: list[tuple[str, str, str, str, str]]) -> None:
        """Populate the table with the provided rows."""
        header, *data_rows = rows
        self.add_columns(*[str(h) for h in header])
        for row in data_rows:
            self.add_row(*[str(cell) for cell in row])

        self.show_header = True
        self.zebra_stripes = True

    def get_current_data(self) -> list[CuttingBoard]:
        """Extract CuttingBoard objects from the DataTable."""
        cutting_boards = []
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            try:
                name = str(row[0])
                length = int(float(row[1]))
                width = int(float(row[2]))
                weight = int(float(row[3]))
                price_val = float(row[4])
                price_cents = round(price_val * 100)
                cutting_boards.append(CuttingBoard(name, length, width, weight, price_cents))
            except (ValueError, IndexError):
                continue
        return cutting_boards

    def update_from_data(self, cutting_boards: list[CuttingBoard]) -> None:
        """Update the DataTable with the provided CuttingBoard objects."""
        self.clear()
        for cb in cutting_boards:
            self.add_row(
                cb.get_name(),
                str(cb.get_length_in_centimeters()),
                str(cb.get_width_in_centimeters()),
                str(cb.get_weight_in_grams()),
                cb.get_price_in_chf(),
            )
