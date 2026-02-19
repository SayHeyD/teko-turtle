import pytest
from unittest.mock import patch, PropertyMock
from cutting_board_drawers_optimizer.ui.app import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.ui.cutting_board_table import CuttingBoardTable


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
        table.add_row("Bad Row", "not a number", "10", "10", "10", "0")
        data = table.get_current_data()
        # Should skip the bad row
        assert len(data) == 3
        for item in data:
            assert item.get_name() != "Bad Row"
