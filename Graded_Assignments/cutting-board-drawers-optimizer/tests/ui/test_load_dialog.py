import pytest
import os
from unittest.mock import patch
from textual.widgets import Input
from cutting_board_drawers_optimizer.ui.app import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.ui.load_dialog import LoadDialog


@pytest.mark.asyncio
async def test_load_dialog_empty_path():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("ctrl+o")
        await pilot.pause()

        # Empty value should result in None being passed to dismiss
        app.screen.query_one("#path_input", Input).value = ""
        await pilot.click("#open")
        await pilot.pause()

        assert not isinstance(app.screen, LoadDialog)


@pytest.mark.asyncio
async def test_load_dialog_initial_path():
    start_path = "/test/path"
    dialog = LoadDialog(start_path)
    assert dialog._start_path == start_path


@pytest.mark.asyncio
async def test_load_dialog_default_path():
    dialog = LoadDialog()
    assert dialog._start_path == os.getcwd()
