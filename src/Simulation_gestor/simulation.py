import time
from src.Simulation_Model.Game import Game
from src.Simulation_gestor.config_class import Config
from src.Llm.log_manager import LogIndexType, LogManager, LogNode
import csv
import random


class Simulation:
    def __init__(self, config: Config, log_manager: LogManager):
        self._config = config
        self._simulation_wins = []
        self._simulation_strategies_for_player = [
            player.name for player in config.players
        ]
        self._log_manager = log_manager
        self._verbose = config.verbose

    def run(self):
        """Perform the simulation with the given configuration."""

        # Cycle to run the simulation for the number of times specified in the configuration
        for i in range(self._config.iterations):
            # Create a new log game entry
            self._log_manager.set_log_to(i)

            Players = self._config.players
            random.shuffle(Players)

            # Create a new game
            print(f"Starting Game {i+1}")
            game = Game(
                self._config.kingdoms,
                Players,
                self._verbose,
                self._log_manager,
                self._config.rounds_per_game,
            )

            # Run the game
            game.run_game()

            # Store the results of the game
            self.get_results(self._log_manager.get_logs_from_game(i))

        self._export_results()

    def get_results(self, logs: LogNode) -> list:
        """
        Get the results of the game from the logs.

        Args:
            logs (LogNode): The logs of the game.

        Returns:
            list: The results of the game.
        """

        # Get the winner of the game
        iterable_logs = logs
        while iterable_logs.next is not None:
            iterable_logs = iterable_logs.next
        winner = int(iterable_logs.elements[LogIndexType.END_GAME_WINNER])

        self._simulation_wins[winner] += 1

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

    def export_results(self):
        """Export the results of the simulation to a csv file.\n
        The table will look like this\n
        |Player|Strategy|Wins|
        """

        with open(f"simulation_results.{time.time()}.csv", mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["Player", "Strategy", "Wins"])
            for i in range(len(self._simulation_wins)):
                writer.writerow(
                    [
                        i,
                        self._simulation_strategies_for_player[i],
                        self._simulation_wins[i],
                    ]
                )
