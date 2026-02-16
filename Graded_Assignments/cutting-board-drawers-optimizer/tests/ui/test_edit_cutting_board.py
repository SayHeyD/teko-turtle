import pytest
from textual.widgets import TabbedContent
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable
from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp


@pytest.mark.asyncio
async def test_cutting_board_manager_edit_item():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(CuttingBoardManager)
        # Switch to cutting boards tab (it's default, but let's be explicit)
        app.action_show_tab("cutting_boards")
        await pilot.pause()

        table = manager.query_one(CuttingBoardTable)
        tabs = manager.query_one("#cb_tabs", TabbedContent)

        # Focus table and ensure a row is selected
        table.focus()
        if table.cursor_row is None:
            await pilot.press("down")
            await pilot.pause()
        selected_index = table.cursor_row or 0
        expected_name = table.get_row_at(selected_index)[0]

        # Open edit for the selected row
        await pilot.press("ctrl+e")
        await pilot.pause()

        # Should switch to edit tab
        assert tabs.active == "edit_tab"
        
        # Check if the selected row's values are correctly populated
        assert app.query_one("#cbe_name").value == expected_name
        assert app.query_one("#cbe_length").value == "40"
        assert app.query_one("#cbe_width").value == "30"
        assert app.query_one("#cbe_weight").value == "2000"
        assert app.query_one("#cbe_price").value == "50.39"

        # Edit values
        await pilot.click("#cbe_name")
        # Clear and type new name
        await pilot.press("home", "shift+end", "delete")
        await pilot.press("U", "p", "d", "a", "t", "e", "d", " ", "C", "B")
        
        await pilot.click("#cbe_price")
        await pilot.press("home", "shift+end", "delete")
        await pilot.press("6", "0", ".", "0", "0")

        # Click Save
        await pilot.click("#cbe_save")
        await pilot.pause()

        # Table should have updated row
        assert table.get_row_at(0)[0] == "Updated CB"
        assert table.get_row_at(0)[4] == "60.00"
