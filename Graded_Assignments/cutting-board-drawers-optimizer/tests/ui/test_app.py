import os
import pytest
from textual.widgets import Input, TabbedContent
from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.ui.save_dialog import SaveDialog
from cutting_board_drawers_optimizer.ui.load_dialog import LoadDialog
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable

from textual.widgets import Header, Footer

from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp


@pytest.mark.asyncio
async def test_that_app_shows_correct_header_content():
    app = CuttingBoardDrawersOptimizerApp()

    async with app.run_test():
        header = app.query_one(Header)
        assert header.icon == "🔪"
        assert header._show_clock is True
        assert header.screen_title == "Cutting Board Drawers Optimizer"


@pytest.mark.asyncio
async def test_that_app_has_footer():
    app = CuttingBoardDrawersOptimizerApp()

    async with app.run_test():
        footer = app.query_one(Footer)
        assert footer is not None


@pytest.mark.asyncio
async def test_app_save_config_flow(tmp_path):
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        save_path = str(tmp_path / "test_config.json")

        # Trigger save action
        await pilot.press("ctrl+s")
        await pilot.pause()

        # Verify SaveDialog is pushed
        assert isinstance(app.screen, SaveDialog)

        # Fill path and confirm
        app.screen.query_one("#path_input", Input).value = save_path
        await pilot.click("#confirm")
        await pilot.pause()

        # Verify file exists
        assert os.path.exists(save_path)
        assert app._last_path == save_path


@pytest.mark.asyncio
async def test_app_load_config_flow(tmp_path):
    # First create a config file
    config_path = str(tmp_path / "load_test.json")
    app_to_save = CuttingBoardDrawersOptimizerApp()
    async with app_to_save.run_test() as pilot:
        # Add a custom item to verify it's loaded later
        cb_manager = app_to_save.query_one(CuttingBoardManager)
        cb_manager.action_switch_to_create_tab()
        await pilot.pause()
        await pilot.click("#cb_name")
        await pilot.press("L", "o", "a", "d", " ", "M", "e")
        await pilot.click("#cb_length")
        await pilot.press("1", "0")
        await pilot.click("#cb_width")
        await pilot.press("1", "0")
        await pilot.click("#cb_weight")
        await pilot.press("1", "0")
        await pilot.click("#cb_price")
        await pilot.press("1", "0")
        await pilot.click("#cb_add")
        await pilot.pause()

        # Verify it was added to the table
        cb_manager.action_switch_to_table()
        await pilot.pause()
        assert cb_manager.query_one(CuttingBoardTable).row_count == 4

        # Save the current state
        await pilot.press("ctrl+s")
        await pilot.pause()
        app_to_save.screen.query_one("#path_input", Input).value = config_path
        await pilot.click("#confirm")
        await pilot.pause()

    # Now load it in a new app instance
    app_to_load = CuttingBoardDrawersOptimizerApp()
    async with app_to_load.run_test() as pilot:
        await pilot.press("ctrl+o")
        await pilot.pause()

        assert isinstance(app_to_load.screen, LoadDialog)
        app_to_load.screen.query_one("#path_input", Input).value = config_path
        await pilot.click("#open")
        await pilot.pause()

        # Verify data is loaded
        cb_manager = app_to_load.query_one(CuttingBoardManager)
        table = cb_manager.query_one(CuttingBoardTable)
        # 3 default + 1 loaded
        assert table.row_count == 4
        assert table.get_row_at(3)[0] == "Load Me"


@pytest.mark.asyncio
async def test_app_tab_switching():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        # Initial tab
        tabs = app.query_one("#tabs", TabbedContent)
        assert tabs.active == "cutting_boards"

        # Switch to drawers via keybind
        await pilot.press("d")
        await pilot.pause()
        assert tabs.active == "drawers"

        # Switch back to cutting boards via keybind
        await pilot.press("c")
        await pilot.pause()
        assert tabs.active == "cutting_boards"
