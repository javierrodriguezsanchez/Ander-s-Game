from src.Strategies.Implementations.MultipleStrategy import MultipleStrategy
from src.Simulation_Model.Reigns import Kingdom
from src.Agent.Agent import Agent


class Config:

    def __init__(
        self,
        simulation_kingdoms: list[Kingdom],
        players: list[Agent],
        verbose: bool,
        iterations: int = 100,
        rounds_per_game: int = 100,
    ):
        self._kingdoms = simulation_kingdoms
        self._players = players
        self._iterations = iterations
        self._rounds_per_game = rounds_per_game
        self._verbose = verbose

    @property
    def kingdoms(self):
        return [kingdom.clone() for kingdom in self._kingdoms]

    @property
    def players(self):
        return [
            Agent(self._get_strategy(player.KB.strategy)) for player in self._players
        ]

    @property
    def verbose(self):
        return self._verbose

    def _get_strategy(self, strategy_in):
        """Get a full clone of the strategy_in

        Args:
            strategy_in (Strategy): Strategy to clone
        """

        result = strategy_in
        if strategy_in is MultipleStrategy:
            strategies_in_strategy = []
            for s in strategy_in.strategies:
                strategies_in_strategy.append(self._get_strategy(s))
            result = MultipleStrategy(strategies_in_strategy)
        return result

    @property
    def iterations(self):
        """Return the number of iterations to run the simulation.

        Returns:
            int: The number of iterations to run the simulation.
        """
        return self._iterations

    @property
    def rounds_per_game(self):
        """Return the number of rounds per game.

        Returns:
            int: The number of rounds per game.
        """
        return self._rounds_per_game
