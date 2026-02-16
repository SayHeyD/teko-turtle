from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import (
    Button,
    Input,
    Label,
)


class CreateDrawer(Widget):
    """Widget for creating a new drawer."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.errors: list[str] = []

    class Created(Message):
        """Message sent when a drawer is created."""

        def __init__(self, name: str, length: str, width: str, max_load: str) -> None:
            self.name = name
            self.length = length
            self.width = width
            self.max_load = max_load
            super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the creation form."""
        with Vertical(id="drawer_form"):
            yield Label("Create Drawer")
            yield Input(placeholder="Name", id="d_name")
            yield Input(placeholder="Length", id="d_length")
            yield Input(placeholder="Width", id="d_width")
            yield Input(placeholder="Maximum Load", id="d_max_load")
            yield Label("", id="d_error", classes="error")
            yield Button("Add", id="d_add")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the add button press."""
        if event.button.id == "d_add":
            name = self.query_one("#d_name", Input).value.strip()
            length = self.query_one("#d_length", Input).value.strip()
            width = self.query_one("#d_width", Input).value.strip()
            max_load = self.query_one("#d_max_load", Input).value.strip()

            error_label = self.query_one("#d_error", Label)
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
                ml_val = float(max_load)
                if ml_val <= 0:
                    errors.append("Maximum Load must be positive.")
            except ValueError:
                errors.append("Maximum Load must be a number.")

            if errors:
                self.errors = errors
                error_label.update(" ".join(errors))
                error_label.visible = True
            else:
                self.errors = []
                error_label.update("")
                error_label.visible = False
                self.post_message(self.Created(name, length, width, max_load))

    def on_input_submitted(self) -> None:
        """Handle input submission (pressing Enter)."""
        # Trigger the same logic as clicking "Add"
        self.on_button_pressed(Button.Pressed(self.query_one("#d_add", Button)))
