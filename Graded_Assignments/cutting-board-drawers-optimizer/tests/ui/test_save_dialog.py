import pytest
import os
from unittest.mock import patch
from textual.widgets import Input
from cutting_board_drawers_optimizer.ui.app import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.ui.save_dialog import SaveDialog

@pytest.mark.asyncio
async def test_save_dialog_empty_path():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("ctrl+s")
        await pilot.pause()

        app.screen.query_one("#path_input", Input).value = ""
        await pilot.click("#confirm")
        await pilot.pause()

        assert not isinstance(app.screen, SaveDialog)
        assert app._last_path is None

@pytest.mark.asyncio
async def test_save_dialog_append_extension():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("ctrl+s")
        await pilot.pause()

        # Path without .json
        base_path = "myconfig"
        app.screen.query_one("#path_input", Input).value = base_path

        with patch.object(app._state, "save") as mock_save:
            await pilot.click("#confirm")
            await pilot.pause()
            mock_save.assert_called_once_with(base_path + ".json")

        # Path with .json (uppercase to check case-insensitive branch)
        await pilot.press("ctrl+s")
        await pilot.pause()
        app.screen.query_one("#path_input", Input).value = "other.JSON"
        with patch.object(app._state, "save") as mock_save:
            await pilot.click("#confirm")
            await pilot.pause()
            mock_save.assert_called_once_with("other.JSON")

@pytest.mark.asyncio
async def test_save_dialog_start_path_dir(tmp_path):
    dir_path = str(tmp_path)
    # Pass a directory as start_path
    dialog = SaveDialog(dir_path)
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await app.push_screen(dialog)
        await pilot.pause()
        input_widget = dialog.query_one("#path_input", Input)
        assert input_widget.value == os.path.join(dir_path, "config.json")

    # Pass a file as start_path
    file_path = os.path.join(dir_path, "test.json")
    dialog2 = SaveDialog(file_path)
    app2 = CuttingBoardDrawersOptimizerApp()
    async with app2.run_test() as pilot:
        await app2.push_screen(dialog2)
        await pilot.pause()
        assert dialog2.query_one("#path_input", Input).value == file_path
