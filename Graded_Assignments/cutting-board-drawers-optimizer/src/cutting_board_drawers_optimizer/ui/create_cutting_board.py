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


class CreateCuttingBoard(Widget):
    """
    Form widget for defining a new cutting board.
    Validates inputs and sends a 'Created' message to the parent manager.
    """

    class Created(Message):
        """Custom message containing the data for the new cutting board."""

        def __init__(self, name: str, length: str, width: str, weight: str, price: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.weight = weight
            self.price = price
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the layout of the creation form."""
        with Vertical(id="cutting_board_form"):
            yield Label("Create Cutting Board")
            yield Input(placeholder="Name", id="cb_name")
            yield Input(placeholder="Length (cm)", id="cb_length")
            yield Input(placeholder="Width (cm)", id="cb_width")
            yield Input(placeholder="Weight (g)", id="cb_weight")
            yield Input(placeholder="Price (CHF)", id="cb_price")
            yield Label("", id="cb_error", classes="error")
            yield Button("Add", id="cb_add", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles the 'Add' button click.
        Validates all fields before creating the board.
        """
        if event.button.id == "cb_add":
            # Extract values and trim whitespace
            name = self.query_one("#cb_name", Input).value.strip()
            length = self.query_one("#cb_length", Input).value.strip()
            width = self.query_one("#cb_width", Input).value.strip()
            weight = self.query_one("#cb_weight", Input).value.strip()
            price = self.query_one("#cb_price", Input).value.strip()

            error_label = self.query_one("#cb_error", Label)
            errors = []

            # 1. Validate name
            valid, err = Validator.is_valid_name(name)
            if not valid and err is not None:
                errors.append(err)

            # 2. Validate numeric dimensions and weight
            for val, label in [(length, "Length"), (width, "Width"), (weight, "Weight")]:
                valid, err = Validator.is_positive_number(val, label)
                if not valid and err is not None:
                    errors.append(err)

            # 3. Validate price as currency (max 2 decimals)
            valid_price, err_price = Validator.is_valid_currency(price, "Price")
            if not valid_price and err_price is not None:
                errors.append(err_price)

            if errors:
                # Show all validation errors in the error label
                error_label.update(" ".join(errors))
                error_label.visible = True
            else:
                # Success: notify parent manager and clear form
                error_label.update("")
                error_label.visible = False
                self.post_message(self.Created(name, length, width, weight, price))
                # Clear all input fields for the next entry
                for input_widget in self.query(Input):
                    input_widget.value = ""

    def on_input_submitted(self, _event: Input.Submitted) -> None:
        """Enables submitting the form by pressing 'Enter' in any input field."""
        self.on_button_pressed(Button.Pressed(self.query_one("#cb_add", Button)))
