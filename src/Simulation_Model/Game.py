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

        while alive_players_count > 1 and current_round < self._max_rounds:
            print(current_round)
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
        a = 1

        # Todo: quitar esta línea, es temporal hasta que ponga el modo verbose
        # Print the winner

        self._print_end_condition(alive_players_count)
        self._print_winner(alive_players_count, alive_players_status)
        self._print_end_status()

    def _print_end_condition(self, alive_players_count):
        """Print the end condition of the game

        Args:
            alive_players_count (int): The number of players alive at the end of the game
        """
        if alive_players_count == 1:
            print("Win by elimination")
        else:
            print("Win by score")

    def _print_winner(self, alive_players_count, alive_players_status):
        """Print the winner of the game

        Args:
            alive_players_count (int): The number of players alive at the end of the game
            alive_players_status (int): The status of the players at the end of the game
        """
        if alive_players_count == 1:
            for i in range(len(alive_players_status)):
                if alive_players_status[i]:
                    print(f"Player {i} wins!")
                    break
        else:
            winner_index, score = max(
                enumerate(
                    [self._get_player_score(i) for i in range(len(self.kingdoms))]
                ),
                key=lambda x: x[1],
            )
            print(f"Player {winner_index} wins with a score of {score}!")

    def _get_player_score(self, player_index: int):
        """Get the score of the player with the given index

        Args:
            player_index (int): The index of the player to get the score
        """
        return (
            self.kingdoms[player_index].kingdom.population
            + self.kingdoms[player_index].kingdom.walls
            + sum(self.kingdoms[player_index].kingdom.army)
        )

    def _print_end_status(self):
        """Print the end state of the game"""
        for i, kingdom in enumerate(self.kingdoms):
            if kingdom.king_alive:
                score = kingdom.population + kingdom.walls + sum(kingdom.army)
                print(
                    f"Player {i} survived {self._max_rounds} rounds with a town of {kingdom.population}, a wall of {kingdom.walls}, and with this army {kingdom.army}. Total score {score}!"
                )
            else:
                print(f"Player {i} don't make it :(")
