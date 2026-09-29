"""Re-opt bonus + bonus_4 LUTs to 96% RTP after cost change (200 / 160)."""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    rust_threads = 20
    # Books already exist — only re-weight LUTs for modes whose cost changed
    target_modes = ["bonus", "bonus_4"]

    config = GameConfig()
    gamestate = GameState(config)
    OptimizationSetup(config)
    generate_configs(gamestate)

    print("Re-optimizing modes:", target_modes)
    print("Costs:", {bm.get_name(): bm.get_cost() for bm in config.bet_modes if bm.get_name() in target_modes})
    OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
    generate_configs(gamestate)
    print("Done — check lookUpTable_bonus_0.csv and lookUpTable_bonus_4_0.csv RTP")
