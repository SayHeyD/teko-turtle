import pytest
from textual.widgets import Input, Label, Button, Tree, Static
from cutting_board_drawers_optimizer.ui.app import CuttingBoardDrawersOptimizerApp
from cutting_board_drawers_optimizer.ui.optimize_manager import OptimizeManager


@pytest.mark.asyncio
async def test_optimize_manager_inputs():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("o")
        await pilot.pause()

        manager = app.query_one(OptimizeManager)
        budget_input = manager.query_one("#opt_budget", Input)
        amount_input = manager.query_one("#opt_amount", Input)
        confirm_button = manager.query_one("#opt_confirm", Button)
        error_label = manager.query_one("#opt_error", Label)

        # Test valid inputs
        budget_input.focus()
        budget_input.value = "100"
        amount_input.value = "5"
        await pilot.press("enter")
        await pilot.pause()
        assert not error_label.display

        # Test invalid inputs
        budget_input.value = "abc"
        amount_input.value = "-1"
        await pilot.press("enter")
        await pilot.pause()
        assert error_label.display
        assert "Budget must be a number" in str(error_label.render())
        assert "Amount of Cutting Boards must be positive" in str(error_label.render())


@pytest.mark.asyncio
async def test_optimize_manager_calculation():
    app = CuttingBoardDrawersOptimizerApp()
    async with app.run_test() as pilot:
        await pilot.press("o")
        await pilot.pause()

        manager = app.query_one(OptimizeManager)
        budget_input = manager.query_one("#opt_budget", Input)
        amount_input = manager.query_one("#opt_amount", Input)
        tree = manager.query_one("#opt_result_tree", Tree)
        result_label = manager.query_one("#opt_result_label", Static)

        # Use default data (already in managers)
        budget_input.focus()
        budget_input.value = "1000"
        amount_input.value = "10"

        await pilot.press("enter")
        await pilot.pause()

        # Check if tree is displayed and has nodes
        assert tree.display is True
        assert result_label.display is True
        # Tree root + at least one drawer node
        assert len(tree.root.children) > 0
