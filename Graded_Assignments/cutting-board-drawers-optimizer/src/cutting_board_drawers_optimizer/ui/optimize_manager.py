from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import (
    Button,
    Input,
    Label,
    Static,
    Tree,
)

from cutting_board_drawers_optimizer.optimizer import Optimizer
from cutting_board_drawers_optimizer.ui.cutting_board_manager import CuttingBoardManager
from cutting_board_drawers_optimizer.ui.drawer_manager import DrawerManager
from cutting_board_drawers_optimizer.ui.validator import Validator


class OptimizeManager(Widget):
    """Manager widget for optimization calculations."""

    def compose(self) -> ComposeResult:
        """Compose the OptimizeManager UI."""
        with Vertical(id="optimize_form"):
            yield Label("Optimization Settings")
            yield Label("Budget (CHF)")
            yield Input(placeholder="Budget", id="opt_budget")
            yield Label("Amount of Cutting Boards")
            yield Input(placeholder="Amount of Cutting Boards", id="opt_amount")
            yield Label("", id="opt_error", classes="error")
            yield Button("Confirm", id="opt_confirm", variant="primary")
            yield Static("Optimization Result:", id="opt_result_label")
            yield Tree("Results", id="opt_result_tree")

    def on_mount(self) -> None:
        """Initialize UI elements on mount."""
        error_label = self.query_one("#opt_error", Label)
        error_label.display = False

        result_label = self.query_one("#opt_result_label", Static)
        result_label.display = False

        tree = self.query_one("#opt_result_tree", Tree)
        tree.display = False
        tree.root.expand()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the confirm button press."""
        if event.button.id == "opt_confirm":
            budget_str = self.query_one("#opt_budget", Input).value.strip()
            amount_str = self.query_one("#opt_amount", Input).value.strip()

            error_label = self.query_one("#opt_error", Label)
            errors = []

            for val, label in [
                (budget_str, "Budget"),
                (amount_str, "Amount of Cutting Boards"),
            ]:
                valid, err = Validator.is_positive_number(val, label)
                if not valid and err is not None:
                    errors.append(err)

            if errors:
                error_label.update(" ".join(errors))
                error_label.display = True
            else:
                error_label.update("")
                error_label.display = False
                self.__run_optimization(budget_str, amount_str)

    def __run_optimization(self, budget_str: str, amount_str: str) -> None:
        """Run the optimization and display results."""
        from cutting_board_drawers_optimizer.ui.app import CuttingBoardDrawersOptimizerApp

        app = self.app
        if not isinstance(app, CuttingBoardDrawersOptimizerApp):
            return

        cb_manager = app.query_one(CuttingBoardManager)
        dr_manager = app.query_one(DrawerManager)

        drawers = dr_manager.get_current_data()
        cutting_boards = cb_manager.get_current_data()

        budget_cents = int(float(budget_str) * 100)
        amount = int(float(amount_str))

        optimizer = Optimizer(drawers, cutting_boards, budget_cents, amount)
        result = optimizer.optimize()

        self.__display_results(result)

    def __display_results(self, result: dict) -> None:
        """Display the optimization results in the Tree."""
        tree = self.query_one("#opt_result_tree", Tree)
        result_label = self.query_one("#opt_result_label", Static)

        tree.clear()
        any_assigned = False

        for drawer, boards in result.items():
            if boards:
                any_assigned = True
                total_area = sum(b.area for b in boards)
                total_weight = sum(b.get_weight_in_grams() for b in boards)
                total_cost_cents = sum(b.get_price_in_centime() for b in boards)
                total_cost_chf = f"{total_cost_cents / 100:.2f}"

                drawer_node = tree.root.add(
                    f"[bold]{drawer.get_name()}[/bold] (Area: {total_area}, Weight: {total_weight}, Cost: {total_cost_chf} CHF)",
                    expand=True,
                )
                for board in boards:
                    drawer_node.add_leaf(
                        f"{board.get_name()} (Area: {board.area}, Weight: {board.get_weight_in_grams()}, Price: {board.get_price_in_chf()} CHF)"
                    )

        if not any_assigned:
            result_label.update("No cutting boards could be assigned with the given constraints.")
            tree.display = False
        else:
            result_label.update("Optimization Result:")
            tree.display = True

        result_label.display = True

    def on_input_submitted(self) -> None:
        """Handle input submission (pressing Enter)."""
        # Trigger the same logic as clicking "Confirm"
        self.on_button_pressed(Button.Pressed(self.query_one("#opt_confirm", Button)))
