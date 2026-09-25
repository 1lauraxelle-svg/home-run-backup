"""HOME RUN - configuration du jeu."""

from src.config.config import Config
from src.config.distributions import Distribution
from src.config.config import BetMode


TARGETS_OFF = [1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.20, 2.50, 3.00,
               3.50, 4.00, 5.00, 6.00, 7.00, 8.00, 10.00, 12.00, 15.00,
               20.00, 25.00, 30.00, 35.00]

TARGETS_50 = [3.00, 4.00, 5.00, 6.00, 8.00, 10.00, 12.00, 15.00, 20.00,
              25.00, 30.00, 40.00, 50.00, 75.00, 100.00, 150.00, 200.00,
              250.00, 500.00, 750.00, 1000.00, 1500.00, 2000.00, 2500.00,
              5000.00, 7500.00, 10000.00]

TARGETS_90 = [1000.00, 1500.00, 2000.00, 2500.00, 5000.00, 7500.00,
              10000.00, 15000.00, 20000.00, 25000.00, 50000.00, 75000.00,
              100000.00, 150000.00, 200000.00, 250000.00]


class GameConfig(Config):
    """Configuration HOME RUN."""

    def __init__(self):
        super().__init__()
        self.game_id = "home-run"
        self.provider_numer = 0
        self.working_name = "home-run"
        self.wincap = 25000
        self.win_type = "other"
        self.rtp = 0.965

        self.num_reels = 0
        self.num_rows = [0] * self.num_reels
        self.paytable = {}
        self.include_padding = False
        self.special_symbols = {"wild": [], "scatter": [], "multiplier": []}

        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 0, self.freegame_type: 0}

        self.bet_modes = []
        self.bet_modes += self._build_modes(TARGETS_OFF, secure=0.0)
        self.bet_modes += self._build_modes(TARGETS_50, secure=0.5)
        self.bet_modes += self._build_modes(TARGETS_90, secure=0.9)
        # Mode bidon pour le SDK (il cherche toujours "base")
        self.bet_modes.append(
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="basegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            )
        )

    def _build_modes(self, targets, secure):
        modes = []
        for target in targets:
            mode_name = f"t{int(round(target * 100))}_s{int(secure * 100)}"
            modes.append(
                BetMode(
                    name=mode_name,
                    cost=1.0,
                    rtp=self.rtp,
                    max_win=self.wincap,
                    auto_close_disabled=False,
                    is_feature=False,
                    is_buybonus=False,
                    distributions=[
                        Distribution(
                            criteria="basegame",
                            quota=1.0,
                            conditions={
                                "reel_weights": {},
                                "force_wincap": False,
                                "force_freegame": False,
                            },
                        ),
                    ],
                )
            )
        return modes