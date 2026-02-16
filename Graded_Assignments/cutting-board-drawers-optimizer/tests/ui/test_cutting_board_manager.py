import pytest
from textual.widgets import TabbedContent, Input
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable
from unittest.mock import MagicMock, patch
from cutting_board_drawers_optimizer.optimizer import CuttingBoard
from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp


@pytest.mark.asyncio
async def test_cutting_board_manager_initial_population():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        table = manager.query_one(CuttingBoardTable)
        # 3 initial rows
        assert table.row_count == 3
        assert len(table.columns) == 5


@pytest.mark.asyncio
async def test_cutting_board_manager_add_item():
    from cutting_board_drawers_optimizer.ui.create_cutting_board import CreateCuttingBoard
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        # Switch to cutting boards tab (it should be active by default, but let's be sure)
        app.action_show_tab("cutting_boards")
        await pilot.pause()

        # Switch to create tab inside manager
        manager.action_switch_to_create_tab()
        await pilot.pause()

        tabs = manager.query_one("#cb_tabs", TabbedContent)
        assert tabs.active == "create_tab"

        create_cb = manager.query_one(CreateCuttingBoard)
        # Fill form
        create_cb.query_one("#cb_name", Input).focus()
        await pilot.press(*"Test Board")
        create_cb.query_one("#cb_length", Input).focus()
        await pilot.press(*"50")
        create_cb.query_one("#cb_width", Input).focus()
        await pilot.press(*"40")
        create_cb.query_one("#cb_weight", Input).focus()
        await pilot.press(*"1000")
        create_cb.query_one("#cb_price", Input).focus()
        await pilot.press(*"25.50")

        # Click Add
        await pilot.press("enter")
        await pilot.pause()

        # Should switch back to table tab
        assert tabs.active == "table_tab"

        # Table should have new row
        table = manager.query_one(CuttingBoardTable)
        assert table.row_count == 4
        assert table.get_row_at(3)[0] == "Test Board"


@pytest.mark.asyncio
async def test_cutting_board_manager_add_item_via_enter():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        app.action_show_tab("cutting_boards")
        await pilot.pause()

        # Switch to create tab
        manager.action_switch_to_create_tab()
        await pilot.pause()

        # Fill form
        await pilot.click("#cb_name")
        await pilot.press("E", "n", "t", "e", "r", " ", "B", "o", "a", "r", "d")
        await pilot.click("#cb_length")
        await pilot.press("1", "0")
        await pilot.click("#cb_width")
        await pilot.press("1", "0")
        await pilot.click("#cb_weight")
        await pilot.press("1", "0", "0")
        await pilot.click("#cb_price")
        await pilot.press("5")

        # Press Enter
        await pilot.press("enter")
        await pilot.pause()

        # Should switch back to table tab
        tabs = manager.query_one("#cb_tabs", TabbedContent)
        assert tabs.active == "table_tab"

        # Table should have new row
        table = manager.query_one(CuttingBoardTable)
        assert table.row_count == 4
        assert table.get_row_at(3)[0] == "Enter Board"


@pytest.mark.asyncio
async def test_cutting_board_manager_delete_item():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        table = manager.query_one(CuttingBoardTable)
        initial_count = table.row_count

        # Focus table and delete first row
        table.focus()
        await pilot.press("ctrl+d")
        await pilot.pause()

        assert table.row_count == initial_count - 1


@pytest.mark.asyncio
async def test_cutting_board_manager_data_methods():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        data = manager.get_current_data()
        assert len(data) == 3
        assert isinstance(data[0], CuttingBoard)

        new_data = [CuttingBoard("New CB", 10, 20, 300, 1500)]
        manager.update_from_data(new_data)
        await pilot.pause()

        table = manager.query_one(CuttingBoardTable)
        assert table.row_count == 1
        assert table.get_row_at(0)[0] == "New CB"


@pytest.mark.asyncio
async def test_cutting_board_manager_tab_activation_branches():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        mock_event = MagicMock()
        mock_event.tabbed_content.id = "cb_tabs"

        # Test table_tab
        mock_event.tab.id = "table_tab"
        with patch.object(manager.query_one(CuttingBoardTable), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()

        # Test create_tab
        mock_event.tab.id = "create_tab"
        with patch.object(manager.query_one("#cb_name", Input), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()

        # Test irrelevant tab
        mock_event.tab.id = "other"
        with patch.object(manager.query_one(CuttingBoardTable), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_not_called()

        # Test irrelevant tabbed content
        mock_event.tabbed_content.id = "other_tabs"
        with patch.object(manager.query_one(CuttingBoardTable), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_not_called()
