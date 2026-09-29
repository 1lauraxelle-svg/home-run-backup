"""Paramètres d'optimisation RTP / hit-rate pour HOME RUN."""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    ConstructFenceBias,
    verify_optimization_input,
)


class OptimizationSetup:
    def __init__(self, game_config):
        self.game_config = game_config
        wincaps = {}
        for bm in game_config.bet_modes:
            wincaps[bm.get_name()] = bm.get_wincap()

        self.game_config.opt_params = {
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.001, av_win=wincaps["base"], search_conditions=wincaps["base"]
                    ).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.36, hr=200, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(hr=3.5, rtp=0.599).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 2), "probability": 1.0},
                        {"criteria": "basegame", "scale_factor": 1.5, "win_range": (10, 20), "probability": 1.0},
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.8,
                            "win_range": (1000, 5000),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.2,
                            "win_range": (5000, 15000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["basegame"],
                    bias_ranges=[(2.0, 3.0)],
                    bias_weights=[0.5],
                ).return_dict(),
            },
            "bonus": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.001, av_win=wincaps["bonus"], search_conditions=wincaps["bonus"]
                    ).return_dict(),
                    "freegame": ConstructConditions(rtp=0.959, hr="x").return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.2,
                            "win_range": (1, 20),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.5,
                            "win_range": (20, 50),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.8,
                            "win_range": (50, 100),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.8,
                            "win_range": (1000, 5000),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.2,
                            "win_range": (10000, 20000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["freegame"],
                    bias_ranges=[(200.0, 350.0)],
                    bias_weights=[0.3],
                ).return_dict(),
            },
        }

        # Clone params for extra buy / ante modes
        self.game_config.opt_params["ante"] = {
            "conditions": {
                "wincap": ConstructConditions(
                    rtp=0.001, av_win=wincaps["ante"], search_conditions=wincaps["ante"]
                ).return_dict(),
                "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                "freegame": ConstructConditions(
                    rtp=0.36, hr=100, search_conditions={"symbol": "scatter"}
                ).return_dict(),
                "basegame": ConstructConditions(hr=3.5, rtp=0.599).return_dict(),
            },
            "scaling": self.game_config.opt_params["base"]["scaling"],
            "parameters": self.game_config.opt_params["base"]["parameters"],
            "distribution_bias": self.game_config.opt_params["base"]["distribution_bias"],
        }
        for mode in ("bonus_3", "bonus_4"):
            self.game_config.opt_params[mode] = {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.001, av_win=wincaps[mode], search_conditions=wincaps[mode]
                    ).return_dict(),
                    "freegame": ConstructConditions(rtp=0.959, hr="x").return_dict(),
                },
                "scaling": self.game_config.opt_params["bonus"]["scaling"],
                "parameters": self.game_config.opt_params["bonus"]["parameters"],
                "distribution_bias": self.game_config.opt_params["bonus"]["distribution_bias"],
            }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
