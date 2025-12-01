import pytest
from textual.widgets import Header, Footer

from cutting_board_drawers_optimizer.ui import CuttingBoardDrawersOptimizerApp

@pytest.mark.asyncio
async def test_that_app_shows_correct_header_content():
    app = CuttingBoardDrawersOptimizerApp()

    async with app.run_test():
        header = app.query_one(Header)
        assert header.icon == '🔪'
        assert header._show_clock is True
        assert header.screen_title == 'Cutting Board Drawers Optimizer'

@pytest.mark.asyncio
async def test_that_app_has_footer():
    app = CuttingBoardDrawersOptimizerApp()

    async with app.run_test():
        footer = app.query_one(Footer)
        assert footer is not None

