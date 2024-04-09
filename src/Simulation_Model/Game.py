from src.Agent.Agent import Agent
from src.Simulation_Model.Reigns import Kingdom
import os


class Game:

    def __init__(
        self, Kingdoms: list[Kingdom], Players: list[Agent], max_rounds: int = 100
    ):
        self.kingdoms = Kingdoms
        self.players = Players
        self._max_rounds = max_rounds

    def run_game(self):
        current_turn = 0
        current_round = 0

        players_count = len(self.players)

        while players_count > 1 or current_round < self._max_rounds:
            for i in range(players_count):
                self.players[i].Update_State(self.kingdoms, i)
                self.players[i].Number_Of_Players(players_count)
                self.players[i].Play()
                self.players[i].EndTurn()
                current_turn += 1
                players_count = len(self.players)
                if current_turn % players_count == 0:
                    current_round += 1
