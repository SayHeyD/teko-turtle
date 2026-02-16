import pytest
from textual.widgets import TabbedContent, Input, DataTable, Label
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable
from unittest.mock import MagicMock, patch, PropertyMock
from cutting_board_drawers_optimizer.ui.create_cutting_board import CreateCuttingBoard
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
async def test_cutting_board_table_delete_no_selection():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        table = app.query_one(CuttingBoardTable)
        # Mock cursor_row as None to test branch
        with patch.object(CuttingBoardTable, "cursor_row", new_callable=PropertyMock, return_value=None):
            initial_count = table.row_count
            table.action_delete_current_row()
            assert table.row_count == initial_count


@pytest.mark.asyncio
async def test_cutting_board_table_invalid_data_parsing():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        table = app.query_one(CuttingBoardTable)
        # Add a row with invalid data
        table.add_row("Bad Row", "not a number", "10", "10", "10")
        data = table.get_current_data()
        # Should skip the bad row
        assert len(data) == 3
        for item in data:
            assert item.get_name() != "Bad Row"


@pytest.mark.asyncio
async def test_create_cutting_board_wrong_button():
    # This covers on_button_pressed branch if event.button.id != "cb_add"
    widget = CreateCuttingBoard()
    mock_event = MagicMock()
    mock_event.button.id = "other_id"
    # Should not post Created message
    with patch.object(widget, "post_message") as mock_post:
        widget.on_button_pressed(mock_event)
        mock_post.assert_not_called()


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


@pytest.mark.asyncio
async def test_create_cutting_board_validation():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        table = manager.query_one(CuttingBoardTable)
        initial_rows = table.row_count

        # Navigate to Cutting Boards -> Create
        await pilot.press("c")
        manager.action_switch_to_create_tab()
        await pilot.pause()

        create_cb = app.query_one(CreateCuttingBoard)
        error_label = create_cb.query_one("#cb_error", Label)
        tabs = manager.query_one("#cb_tabs", TabbedContent)

        # 1. Test empty fields -> should not add, stay on create, show error
        # Use key presses instead of click to avoid potential focus issues with pilot.click
        await pilot.press("tab", "tab", "tab", "tab", "tab", "enter")
        await pilot.pause()
        assert error_label.visible is True
        assert tabs.active == "create_tab"
        assert table.row_count == initial_rows

        # 2. Test invalid numeric values -> still error
        create_cb.query_one("#cb_name", Input).value = "Valid Name"
        create_cb.query_one("#cb_length", Input).value = "abc"
        create_cb.query_one("#cb_width", Input).value = "-10"
        create_cb.query_one("#cb_weight", Input).value = "0"
        create_cb.query_one("#cb_price", Input).value = "foo"
        await pilot.press("enter")
        await pilot.pause()
        assert error_label.visible is True
        assert tabs.active == "create_tab"
        assert table.row_count == initial_rows

        # 3. Test valid values -> should add, switch to table, hide error
        create_cb.query_one("#cb_length", Input).value = "50"
        create_cb.query_one("#cb_width", Input).value = "40"
        create_cb.query_one("#cb_weight", Input).value = "1000"
        create_cb.query_one("#cb_price", Input).value = "25.50"
        await pilot.press("enter")
        await pilot.pause()
        assert error_label.visible is False
        assert tabs.active == "table_tab"
        assert table.row_count == initial_rows + 1
