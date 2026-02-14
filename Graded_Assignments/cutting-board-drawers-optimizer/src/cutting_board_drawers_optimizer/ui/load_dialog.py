import os

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class LoadDialog(ModalScreen[str | None]):
    """Minimal load dialog with a single text input for the file path to open."""

    def __init__(self, start_path: str | None = None) -> None:
        """Initialize the LoadDialog."""
        super().__init__()
        self._start_path: str = start_path or os.getcwd()

    def compose(self) -> ComposeResult:
        """Compose the LoadDialog UI."""
        default_path = self._start_path
        yield Vertical(
            Label("Enter the full path of the config file to load"),
            Input(value=default_path, id="path_input"),
            Horizontal(
                Button("Open", id="open", variant="primary"),
                Button("Cancel", id="cancel"),
            ),
            id="load_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel":
            # Dismiss the dialog with no path
            self.dismiss(None)
            return
        if event.button.id == "open":
            # Dismiss the dialog with the returned result being the path
            path = self.query_one("#path_input", Input).value.strip()
            self.dismiss(path or None)
