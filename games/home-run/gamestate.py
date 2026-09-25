"""HOME RUN - logique d'une manche."""

import math
from game_override import GameStateOverride
from src.events.events import *


class GameState(GameStateOverride):
    """Logique d'une manche HOME RUN."""

    def run_spin(self, sim, simulation_seed=None):
        """Tire un crash et calcule le gain."""
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()

            # 1. Tirage du crash selon P(C >= x) = RTP / x
            crash = self._draw_crash()

            # 2. Calcul du gain (mode courant, doc §2)
            mode = self.get_current_betmode()
            mode_name = mode.get_name()

            if mode_name == "base" or "_" not in mode_name:
                target = 2.00
                secure = 0.0
            else:
                parts = mode_name.split("_")
                target = int(parts[0][1:]) / 100.0
                secure = int(parts[1][1:]) / 100.0

            win = 0.0
            if secure > 0 and crash >= 2.00:
                win += secure * 2.00
            if crash >= target:
                win += (1 - secure) * target
            win = min(win, mode.get_wincap())

            win_data = {"totalWin": win}

            self.win_manager.update_spinwin(win_data["totalWin"])
            self.win_manager.update_gametype_wins(self.gametype)

            # 3. On écrit les événements dans le book
            #    (crash + gain, ce que le front va lire)
            crash_event = {
                "index": len(self.book.events),
                "type": EventConstants.WIN_DATA.value,
                "crash": int(round(crash * 100, 0)),
                "totalWin": int(round(win_data["totalWin"] * 100, 0)),
            }
            self.book.add_event(crash_event)

            self.evaluate_finalwin()

        self.imprint_wins()

    def _draw_crash(self):
        """Tire un crash selon la loi P(C >= x) = 0.965 / x.

        Retourne une valeur entre 1.01 et 1 000 000.
        """
        import random
        r = random.random()  # entre 0 et 1
        if r < 0.035:
            return 1.00
        return 0.965 / r

    def run_freespin(self):
        pass
