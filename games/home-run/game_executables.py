from game_calculations import GameCalculations
from src.calculations.lines import Lines


class GameExecutables(GameCalculations):

    def evaluate_lines_board(self):
        """Calcule les gains lignes ; les multis des balles wild se multiplient entre eux."""
        self.win_data = Lines.get_lines(
            self.board,
            self.config,
            global_multiplier=self.global_multiplier,
            multiplier_method="symbol_product",
        )
        Lines.record_lines_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        Lines.emit_linewin_events(self)
