from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import (
    Button,
    Input,
    Label,
)

from cutting_board_drawers_optimizer.ui.validator import Validator


class EditDrawer(Widget):
    """Widget for editing an existing drawer."""

    class Saved(Message):
        """Message sent when a drawer is saved."""

        def __init__(self, name: str, length: str, width: str, max_load: str, max_boards: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.max_load = max_load
            self.max_boards = max_boards
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the editing form."""
        with Vertical(id="drawer_edit_form"):
            yield Label("Edit Drawer")
            yield Input(placeholder="Name", id="de_name")
            yield Input(placeholder="Length", id="de_length")
            yield Input(placeholder="Width", id="de_width")
            yield Input(placeholder="Maximum Load", id="de_max_load")
            yield Input(placeholder="Max Boards", id="de_max_boards")
            yield Label("", id="de_error", classes="error")
            yield Button("Save", id="de_save", variant="primary")

    def set_values(self, name: str, length: str, width: str, max_load: str, max_boards: str) -> None:
        """Set the values of the input fields."""
        self.query_one("#de_name", Input).value = name
        self.query_one("#de_length", Input).value = length
        self.query_one("#de_width", Input).value = width
        self.query_one("#de_max_load", Input).value = max_load
        self.query_one("#de_max_boards", Input).value = max_boards
        self.query_one("#de_error", Label).update("")
        self.query_one("#de_error", Label).visible = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the save button press."""
        if event.button.id == "de_save":
            name = self.query_one("#de_name", Input).value.strip()
            length = self.query_one("#de_length", Input).value.strip()
            width = self.query_one("#de_width", Input).value.strip()
            max_load = self.query_one("#de_max_load", Input).value.strip()
            max_boards = self.query_one("#de_max_boards", Input).value.strip()

            error_label = self.query_one("#de_error", Label)
            errors = []

            # Use generalized Validator
            valid, err = Validator.is_valid_name(name)
            if not valid and err is not None:
                errors.append(err)

            for val, label in [(length, "Length"), (width, "Width"), (max_load, "Maximum Load"), (max_boards, "Max Boards")]:
                valid, err = Validator.is_positive_number(val, label)
                if not valid and err is not None:
                    errors.append(err)

            if errors:
                error_label.update(" ".join(errors))
                error_label.visible = True
            else:
                error_label.update("")
                error_label.visible = False
                self.post_message(self.Saved(name, length, width, max_load, max_boards))

    def on_input_submitted(self) -> None:
        """Handle input submission (pressing Enter)."""
        # Trigger the same logic as clicking "Save"
        self.on_button_pressed(Button.Pressed(self.query_one("#de_save", Button)))
