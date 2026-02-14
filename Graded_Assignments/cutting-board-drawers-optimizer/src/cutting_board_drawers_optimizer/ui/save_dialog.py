import os

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class SaveDialog(ModalScreen[str | None]):
    """Minimal save dialog with a single text input for the target file path."""

    def __init__(self, start_path: str | None = None) -> None:
        """Initialize the SaveDialog."""
        super().__init__()
        self._start_path: str = start_path or os.getcwd()

    def compose(self) -> ComposeResult:
        """Compose the SaveDialog UI."""
        default_path = self._start_path
        suggested = os.path.join(default_path, "config.json") if os.path.isdir(default_path) else default_path
        yield Vertical(
            Label("Enter the full path to save the config"),
            Input(value=suggested, id="path_input"),
            Horizontal(
                Button("Save", id="confirm", variant="primary"),
                Button("Cancel", id="cancel"),
            ),
            id="save_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel":
            # Dismiss the dialog with no path
            self.dismiss(None)
            return

        if event.button.id == "confirm":
            # Get the path from the text input
            path = self.query_one("#path_input", Input).value.strip()

            if not path:
                # Dismiss the dialog with no path
                self.dismiss(None)
                return

            if not path.lower().endswith(".json"):
                # Ensure the path ends with .json
                path += ".json"

            # Dismiss the dialog with the returned path as the result
            self.dismiss(path)
