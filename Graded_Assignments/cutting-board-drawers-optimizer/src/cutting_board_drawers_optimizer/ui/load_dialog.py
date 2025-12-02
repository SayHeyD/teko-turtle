import os
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Label, DirectoryTree, Button


class LoadDialog(ModalScreen[Optional[str]]):
    """Simple modal to select a config file to load."""

    def __init__(self, start_path: Optional[str] = None) -> None:
        super().__init__()
        self._start_path: str = start_path or os.getcwd()
        self._selected_file: Optional[str] = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Select a config file to load"),
            DirectoryTree(self._start_path, id="tree"),
            Label("", id="selection_label"),
            Horizontal(
                Button("Open", id="open", variant="primary"),
                Button("Cancel", id="cancel"),
            ),
            id="load_dialog",
        )

    def on_directory_tree_file_selected(self, event) -> None:  # type: ignore[override]
        self._selected_file = str(event.path)
        self.query_one("#selection_label", Label).update(self._selected_file)

    def on_directory_tree_directory_selected(self, event) -> None:  # type: ignore[override]
        # Clear selection when navigating directories
        self._selected_file = None
        self.query_one("#selection_label", Label).update("")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
            return
        if event.button.id == "open":
            self.dismiss(self._selected_file)