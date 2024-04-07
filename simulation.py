from Game import Game
from config_class import Config


class Simulation:
    def __init__(self, config: Config):
        self._config = config
        self._simulations_results = []
        self._game_to_print = None
        self._game_to_print_index = 0

    def run(self):
        """Perform the simulation with the given configuration."""

        # Cycle to run the simulation for the number of times specified in the configuration
        for i in range(self._config.number_of_simulations):
            # Create a new game
            game = Game(self._config.kingdoms, self._config.players)

            # Run the game
            game.run_game()

            # Store the results of the game
            self._simulations_results.append(game.get_results())

            # Set the game to print if it is the one at the index
            if i == self._game_to_print_index:
                self._game_to_print = game

    def get_results(self) -> list:
        """
        Return the results of the simulations.

        Returns:
            list: A copy of the simulations results.
        """
        return self._simulations_results.copy()

    def change_game_to_print(self, index: int) -> bool:
        """Set the game to print to the one at the given index.

        Args:
            index (int): The index of the game to print.

        Returns:
            bool: True if the index is valid and already set, False otherwise.
        """
        if index < 0 or index >= len(self._config.iterations):
            return False
        self._game_to_print_index = index
        return True
