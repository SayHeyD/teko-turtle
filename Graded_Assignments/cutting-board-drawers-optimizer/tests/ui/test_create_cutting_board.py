import pytest
from unittest.mock import MagicMock, patch
from textual.widgets import Label, Button, Input
from cutting_board_drawers_optimizer.ui.create_cutting_board import CreateCuttingBoard
from cutting_board_drawers_optimizer.ui.app import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable


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

        from textual.widgets import TabbedContent

        tabs = manager.query_one("#cb_tabs", TabbedContent)

        # 1. Test empty fields -> should not add, stay on create, show error
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


@pytest.mark.asyncio
async def test_clear_inputs_after_adding_cutting_board():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        cb_manager = app.query_one(CuttingBoardManager)
        cb_manager.action_switch_to_create_tab()
        await pilot.pause()

        create_cb = cb_manager.query_one(CreateCuttingBoard)

        # Fill form
        create_cb.query_one("#cb_name", Input).value = "Test Board"
        create_cb.query_one("#cb_length", Input).value = "50"
        create_cb.query_one("#cb_width", Input).value = "40"
        create_cb.query_one("#cb_weight", Input).value = "1000"
        create_cb.query_one("#cb_price", Input).value = "25.50"

        # Click Add (via enter on button or just submitted message)
        create_cb.query_one("#cb_add", Button).focus()
        await pilot.press("enter")
        await pilot.pause()

        # Switch back to create tab to check inputs
        cb_manager.action_switch_to_create_tab()
        await pilot.pause()

        # Verify inputs are cleared
        assert create_cb.query_one("#cb_name", Input).value == ""
        assert create_cb.query_one("#cb_length", Input).value == ""
        assert create_cb.query_one("#cb_width", Input).value == ""
        assert create_cb.query_one("#cb_weight", Input).value == ""
        assert create_cb.query_one("#cb_price", Input).value == ""
