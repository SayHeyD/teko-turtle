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
            yield Button("Add", id="cb_add")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the add button press."""
        if event.button.id == "cb_add":
            name = self.query_one("#cb_name", Input).value or ""
            length = self.query_one("#cb_length", Input).value or ""
            width = self.query_one("#cb_width", Input).value or ""
            weight = self.query_one("#cb_weight", Input).value or ""
            price = self.query_one("#cb_price", Input).value or ""

            self.post_message(self.Created(name, length, width, weight, price))
