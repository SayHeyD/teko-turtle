import pytest
from textual.widgets import TabbedContent, Input
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.drawer_table import DrawerTable
from unittest.mock import MagicMock, patch
from cutting_board_drawers_optimizer.optimizer import Drawer
from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp


@pytest.mark.asyncio
async def test_drawer_manager_initial_population():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        table = manager.query_one(DrawerTable)
        # 2 initial rows
        assert table.row_count == 2
        assert len(table.columns) == 6


@pytest.mark.asyncio
async def test_drawer_manager_add_item():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        # Switch to drawers tab
        app.action_show_tab("drawers")
        await pilot.pause()

        # Switch to create tab
        manager.action_switch_to_create_tab()
        await pilot.pause()

        tabs = manager.query_one("#drawer_tabs", TabbedContent)
        assert tabs.active == "create_tab"

        # Fill form programmatically
        from cutting_board_drawers_optimizer.ui.create_drawer import CreateDrawer

        create_dr = manager.query_one(CreateDrawer)
        create_dr.query_one("#d_name", Input).value = "Test Drawer"
        create_dr.query_one("#d_length", Input).value = "80"
        create_dr.query_one("#d_width", Input).value = "60"
        create_dr.query_one("#d_max_load", Input).value = "20000"
        create_dr.query_one("#d_max_boards", Input).value = "8"

        # Click Add
        create_dr.query_one("#d_add").focus()
        await pilot.press("enter")
        await pilot.pause()

        # Table should have new row
        table = manager.query_one(DrawerTable)
        assert table.row_count == 3
        assert table.get_row_at(2)[0] == "Test Drawer"


@pytest.mark.asyncio
async def test_drawer_manager_add_item_via_enter():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        app.action_show_tab("drawers")
        await pilot.pause()

        # Switch to create tab
        manager.action_switch_to_create_tab()
        await pilot.pause()

        # Fill form
        await pilot.click("#d_name")
        await pilot.press("E", "n", "t", "e", "r", " ", "D", "r", "a", "w", "e", "r")
        await pilot.click("#d_length")
        await pilot.press("1", "0")
        await pilot.click("#d_width")
        await pilot.press("1", "0")
        await pilot.click("#d_max_load")
        await pilot.press("1", "0", "0")
        await pilot.click("#d_max_boards")
        await pilot.press("5")

        # Press Enter
        await pilot.press("enter")
        await pilot.pause()

        # Should switch back to table tab
        tabs = manager.query_one("#drawer_tabs", TabbedContent)
        assert tabs.active == "table_tab"

        # Table should have new row
        table = manager.query_one(DrawerTable)
        assert table.row_count == 3
        assert table.get_row_at(2)[0] == "Enter Drawer"


@pytest.mark.asyncio
async def test_drawer_manager_delete_item():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        table = manager.query_one(DrawerTable)
        initial_count = table.row_count

        # Focus table and delete first row
        table.focus()
        await pilot.press("ctrl+d")
        await pilot.pause()

        assert table.row_count == initial_count - 1


@pytest.mark.asyncio
async def test_drawer_manager_data_methods():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        data = manager.get_current_data()
        assert len(data) == 2
        assert isinstance(data[0], Drawer)

        new_data = [Drawer("New Drawer", 50, 40, 5000, 4)]
        manager.update_from_data(new_data)
        await pilot.pause()

        table = manager.query_one(DrawerTable)
        assert table.row_count == 1
        assert table.get_row_at(0)[0] == "New Drawer"


@pytest.mark.asyncio
async def test_drawer_manager_tab_activation_branches():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        mock_event = MagicMock()
        mock_event.tabbed_content.id = "drawer_tabs"

        # Test table_tab
        mock_event.tab.id = "table_tab"
        with patch.object(manager.query_one(DrawerTable), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()

        # Test create_tab
        mock_event.tab.id = "create_tab"
        with patch.object(manager.query_one("#d_name", Input), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()

        # Test irrelevant tab
        mock_event.tab.id = "other"
        with patch.object(manager.query_one(DrawerTable), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_not_called()

        # Test irrelevant tabbed content
        mock_event.tabbed_content.id = "other_tabs"
        with patch.object(manager.query_one(DrawerTable), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_not_called()
