import os
import pytest
from unittest.mock import MagicMock, patch
from textual.widgets import TabbedContent, Input
from cutting_board_drawers_optimizer.ui.save_dialog import SaveDialog
from cutting_board_drawers_optimizer.ui.load_dialog import LoadDialog
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.state.state import State


@pytest.mark.asyncio
async def test_app_init():
    """Test the CuttingBoardDrawersOptimizerApp constructor."""
    app = CuttingBoardDrawersOptimizerApp()
    # Verify that the state is initialized
    assert isinstance(app._state, State)
    # Verify that _last_path is initialized to None
    assert app._last_path is None


@pytest.mark.asyncio
async def test_that_app_shows_correct_header_content():
    from textual.widgets import Header

    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test():
        header = app.query_one(Header)
        assert header.icon == "🔪"
        assert header._show_clock is True
        assert header.screen_title == "Cutting Board Drawers Optimizer"


@pytest.mark.asyncio
async def test_that_app_has_footer():
    from textual.widgets import Footer

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
    from cutting_board_drawers_optimizer.ui.create_cutting_board import CreateCuttingBoard
    from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable

    # First create a config file
    config_path = str(tmp_path / "load_test.json")
    app_to_save = CuttingBoardDrawersOptimizerApp()
    async with app_to_save.run_test() as pilot:
        # Add a custom item to verify it's loaded later
        cb_manager = app_to_save.query_one(CuttingBoardManager)
        cb_manager.action_switch_to_create_tab()
        await pilot.pause()
        create_cb = app_to_save.query_one(CreateCuttingBoard)
        create_cb.query_one("#cb_name", Input).focus()
        await pilot.press(*"Load Me")
        create_cb.query_one("#cb_length", Input).focus()
        await pilot.press(*"10")
        create_cb.query_one("#cb_width", Input).focus()
        await pilot.press(*"10")
        create_cb.query_one("#cb_weight", Input).focus()
        await pilot.press(*"10")
        create_cb.query_one("#cb_price", Input).focus()
        await pilot.press(*"10")
        await pilot.press("enter")
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


@pytest.mark.asyncio
async def test_app_tab_activation_focus():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        # Initially, the first tab is active
        tabs = app.query_one("#tabs", TabbedContent)
        assert tabs.active == "cutting_boards"
        # Switch to drawers tab via pilot to trigger events naturally
        await pilot.press("d")
        await pilot.pause()
        assert tabs.active == "drawers"

        mock_event = MagicMock()
        mock_event.tabbed_content.id = "tabs"
        # Test cutting_boards focus
        mock_event.tab.id = "cutting_boards"
        cb_manager = app.query_one(CuttingBoardManager)
        with patch.object(cb_manager, "focus") as mock_focus:
            app.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()
        # Test drawers focus
        mock_event.tab.id = "drawers"
        dr_manager = app.query_one(DrawerManager)
        with patch.object(dr_manager, "focus") as mock_focus:
            app.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()


@pytest.mark.asyncio
async def test_app_save_config_cancel():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("ctrl+s")
        await pilot.pause()
        assert isinstance(app.screen, SaveDialog)
        # Click cancel
        await pilot.click("#cancel")
        await pilot.pause()
        # Should be back to main screen
        assert not isinstance(app.screen, SaveDialog)
        assert app._last_path is None


@pytest.mark.asyncio
async def test_app_save_config_error(tmp_path):
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        save_path = str(tmp_path / "error_test.json")
        await pilot.press("ctrl+s")
        await pilot.pause()
        app.screen.query_one("#path_input", Input).value = save_path
        # Simulate OSError during save
        with patch.object(app._state, "save", side_effect=OSError("Disk full")):
            await pilot.click("#confirm")
            await pilot.pause()
        # Verify it didn't crash and didn't update last_path
        assert app._last_path is None


@pytest.mark.asyncio
async def test_app_load_config_cancel():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("ctrl+o")
        await pilot.pause()
        assert isinstance(app.screen, LoadDialog)
        # Click cancel
        await pilot.click("#cancel")
        await pilot.pause()
        assert not isinstance(app.screen, LoadDialog)
        assert app._last_path is None


@pytest.mark.asyncio
async def test_app_load_config_error(tmp_path):
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("ctrl+o")
        await pilot.pause()
        app.screen.query_one("#path_input", Input).value = "non_existent.json"
        # Simulate FileNotFoundError
        with patch.object(app._state, "load", side_effect=FileNotFoundError()):
            await pilot.click("#open")
            await pilot.pause()
        assert app._last_path is None


@pytest.mark.asyncio
async def test_app_save_config_overwrite(tmp_path):
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        save_path = str(tmp_path / "overwrite.json")
        # Create the file first
        with open(save_path, "w") as f:
            f.write("{}")
        await pilot.press("ctrl+s")
        await pilot.pause()
        app.screen.query_one("#path_input", Input).value = save_path
        await pilot.click("#confirm")
        await pilot.pause()
        assert os.path.exists(save_path)
