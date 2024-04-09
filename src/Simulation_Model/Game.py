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

        # Tell the players how many players are in the game
        for i in range(players_count):
            self.players[i].Number_Of_Players(players_count)

        for i in range(players_count):
            self.players[i].Update_State(self.kingdoms, i)

        # todo: cambiar la condición sin tener el cuenta el conteo, por que no se eliminan
        while players_count > 1 or current_round < self._max_rounds:
            for i in range(players_count):
                current_turn += 1
                if current_turn % players_count == 0:
                    current_round += 1

                # todo: si el jugador está muerto, siguiente turno

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
                    self.kingdoms[i].act(self.kingdoms, action[0], action[1])
                    # If the actins was an attack, tell the other player
                    if "attack" in action[0]:
                        for j in range(players_count):
                            if j != i:
                                self.players[j].Percept_Attack(
                                    i, action[1][2], action[0]
                                )
                # BUG: esto hay que borrarlo, es una nota personal. actions[0] es el nombre de la acción, actions[1] es la información de la acción. actions[1][0] es quien ejecuta la acción, actions[1][1] es con que tropa la ejecuta, actions [1][2] es a quien ataca, actions[1][3] es la cantidad de tropas que ataca.
                # Todo: poner en algún que se murió el rey. Depende de la acción de Luis para que esté viajando esa información por todo el código :)

                self.players[i].EndTurn()
                self.players[i].Update_State(self.kingdoms, i)
