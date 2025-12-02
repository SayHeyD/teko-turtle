import os
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Label, DirectoryTree, Input, Button


class SaveDialog(ModalScreen[Optional[str]]):
    """Simple modal to select a directory and enter a filename to save a config."""

    def __init__(self, start_path: Optional[str] = None) -> None:
        super().__init__()
        self._selected_dir: Optional[str] = start_path or os.getcwd()
        self._full_path_label: Optional[Label] = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Select folder and enter filename to save config"),
            DirectoryTree(self._selected_dir or os.getcwd(), id="tree"),
            Input(placeholder="filename.json", id="filename"),
            Label("", id="path_label"),
            Horizontal(
                Button("Save", id="confirm", variant="primary"),
                Button("Cancel", id="cancel"),
            ),
            id="save_dialog",
        )

    def on_directory_tree_directory_selected(self, event) -> None:  # type: ignore[override]
        # Prefer directory selection for save
        self._selected_dir = str(event.path)
        self._update_path_label()

    def on_directory_tree_file_selected(self, event) -> None:  # type: ignore[override]
        # If a file is selected, use its directory as target
        self._selected_dir = os.path.dirname(str(event.path))
        self._update_path_label()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "filename":
            self._update_path_label()

    def _update_path_label(self) -> None:
        try:
            filename = self.query_one("#filename", Input).value or ""
            dir_path = self._selected_dir or os.getcwd()
            full_path = os.path.join(dir_path, filename) if filename else dir_path
            self.query_one("#path_label", Label).update(full_path)
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
            return
        if event.button.id == "confirm":
            filename = self.query_one("#filename", Input).value.strip()
            if not filename:
                self.dismiss(None)
                return
            # Ensure .json extension by default
            if not filename.lower().endswith(".json"):
                filename += ".json"
            dir_path = self._selected_dir or os.getcwd()
            full_path = os.path.join(dir_path, filename)
            self.dismiss(full_path)