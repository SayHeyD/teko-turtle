import os

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class LoadDialog(ModalScreen[str | None]):
    """
    Minimalistic modal dialog for selecting a file path to load a configuration.
    Displays a text input and 'Open'/'Cancel' buttons.
    Returns the path as a string upon confirmation, or None if canceled.
    """

    def __init__(self, start_path: str | None = None) -> None:
        """
        Initialize the LoadDialog.

        Args:
            start_path: The directory or file path to show by default.
        """
        super().__init__()
        self._start_path: str = start_path or os.getcwd()

    def compose(self) -> ComposeResult:
        """Composes the modal dialog UI layout."""
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
        """Handles button clicks within the modal."""
        if event.button.id == "cancel":
            # Close the modal without returning a path
            self.dismiss(None)
            return
        if event.button.id == "open":
            # Return the entered path to the calling app
            path = self.query_one("#path_input", Input).value.strip()
            self.dismiss(path or None)
