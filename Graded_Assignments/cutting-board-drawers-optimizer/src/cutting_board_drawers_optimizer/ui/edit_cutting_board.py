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
    """
    Form widget for editing an existing cutting board.
    Similar to CreateCuttingBoard but used for modification.
    """

    class Saved(Message):
        """Custom message containing the updated data."""

        def __init__(self, name: str, length: str, width: str, weight: str, price: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.weight = weight
            self.price = price
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the editing form layout."""
        with Vertical(id="cutting_board_edit_form"):
            yield Label("Edit Cutting Board")
            yield Input(placeholder="Name", id="cbe_name")
            yield Input(placeholder="Length (cm)", id="cbe_length")
            yield Input(placeholder="Width (cm)", id="cbe_width")
            yield Input(placeholder="Weight (g)", id="cbe_weight")
            yield Input(placeholder="Price (CHF)", id="cbe_price")
            yield Label("", id="cbe_error", classes="error")
            yield Button("Save", id="cbe_save", variant="primary")

    def set_values(self, name: str, length: str, width: str, weight: str, price: str) -> None:
        """
        Populates the form fields with the current values of the selected board.
        Strips units (e.g., ' cm') before populating the inputs.
        """
        self.query_one("#cbe_name", Input).value = name
        self.query_one("#cbe_length", Input).value = length.replace(" cm", "")
        self.query_one("#cbe_width", Input).value = width.replace(" cm", "")
        self.query_one("#cbe_weight", Input).value = weight.replace(" g", "")
        self.query_one("#cbe_price", Input).value = price.replace(" CHF", "")
        self.query_one("#cbe_error", Label).update("")
        self.query_one("#cbe_error", Label).visible = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles the 'Save' button click.
        Validates inputs and sends a 'Saved' message if valid.
        """
        if event.button.id == "cbe_save":
            name = self.query_one("#cbe_name", Input).value.strip()
            length = self.query_one("#cbe_length", Input).value.strip()
            width = self.query_one("#cbe_width", Input).value.strip()
            weight = self.query_one("#cbe_weight", Input).value.strip()
            price = self.query_one("#cbe_price", Input).value.strip()

            error_label = self.query_one("#cbe_error", Label)
            errors = []

            # 1. Validate name
            valid, err = Validator.is_valid_name(name)
            if not valid and err is not None:
                errors.append(err)

            # 2. Validate dimensions and weight
            for val, label in [(length, "Length"), (width, "Width"), (weight, "Weight")]:
                valid, err = Validator.is_positive_number(val, label)
                if not valid and err is not None:
                    errors.append(err)

            # 3. Validate price
            valid_price, err_price = Validator.is_valid_currency(price, "Price")
            if not valid_price and err_price is not None:
                errors.append(err_price)

            if errors:
                error_label.update(" ".join(errors))
                error_label.visible = True
            else:
                error_label.update("")
                error_label.visible = False
                self.post_message(self.Saved(name, length, width, weight, price))

    def on_input_submitted(self, _event: Input.Submitted) -> None:
        """Enables saving by pressing 'Enter' in any input field."""
        self.on_button_pressed(Button.Pressed(self.query_one("#cbe_save", Button)))
