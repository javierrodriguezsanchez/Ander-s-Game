from src.Llm.log_manager import LogManager, LogType
from src.Agent.Agent import Agent
from src.Simulation_Model.Reigns import Kingdom
import os


class Game:

    def __init__(
        self,
        Kingdoms: list[Kingdom],
        Players: list[Agent],
        verbose: bool,
        log_manager: LogManager,
        max_rounds: int = 100,
    ):
        self.kingdoms = Kingdoms
        self.players = Players
        self._max_rounds = max_rounds
        self.winner = ""
        self.win_reason = ""
        self._verbose = verbose
        self._log_manager = log_manager

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
            self.players[i].Update_State(self.kingdoms, i,None,0)

        self._log_manager.add_start_game_log(players_count)

        while alive_players_count > 1 and current_round < self._max_rounds:

            if self._verbose:
                print(f"Round:{current_round}")
            for i in range(players_count):
                current_turn += 1
                if current_turn % players_count == 0:
                    current_round += 1

                if not self.kingdoms[i].king_alive:
                    if alive_players_status[i]:
                        alive_players_count -= 1
                        alive_players_status[i] = False
                    continue

                old_town_population = self.kingdoms[i].population
                self.kingdoms[i].new_turn()
                self._log_manager.add_town_upgrade_log(
                    i, old_town_population, self.kingdoms[i].population
                )

                # Search for alliances
                possible_alliances = self.players[i].Propose_Alliance()

                for target, p_a in enumerate(possible_alliances):
                    if p_a:
                        # Fix: Ahora mismo, las alianzas tienen turnos fijos a 3
                        self._log_manager.add_propose_alliance_log(i, target, 3)

                # Search for acceptance
                for j in possible_alliances:
                    if possible_alliances[j]:
                        if self.players[i].Alliance_Answer(
                            j, self.players[j].Accept_Alliance(i)
                        ):
                            # Fix: Ahora mismo, las alianzas tienen turnos fijos a 3
                            self._log_manager.add_accept_alliance_log(j, i, 3)
                        else:
                            # Fix: Ahora mismo, las alianzas tienen turnos fijos a 3
                            self._log_manager.add_decline_alliance_log(j, i, 3)

                # Get all turn actions
                actions_to_perform = self.players[i].Play()

                # Perform all actions
                for action in actions_to_perform:
                    self.kingdoms[i].act(self.kingdoms, action, self._log_manager)
                    # If the actins was an attack, tell the other player
                    if "Attack" in action["action"]:
                        for j in range(players_count):
                            if j != i:
                                self.players[j].Percept_Attack(
                                    action["index"], action["target"], action["action"]
                                )

                self.players[i].EndTurn()
                for j in range(players_count):
                    self.players[j].Update_State(self.kingdoms, j, actions_to_perform, i)

        self._get_winner(alive_players_count, alive_players_status)

        self._log_manager.add_end_game_log(self.winner, self.win_reason)

        if self._verbose:
            self._print_end_condition(alive_players_count)
            self._print_winner()
            self._print_end_status()

    def _get_winner(self, alive_players_count, alive_players_status):
        if alive_players_count == 1:
            self.win_reason = "Win by elimination"

            for i in range(len(alive_players_status)):
                if alive_players_status[i]:
                    self.winner = i
                    break
        else:
            winner_index, _ = max(
                enumerate(
                    [self._get_player_score(i) for i in range(len(self.kingdoms))]
                ),
                key=lambda x: x[1],
            )
            self.winner = winner_index
            self.win_reason = "Win by score"

    def _print_end_condition(self, alive_players_count):
        """Print the end condition of the game

        Args:
            alive_players_count (int): The number of players alive at the end of the game
        """
        print(
            f"<---Game ended with {alive_players_count} players alive--->\n{self.win_reason}"
        )

    def _print_winner(self):
        """Print the winner of the game

        Args:
            alive_players_count (int): The number of players alive at the end of the game
            alive_players_status (int): The status of the players at the end of the game
        """
        print(
            f"<---Player {self.winner} wins using {self.players[self.winner].strategy_name} strategy!--->"
        )

    def _get_player_score(self, player_index: int):
        """Get the score of the player with the given index

        Args:
            player_index (int): The index of the player to get the score
        """
        return (
            self.kingdoms[player_index].population
            + self.kingdoms[player_index].walls
            + sum(self.kingdoms[player_index].army)
        )

    def _print_end_status(self):
        """Print the end state of the game"""
        for i, kingdom in enumerate(self.kingdoms):
            if kingdom.king_alive:
                score = kingdom.population + kingdom.walls + sum(kingdom.army)
                print(
                    f"{self.players[i].strategy_name} survived, with a town of {kingdom.population}, a wall of {kingdom.walls}, and with this army {kingdom.army}. Total score {score}!"
                )
            else:
                print(f"{self.players[i].strategy_name} don't make it :(")
