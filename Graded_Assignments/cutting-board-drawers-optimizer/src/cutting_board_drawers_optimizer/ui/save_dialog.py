import os

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class SaveDialog(ModalScreen[str | None]):
    """Minimal save dialog with a single text input for the target file path."""

    def __init__(self, start_path: str | None = None) -> None:
        super().__init__()
        self._start_path: str = start_path or os.getcwd()

    def compose(self) -> ComposeResult:
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
        if event.button.id == "cancel":
            self.dismiss(None)
            return
        if event.button.id == "confirm":
            path = self.query_one("#path_input", Input).value.strip()
            if not path:
                self.dismiss(None)
                return
            if not path.lower().endswith(".json"):
                path += ".json"
            self.dismiss(path)
