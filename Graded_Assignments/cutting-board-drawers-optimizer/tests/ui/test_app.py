import os
from unittest.mock import MagicMock, patch, PropertyMock
import pytest
from textual.widgets import Input, TabbedContent
from cutting_board_drawers_optimizer.ui.save_dialog import SaveDialog
from cutting_board_drawers_optimizer.ui.load_dialog import LoadDialog
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable
from cutting_board_drawers_optimizer.state.state import State

from textual.widgets import Header, Footer

from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp


def test_app_init():
    """Test the CuttingBoardDrawersOptimizerApp constructor."""
    app = CuttingBoardDrawersOptimizerApp()

    # Verify that the state is initialized
    assert isinstance(app._state, State)

    # Verify that _last_path is initialized to None
    assert app._last_path is None


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

        # Instead of checking app.focused (which might be delegated deeper),
        # we can verify the method was called or check the intermediate state.
        # But wait, if I want to test on_tabbed_content_tab_activated specifically,
        # I can just call it with a mock event.

        from unittest.mock import MagicMock, patch, PropertyMock

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

        # Test irrelevant tab activation (no focus call)
        mock_event.tabbed_content.id = "other"
        with patch.object(cb_manager, "focus") as mock_focus:
            app.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_not_called()


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
