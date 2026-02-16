from typing import ClassVar

from textual.binding import Binding
from textual.message import Message
from textual.widgets import DataTable

from cutting_board_drawers_optimizer.optimizer import Drawer


class DrawerTable(DataTable):
    """Custom DataTable for drawers with delete and edit bindings."""

    class EditRequested(Message):
        """Message sent when an edit is requested for a row."""

        def __init__(self, name: str, length: str, width: str, max_load: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.max_load = max_load
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
                )
            )

    def populate(self, rows: list[tuple[str, str, str, str]]) -> None:
        """Populate the table with the provided rows."""
        header, *data_rows = rows
        self.add_columns(*[str(h) for h in header])
        for row in data_rows:
            self.add_row(*[str(cell) for cell in row])

        self.show_header = True
        self.zebra_stripes = True

    def get_current_data(self) -> list[Drawer]:
        """Extract Drawer objects from the DataTable."""
        drawers = []
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
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
        self.clear()
        for drawer in drawers:
            self.add_row(
                drawer.get_name(),
                str(drawer.get_length_in_centimeters()),
                str(drawer.get_width_in_centimeters()),
                str(drawer.get_max_load_in_grams()),
            )
