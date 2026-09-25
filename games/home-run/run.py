"""HOME RUN — génération des books."""

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    num_threads = 1
    batching_size = 50000
    compression = True
    profiling = False

    # Nombre de simulations par mode.
    # Pour un premier test : 10 000 par mode.
    # Pour la production : ~46 695 par mode (une par crash).
    SIMS_PER_MODE = int(1e4)

    # On construit les 66 modes depuis la config
    config = GameConfig()
    num_sim_args = {mode._name: SIMS_PER_MODE for mode in config.bet_modes}

    run_conditions = {"run_sims": True}

    gamestate = GameState(config)

    if run_conditions["run_sims"]:
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )
    generate_configs(gamestate)