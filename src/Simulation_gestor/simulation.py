from src.Simulation_Model.Game import Game
from src.Simulation_gestor.config_class import Config
from src.Llm.log_manager import LogManager


class Simulation:
    def __init__(self, config: Config, log_manager: LogManager):
        self._config = config
        self._simulations_results = []
        self._log_manager = log_manager

    def run(self):
        """Perform the simulation with the given configuration."""

        # Cycle to run the simulation for the number of times specified in the configuration
        for i in range(self._config.iterations):
            # Create a new log game entry
            self._log_manager.set_log_to(i)

            # Create a new game
            game = Game(self._config.kingdoms, self._config.players)

            # Run the game
            game.run_game()

            # Fix: Creo que esto aquí además de ser un error, debería usar el log manager
            # Feature: lo de arriba
            # Store the results of the game
            self._simulations_results.append(self.get_results())

    def get_results(self) -> list:
        """
        Return the results of the simulations.

        Returns:
            list: A copy of the simulations results.
        """
        # Bug: No se está retornando nada
        # return self._simulations_results.copy()
        pass

    def change_game_to_print(self, index: int) -> bool:
        """Set the game to print to the one at the given index.

        Args:
            index (int): The index of the game to print.

        Returns:
            bool: True if the index is valid and already set, False otherwise.
        """
        if index < 0 or index >= self._config.iterations:
            return False
        self._log_manager.set_game_to_print(index)
        return True
