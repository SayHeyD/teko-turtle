import os
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button


class LoadDialog(ModalScreen[Optional[str]]):
    """Minimal load dialog with a single text input for the file path to open."""

    def __init__(self, start_path: Optional[str] = None) -> None:
        super().__init__()
        self._start_path: str = start_path or os.getcwd()

    def compose(self) -> ComposeResult:
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
        if event.button.id == "cancel":
            self.dismiss(None)
            return
        if event.button.id == "open":
            path = self.query_one("#path_input", Input).value.strip()
            self.dismiss(path or None)