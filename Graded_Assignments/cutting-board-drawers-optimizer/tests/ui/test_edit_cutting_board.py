import pytest
from textual.widgets import Input, TabbedContent, Label
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable
from cutting_board_drawers_optimizer.ui.edit_cutting_board import EditCuttingBoard
from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp


@pytest.mark.asyncio
async def test_cutting_board_manager_edit_item():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        app.action_show_tab("cutting_boards")
        await pilot.pause()

        table = manager.query_one(CuttingBoardTable)
        tabs = manager.query_one("#cb_tabs", TabbedContent)

        # Focus table and ensure a row is selected
        table.focus()
        await pilot.pause()
        if table.cursor_row is None:
            await pilot.press("down")
            await pilot.pause()
        selected_index = table.cursor_row or 0
        expected_row = table.get_row_at(selected_index)

        # Open edit for the selected row
        await pilot.press("ctrl+e")
        await pilot.pause()

        # Should switch to edit tab
        assert tabs.active == "edit_tab"

        # Check if the selected row's values are correctly populated
        assert app.query_one("#cbe_name", Input).value == str(expected_row[0])
        assert app.query_one("#cbe_length", Input).value == str(expected_row[1]).replace(" cm", "")
        assert app.query_one("#cbe_width", Input).value == str(expected_row[2]).replace(" cm", "")
        assert app.query_one("#cbe_weight", Input).value == str(expected_row[3]).replace(" g", "")
        assert app.query_one("#cbe_price", Input).value == str(expected_row[4]).replace(" CHF", "")

        # Edit values programmatically (click+type is unreliable in headless mode)
        edit_form = manager.query_one(EditCuttingBoard)
        edit_form.query_one("#cbe_name", Input).value = "Updated CB"
        edit_form.query_one("#cbe_price", Input).value = "60.00"
        await pilot.pause()

        # Submit save via Enter on the save button
        edit_form.query_one("#cbe_save").focus()
        await pilot.press("enter")
        await pilot.pause()

        # Verify the row was updated
        row = table.get_row_at(selected_index)
        assert row[0] == "Updated CB"
        assert row[4] == "60.00 CHF"


@pytest.mark.asyncio
async def test_edit_cutting_board_invalid_data_and_enter():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        app.action_show_tab("cutting_boards")
        await pilot.pause()

        manager = app.query_one(CuttingBoardManager)
        tabs = manager.query_one("#cb_tabs", TabbedContent)
        # Force switch to edit tab
        tabs.active = "edit_tab"
        await pilot.pause()

        edit_cb = app.query_one(EditCuttingBoard)
        # Invalid data
        edit_cb.query_one("#cbe_name", Input).value = ""
        edit_cb.query_one("#cbe_length", Input).value = "-10"
        edit_cb.query_one("#cbe_price", Input).value = "invalid"

        # Focus name and press enter
        edit_cb.query_one("#cbe_name", Input).focus()
        await pilot.press("enter")
        await pilot.pause()

        error_label = edit_cb.query_one("#cbe_error", Label)
        assert error_label.visible is True
