from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import (
    Button,
    Input,
    Label,
)

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

    def on_mount(self) -> None:
        """Hide the error label on mount."""
        error_label = self.query_one("#opt_error", Label)
        error_label.display = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the confirm button press."""
        if event.button.id == "opt_confirm":
            budget = self.query_one("#opt_budget", Input).value.strip()
            amount = self.query_one("#opt_amount", Input).value.strip()

            error_label = self.query_one("#opt_error", Label)
            errors = []

            for val, label in [
                (budget, "Budget"),
                (amount, "Amount of Cutting Boards"),
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
                # For now it shouldn't do anything
                self.log(f"Optimization requested: Budget={budget}, Amount={amount}")

    def on_input_submitted(self) -> None:
        """Handle input submission (pressing Enter)."""
        # Trigger the same logic as clicking "Confirm"
        self.on_button_pressed(Button.Pressed(self.query_one("#opt_confirm", Button)))
