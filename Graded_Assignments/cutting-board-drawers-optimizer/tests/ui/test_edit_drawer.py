import pytest
from textual.widgets import TabbedContent
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
        assert app.query_one("#de_name").value == "Main Kitchen Drawer"
        assert app.query_one("#de_length").value == "60"
        assert app.query_one("#de_width").value == "50"
        assert app.query_one("#de_max_load").value == "10000"

        # Edit values
        await pilot.click("#de_name")
        # Clear and type new name
        await pilot.press("home", "shift+end", "delete")
        await pilot.press("U", "p", "d", "a", "t", "e", "d", " ", "D", "r", "a", "w", "e", "r")

        await pilot.click("#de_length")
        await pilot.press("home", "shift+end", "delete")
        await pilot.press("7", "5")

        # Click Save
        await pilot.click("#de_save")
        await pilot.pause()

        # Should switch back to table tab
        assert tabs.active == "table_tab"

        # Table should have updated row
        assert table.get_row_at(0)[0] == "Updated Drawer"
        assert table.get_row_at(0)[1] == "75"
