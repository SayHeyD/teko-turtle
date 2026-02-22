from typing import ClassVar

from textual.binding import Binding
from textual.message import Message
from textual.widgets import (
    DataTable,
)

from cutting_board_drawers_optimizer.optimizer import CuttingBoard


class CuttingBoardTable(DataTable):
    """
    Custom DataTable tailored for displaying and managing Cutting Boards.
    Supports keyboard shortcuts for deleting (Ctrl+D) and editing (Ctrl+E) rows.
    """

    class EditRequested(Message):
        """Custom message sent to the parent manager when the user wants to edit a cutting board."""

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
        """Deletes the currently selected row from the table."""
        if self.cursor_row is not None:
            row_key = self.coordinate_to_cell_key(self.cursor_coordinate).row_key
            self.remove_row(row_key)

    def action_edit_current_row(self) -> None:
        """
        Retrieves data from the selected row and sends an EditRequested message
        to trigger the edit form.
        """
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

    def populate(self, rows: list[tuple[str, str, str, str, str, str]]) -> None:
        """
        Initializes columns and rows from a list of tuples.
        Used for initial population with sample data.
        """
        header, *data_rows = rows
        self.add_columns(*[str(h) for h in header])
        for row in data_rows:
            self.add_row(*[str(cell) for cell in row])

        self.show_header = True
        self.zebra_stripes = True

    def get_current_data(self) -> list[CuttingBoard]:
        """
        Parses the strings currently displayed in the table back into CuttingBoard objects.
        This is necessary for saving the configuration or running optimization.
        Robustly handles units (like 'cm', 'g', 'CHF') by stripping them before parsing.
        """
        cutting_boards = []
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            try:
                name = str(row[0])
                # Extract numeric part from strings like '40 cm'
                length = int(float(str(row[1]).split(" ")[0]))
                width = int(float(str(row[2]).split(" ")[0]))
                weight = int(float(str(row[3]).split(" ")[0]))
                # Parse price from string like '50.39 CHF' and convert back to centimes
                price_val = float(str(row[4]).split(" ")[0])
                price_cents = round(price_val * 100)
                cutting_boards.append(CuttingBoard(name, length, width, weight, price_cents))
            except (ValueError, IndexError):
                # Skip rows that cannot be parsed correctly
                continue
        return cutting_boards

    def update_from_data(self, cutting_boards: list[CuttingBoard]) -> None:
        """
        Clears the table and repopulates it with the provided CuttingBoard objects.
        Ensures that units and area calculations are displayed correctly.
        """
        self.clear()
        for cb in cutting_boards:
            self.add_row(
                cb.get_name(),
                f"{cb.get_length_in_centimeters()} cm",
                f"{cb.get_width_in_centimeters()} cm",
                f"{cb.get_weight_in_grams()} g",
                f"{cb.get_price_in_chf()} CHF",
                f"{cb.area} cm²",
            )
