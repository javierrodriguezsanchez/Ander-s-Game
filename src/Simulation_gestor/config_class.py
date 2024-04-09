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
        return [Kingdom(kingdom) for kingdom in self._kingdoms]

    @property
    def players(self):
        return [player.clone() for player in self._players]

    @property
    def iterations(self):
        return self._iterations
