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


class CreateDrawer(Widget):
    """Widget for creating a new drawer."""

    class Created(Message):
        """Message sent when a drawer is created."""

        def __init__(self, name: str, length: str, width: str, max_load: str, max_boards: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.max_load = max_load
            self.max_boards = max_boards
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the creation form."""
        with Vertical(id="drawer_form"):
            yield Label("Create Drawer")
            yield Input(placeholder="Name", id="d_name")
            yield Input(placeholder="Length", id="d_length")
            yield Input(placeholder="Width", id="d_width")
            yield Input(placeholder="Maximum Load", id="d_max_load")
            yield Input(placeholder="Max Boards", id="d_max_boards")
            yield Label("", id="d_error", classes="error")
            yield Button("Add", id="d_add", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the add button press."""
        if event.button.id == "d_add":
            name = self.query_one("#d_name", Input).value.strip()
            length = self.query_one("#d_length", Input).value.strip()
            width = self.query_one("#d_width", Input).value.strip()
            max_load = self.query_one("#d_max_load", Input).value.strip()
            max_boards = self.query_one("#d_max_boards", Input).value.strip()

            error_label = self.query_one("#d_error", Label)
            errors = []

            # Use generalized Validator
            valid, err = Validator.is_valid_name(name)
            if not valid and err is not None:
                errors.append(err)

            for val, label in [
                (length, "Length"),
                (width, "Width"),
                (max_load, "Maximum Load"),
                (max_boards, "Max Boards"),
            ]:
                valid, err = Validator.is_positive_number(val, label)
                if not valid and err is not None:
                    errors.append(err)

            if errors:
                error_label.update(" ".join(errors))
                error_label.visible = True
            else:
                error_label.update("")
                error_label.visible = False
                self.post_message(self.Created(name, length, width, max_load, max_boards))
                # Clear inputs after successful creation
                for input_widget in self.query(Input):
                    input_widget.value = ""

    def on_input_submitted(self) -> None:
        """Handle input submission (pressing Enter)."""
        # Trigger the same logic as clicking "Add"
        self.on_button_pressed(Button.Pressed(self.query_one("#d_add", Button)))
