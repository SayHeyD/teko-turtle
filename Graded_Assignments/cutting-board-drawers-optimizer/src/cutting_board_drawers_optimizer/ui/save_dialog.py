import os

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class SaveDialog(ModalScreen[str | None]):
    """
    Modal dialog for selecting a destination path to save the configuration.
    Suggests a 'config.json' filename if a directory is provided.
    Enforces a '.json' extension on the output path.
    """

    def __init__(self, start_path: str | None = None) -> None:
        """
        Initialize the SaveDialog.

        Args:
            start_path: Initial path or directory to suggest.
        """
        super().__init__()
        self._start_path: str = start_path or os.getcwd()

    def compose(self) -> ComposeResult:
        """Composes the modal dialog UI layout."""
        default_path = self._start_path
        # Suggest config.json if the start path is a directory
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
        """Handles button clicks within the modal."""
        if event.button.id == "cancel":
            self.dismiss(None)
            return

        if event.button.id == "confirm":
            path = self.query_one("#path_input", Input).value.strip()

            if not path:
                self.dismiss(None)
                return

            # Automatic extension appending
            if not path.lower().endswith(".json"):
                path += ".json"

            self.dismiss(path)
