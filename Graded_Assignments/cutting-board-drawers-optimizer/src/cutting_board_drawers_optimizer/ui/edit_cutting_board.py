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


class EditCuttingBoard(Widget):
    """Widget for editing an existing cutting board."""

    class Saved(Message):
        """Message sent when a cutting board is saved."""

        def __init__(self, name: str, length: str, width: str, weight: str, price: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.weight = weight
            self.price = price
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the editing form."""
        with Vertical(id="cutting_board_edit_form"):
            yield Label("Edit Cutting Board")
            yield Input(placeholder="Name", id="cbe_name")
            yield Input(placeholder="Length", id="cbe_length")
            yield Input(placeholder="Width", id="cbe_width")
            yield Input(placeholder="Weight", id="cbe_weight")
            yield Input(placeholder="Price", id="cbe_price")
            yield Label("", id="cbe_error", classes="error")
            yield Button("Save", id="cbe_save", variant="primary")

    def set_values(self, name: str, length: str, width: str, weight: str, price: str) -> None:
        """Set the values of the input fields."""
        self.query_one("#cbe_name", Input).value = name
        self.query_one("#cbe_length", Input).value = length
        self.query_one("#cbe_width", Input).value = width
        self.query_one("#cbe_weight", Input).value = weight
        self.query_one("#cbe_price", Input).value = price
        self.query_one("#cbe_error", Label).update("")
        self.query_one("#cbe_error", Label).visible = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the save button press."""
        if event.button.id == "cbe_save":
            name = self.query_one("#cbe_name", Input).value.strip()
            length = self.query_one("#cbe_length", Input).value.strip()
            width = self.query_one("#cbe_width", Input).value.strip()
            weight = self.query_one("#cbe_weight", Input).value.strip()
            price = self.query_one("#cbe_price", Input).value.strip()

            error_label = self.query_one("#cbe_error", Label)
            errors = []

            # Use generalized Validator
            valid, err = Validator.is_valid_name(name)
            if not valid and err is not None:
                errors.append(err)

            for val, label in [(length, "Length"), (width, "Width"), (weight, "Weight"), (price, "Price")]:
                valid, err = Validator.is_positive_number(val, label)
                if not valid and err is not None:
                    errors.append(err)

            if errors:
                error_label.update(" ".join(errors))
                error_label.visible = True
            else:
                error_label.update("")
                error_label.visible = False
                self.post_message(self.Saved(name, length, width, weight, price))

    def on_input_submitted(self) -> None:
        """Handle input submission (pressing Enter)."""
        # Trigger the same logic as clicking "Save"
        self.on_button_pressed(Button.Pressed(self.query_one("#cbe_save", Button)))
