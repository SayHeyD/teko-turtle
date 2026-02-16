import pytest
from unittest.mock import MagicMock, patch
from textual.widgets import Label, Button, Input, TabbedContent
from cutting_board_drawers_optimizer.ui.create_drawer import CreateDrawer
from cutting_board_drawers_optimizer.ui.app import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.drawer_table import DrawerTable

@pytest.mark.asyncio
async def test_create_drawer_wrong_button():
    # This covers on_button_pressed branch if event.button.id != "d_add"
    widget = CreateDrawer()
    mock_event = MagicMock()
    mock_event.button.id = "other_id"
    # Should not post Created message
    with patch.object(widget, "post_message") as mock_post:
        widget.on_button_pressed(mock_event)
        mock_post.assert_not_called()

@pytest.mark.asyncio
async def test_create_drawer_validation():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        table = manager.query_one(DrawerTable)
        initial_rows = table.row_count

        # Navigate to Drawers -> Create
        await pilot.press("d")
        # Ensure the top-level Drawers tab is active in headless mode
        app.action_show_tab("drawers")
        manager.action_switch_to_create_tab()
        await pilot.pause()

        create_dr = app.query_one(CreateDrawer)
        error_label = create_dr.query_one("#d_error", Label)
        tabs = manager.query_one("#drawer_tabs", TabbedContent)

        # 1. Test empty fields
        create_dr.query_one("#d_add", Button).focus()
        await pilot.press("enter")
        await pilot.pause()
        assert error_label.visible is True
        assert tabs.active == "create_tab"
        assert table.row_count == initial_rows

        # 2. Test invalid numeric values
        create_dr.query_one("#d_name", Input).value = "Valid Name"
        create_dr.query_one("#d_length", Input).value = "abc"
        create_dr.query_one("#d_width", Input).value = "-10"
        create_dr.query_one("#d_max_load", Input).value = "foo"
        create_dr.query_one("#d_add", Button).focus()
        await pilot.press("enter")
        await pilot.pause()
        assert error_label.visible is True
        assert tabs.active == "create_tab"
        assert table.row_count == initial_rows

        # 3. Test valid values
        create_dr.query_one("#d_name", Input).value = "Valid Name"
        create_dr.query_one("#d_length", Input).value = "60"
        create_dr.query_one("#d_width", Input).value = "50"
        create_dr.query_one("#d_max_load", Input).value = "10000"
        # Submit via Enter on the last input to trigger on_input_submitted reliably
        create_dr.query_one("#d_max_load", Input).focus()
        await pilot.press("enter")
        # Allow UI to process Created message and tab switch
        await pilot.pause()
        # Verify that the form was accepted by checking inputs were cleared.
        assert create_dr.query_one("#d_name", Input).value == ""
        assert create_dr.query_one("#d_length", Input).value == ""
        assert create_dr.query_one("#d_width", Input).value == ""
        assert create_dr.query_one("#d_max_load", Input).value == ""

@pytest.mark.asyncio
async def test_clear_inputs_after_adding_drawer():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        # Switch to drawers tab
        await pilot.press("d")
        await pilot.pause()

        dr_manager = app.query_one(DrawerManager)
        dr_manager.action_switch_to_create_tab()
        await pilot.pause()

        create_dr = dr_manager.query_one(CreateDrawer)
        
        # Fill form
        create_dr.query_one("#d_name", Input).value = "Test Drawer"
        create_dr.query_one("#d_length", Input).value = "60"
        create_dr.query_one("#d_width", Input).value = "50"
        create_dr.query_one("#d_max_load", Input).value = "10000"

        # Press Enter
        create_dr.query_one("#d_add", Button).focus()
        await pilot.press("enter")
        await pilot.pause()

        # Switch back to create tab to check inputs
        dr_manager.action_switch_to_create_tab()
        await pilot.pause()

        # Verify inputs are cleared
        assert create_dr.query_one("#d_name", Input).value == ""
        assert create_dr.query_one("#d_length", Input).value == ""
        assert create_dr.query_one("#d_width", Input).value == ""
        assert create_dr.query_one("#d_max_load", Input).value == ""
