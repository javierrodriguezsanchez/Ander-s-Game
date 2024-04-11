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
        alive_players_status = [True] * players_count
        alive_players_count = players_count

        # Tell the players how many players are in the game
        for i in range(players_count):
            self.players[i].Number_Of_Players(players_count)

        for i in range(players_count):
            self.players[i].Update_State(self.kingdoms, i)

        while alive_players_count > 1 or current_round < self._max_rounds:
            for i in range(players_count):
                current_turn += 1
                if current_turn % players_count == 0:
                    current_round += 1

                # todo: si el jugador está muerto, siguiente turno
                if not self.kingdoms[i].king_alive:
                    if alive_players_status[i]:
                        alive_players_count -= 1
                        alive_players_status[i] = False
                    continue

                self.kingdoms[i].new_turn()

                # Search for alliances
                possible_alliances = self.players[i].Propose_Alliance()

                # Search for acceptance
                [
                    (
                        self.players[i].Alliance_Answer(
                            j, self.players[j].Accept_Alliance(i)
                        )
                        if possible_alliances[j]
                        else None
                    )
                    for j in possible_alliances
                ]

                # Get all turn actions
                actions_to_perform = self.players[i].Play()

                # Perform all actions
                for action in actions_to_perform:
                    self.kingdoms[i].act(self.kingdoms, action)
                    # If the actins was an attack, tell the other player
                    if "Attack" in action["action"]:
                        for j in range(players_count):
                            if j != i:
                                self.players[j].Percept_Attack(
                                    action["index"], action["target"], action["action"]
                                )

                self.players[i].EndTurn()
                for j in range(players_count):
                    self.players[i].Update_State(self.kingdoms, i)
