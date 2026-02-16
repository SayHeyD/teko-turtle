from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import (
    Button,
    Input,
    Label,
)


class CreateCuttingBoard(Widget):
    """Widget for creating a new cutting board."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.errors: list[str] = []

    class Created(Message):
        """Message sent when a cutting board is created."""

        def __init__(self, name: str, length: str, width: str, weight: str, price: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.weight = weight
            self.price = price
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the creation form."""
        with Vertical(id="cutting_board_form"):
            yield Label("Create Cutting Board")
            yield Input(placeholder="Name", id="cb_name")
            yield Input(placeholder="Length", id="cb_length")
            yield Input(placeholder="Width", id="cb_width")
            yield Input(placeholder="Weight", id="cb_weight")
            yield Input(placeholder="Price", id="cb_price")
            yield Label("", id="cb_error", classes="error")
            yield Button("Add", id="cb_add")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the add button press."""
        if event.button.id == "cb_add":
            name = self.query_one("#cb_name", Input).value.strip()
            length = self.query_one("#cb_length", Input).value.strip()
            width = self.query_one("#cb_width", Input).value.strip()
            weight = self.query_one("#cb_weight", Input).value.strip()
            price = self.query_one("#cb_price", Input).value.strip()

            error_label = self.query_one("#cb_error", Label)
            errors = []

            if not name:
                errors.append("Name is required.")

            try:
                l_val = float(length)
                if l_val <= 0:
                    errors.append("Length must be positive.")
            except ValueError:
                errors.append("Length must be a number.")

            try:
                w_val = float(width)
                if w_val <= 0:
                    errors.append("Width must be positive.")
            except ValueError:
                errors.append("Width must be a number.")

            try:
                wt_val = float(weight)
                if wt_val <= 0:
                    errors.append("Weight must be positive.")
            except ValueError:
                errors.append("Weight must be a number.")

            try:
                p_val = float(price)
                if p_val <= 0:
                    errors.append("Price must be positive.")
            except ValueError:
                errors.append("Price must be a number.")

            if errors:
                self.errors = errors
                error_label.update(" ".join(errors))
                error_label.visible = True
            else:
                self.errors = []
                error_label.update("")
                error_label.visible = False
                self.post_message(self.Created(name, length, width, weight, price))

    def on_input_submitted(self) -> None:
        """Handle input submission (pressing Enter)."""
        # Trigger the same logic as clicking "Add"
        self.on_button_pressed(Button.Pressed(self.query_one("#cb_add", Button)))
