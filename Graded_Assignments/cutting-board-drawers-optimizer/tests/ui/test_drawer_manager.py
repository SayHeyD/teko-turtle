import pytest
from textual.widgets import TabbedContent, Input
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.drawer_table import DrawerTable
from unittest.mock import MagicMock, patch, PropertyMock
from cutting_board_drawers_optimizer.ui.create_drawer import CreateDrawer
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
        assert len(table.columns) == 4


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

        # Fill form
        await pilot.click("#d_name")
        await pilot.press("T", "e", "s", "t", " ", "D", "r", "a", "w", "e", "r")
        await pilot.click("#d_length")
        await pilot.press("8", "0")
        await pilot.click("#d_width")
        await pilot.press("6", "0")
        await pilot.click("#d_max_load")
        await pilot.press("2", "0", "0", "0", "0")

        # Click Add
        await pilot.click("#d_add")
        await pilot.pause()

        # Should switch back to table tab
        assert tabs.active == "table_tab"

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

        new_data = [Drawer("New Drawer", 50, 50, 10000)]
        manager.update_from_data(new_data)
        await pilot.pause()

        table = manager.query_one(DrawerTable)
        assert table.row_count == 1
        assert table.get_row_at(0)[0] == "New Drawer"


@pytest.mark.asyncio
async def test_drawer_table_delete_no_selection():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        table = app.query_one(DrawerTable)
        # Mock cursor_row as None to test branch
        with patch.object(DrawerTable, "cursor_row", new_callable=PropertyMock, return_value=None):
            initial_count = table.row_count
            table.action_delete_current_row()
            assert table.row_count == initial_count


@pytest.mark.asyncio
async def test_drawer_table_invalid_data_parsing():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        table = app.query_one(DrawerTable)
        table.add_row("Bad Row", "not a number", "10", "10")
        data = table.get_current_data()
        assert len(data) == 2
        for item in data:
            assert item.get_name() != "Bad Row"


@pytest.mark.asyncio
async def test_create_drawer_wrong_button():
    widget = CreateDrawer()
    mock_event = MagicMock()
    mock_event.button.id = "other_id"
    with patch.object(widget, "post_message") as mock_post:
        widget.on_button_pressed(mock_event)
        mock_post.assert_not_called()


@pytest.mark.asyncio
async def test_drawer_manager_tab_activation_branches():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        mock_event = MagicMock()
        mock_event.tabbed_content.id = "drawer_tabs"

        mock_event.tab.id = "table_tab"
        with patch.object(manager.query_one(DrawerTable), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()

        mock_event.tab.id = "create_tab"
        with patch.object(manager.query_one("#d_name", Input), "focus") as mock_focus:
            manager.on_tabbed_content_tab_activated(mock_event)
            mock_focus.assert_called_once()

        # Coverage for irrelevant tab
        mock_event.tab.id = "irrelevant"
        manager.on_tabbed_content_tab_activated(mock_event)

        # Coverage for irrelevant tabbed content
        mock_event.tabbed_content.id = "irrelevant"
        manager.on_tabbed_content_tab_activated(mock_event)

@pytest.mark.asyncio
async def test_create_drawer_validation():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        table = manager.query_one(DrawerTable)
        initial_rows = table.row_count

        # Navigate to Drawers -> Create
        await pilot.press("d")
        manager.action_switch_to_create_tab()
        await pilot.pause()

        create_dr = app.query_one(CreateDrawer)
        error_label = create_dr.query_one("#d_error", Label)
        tabs = manager.query_one("#drawer_tabs", TabbedContent)

        # 1. Test empty fields -> should not add, stay on create, show error
        await pilot.click("#d_add")
        await pilot.pause()
        assert error_label.visible is True
        assert tabs.active == "create_tab"
        assert table.row_count == initial_rows

        # 2. Test invalid numeric values -> still error
        create_dr.query_one("#d_name", Input).value = "Valid Name"
        create_dr.query_one("#d_length", Input).value = "abc"
        create_dr.query_one("#d_width", Input).value = "-10"
        create_dr.query_one("#d_max_load", Input).value = "0"
        await pilot.click("#d_add")
        await pilot.pause()
        assert error_label.visible is True
        assert tabs.active == "create_tab"
        assert table.row_count == initial_rows

        # 3. Test valid values -> should add, switch to table, hide error
        create_dr.query_one("#d_length", Input).value = "60"
        create_dr.query_one("#d_width", Input).value = "50"
        create_dr.query_one("#d_max_load", Input).value = "10000"
        await pilot.click("#d_add")
        await pilot.pause()
        assert error_label.visible is False
        assert tabs.active == "table_tab"
        assert table.row_count == initial_rows + 1
