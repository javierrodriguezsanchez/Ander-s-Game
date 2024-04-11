from src.Strategies.Implementations.MultipleStrategy import MultipleStrategy
from src.Simulation_Model.Reigns import Kingdom
from src.Agent.Agent import Agent


class Config:

    def __init__(
        self,
        simulation_kingdoms: list[Kingdom],
        players: list[Agent],
        iterations: int = 100,
    ):
        self._kingdoms = simulation_kingdoms
        self._players = players
        self._iterations = iterations

    @property
    def kingdoms(self):
        return [kingdom.clone() for kingdom in self._kingdoms]

    @property
    def players(self):
        return [
            Agent(self._get_strategy(player.KB.strategy)) for player in self._players
        ]

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
        return self._iterations
