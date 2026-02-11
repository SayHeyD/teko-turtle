from typing import ClassVar

from textual.binding import Binding
from textual.widgets import (
    DataTable,
)


class CuttingBoardTable(DataTable):
    """Custom DataTable for cutting boards with delete binding."""

    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        ("ctrl+d", "delete_current_row", "Delete"),
    ]

    def action_delete_current_row(self) -> None:
        """Delete the currently selected row in the DataTable when ctrl+d is pressed."""
        if self.cursor_row is not None:
            row_key = self.coordinate_to_cell_key(self.cursor_coordinate).row_key
            self.remove_row(row_key)
