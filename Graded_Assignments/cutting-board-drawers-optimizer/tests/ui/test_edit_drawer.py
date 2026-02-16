import pytest
from textual.widgets import Input, TabbedContent
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.drawer_table import DrawerTable
from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp


@pytest.mark.asyncio
async def test_drawer_manager_edit_item():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        manager = app.query_one(DrawerManager)
        # Switch to drawers tab
        app.action_show_tab("drawers")
        await pilot.pause()

        table = manager.query_one(DrawerTable)
        tabs = manager.query_one("#drawer_tabs", TabbedContent)

        # Select first row and press ctrl+e
        table.focus()
        await pilot.press("ctrl+e")
        await pilot.pause()

        # Should switch to edit tab
        assert tabs.active == "edit_tab"

        # Check if values are correctly populated
        assert app.query_one("#de_name", Input).value == "Main Kitchen Drawer"
        assert app.query_one("#de_length", Input).value == "60"
        assert app.query_one("#de_width", Input).value == "50"
        assert app.query_one("#de_max_load", Input).value == "10000"
        assert app.query_one("#de_max_boards", Input).value == "5"

        # Edit values programmatically
        app.query_one("#de_name", Input).value = "Updated Drawer"
        app.query_one("#de_length", Input).value = "75"
        await pilot.pause()

        # Submit save via Enter on the save button
        app.query_one("#de_save").focus()
        await pilot.press("enter")
        await pilot.pause()

        # Should switch back to table tab
        assert tabs.active == "table_tab"

        # Table should have updated row
        assert table.get_row_at(0)[0] == "Updated Drawer"
        assert table.get_row_at(0)[1] == "75"
