from enum import Enum
from multiprocessing import Queue


class LogType(Enum):
    START_GAME = "start_game"
    ATTACK_SOLDIER = "attack_soldier"
    ATTACK_WALL = "attack_wall"
    ATTACK_TOWN = "attack_town"
    ATTACK_KING = "attack_king"
    UPGRADE_SOLDIER = "upgrade_soldier"
    UPGRADE_WALL = "upgrade_wall"
    UPGRADE_TOWN = "upgrade_town"
    PROPOSE_ALLIANCE = "propose_alliance"
    ACCEPT_ALLIANCE = "accept_alliance"
    DECLINE_ALLIANCE = "decline_alliance"
    END_GAME = "end_game"


class LogIndexType:
    ATTACK_SOLDIER_ATTACKER_PLAYER = "asap"
    ATTACK_SOLDIER_ATTACKER_SOLDIER_ID = "asasid"
    ATTACK_SOLDIER_ATTACKER_SOLDIER_LVL = "asaslvl"
    ATTACK_SOLDIER_ATTACKER_STATUS = "asas"
    ATTACK_SOLDIER_DEFENDER_PLAYER = "asdp"
    ATTACK_SOLDIER_DEFENDER_SOLDIER_ID = "asdsid"
    ATTACK_SOLDIER_DEFENDER_SOLDIER_LVL = "asdslvl"
    ATTACK_SOLDIER_DEFENDER_STATUS = "asds"
    ATTACK_WALL_ATTACKER_PLAYER = "awap"
    ATTACK_WALL_ATTACKER_SOLDIER_ID = "awasid"
    ATTACK_WALL_ATTACKER_SOLDIER_LVL = "awaslvl"
    ATTACK_WALL_ATTACKER_STATUS = "awas"
    ATTACK_WALL_DEFENDER_PLAYER = "awdp"
    ATTACK_WALL_DEFENDER_WALL_LVL = "awdwlvl"
    ATTACK_WALL_DEFENDER_WALL_STATUS = "awdws"
    ATTACK_TOWN_ATTACKER_PLAYER = "atap"
    ATTACK_TOWN_ATTACKER_SOLDIER_ID = "atasid"
    ATTACK_TOWN_ATTACKER_SOLDIER_LVL = "ataslvl"
    ATTACK_TOWN_ATTACKER_STATUS = "atas"
    ATTACK_TOWN_DEFENDER_PLAYER = "atdp"
    ATTACK_TOWN_DEFENDER_TOWN_LVL = "atdtlvl"
    ATTACK_TOWN_DEFENDER_TOWN_STATUS = "atdts"
    ATTACK_KING_ATTACKER_PLAYER = "akap"
    ATTACK_KING_ATTACKER_SOLDIER_ID = "akasid"
    ATTACK_KING_ATTACKER_SOLDIER_LVL = "akaslvl"
    ATTACK_KING_DEFENDER_PLAYER = "akdp"
    UPGRADE_SOLDIER_PLAYER = "usap"
    UPGRADE_SOLDIER_SOLDIER_ID = "usasid"
    UPGRADE_SOLDIER_OLD_LVL = "usolvl"
    UPGRADE_SOLDIER_POINTS_USED = "uspu"
    UPGRADE_SOLDIER_CURRENT_LVL = "usclvl"
    UPGRADE_WALL_PLAYER = "uwap"
    UPGRADE_WALL_OLD_LVL = "uwolvl"
    UPGRADE_WALL_POINTS_USED = "uwpu"
    UPGRADE_WALL_CURRENT_LVL = "uwclvl"
    UPGRADE_TOWN_PLAYER = "utap"
    UPGRADE_TOWN_OLD_LVL = "utolvl"
    UPGRADE_TOWN_CURRENT_LVL = "utclvl"
    PROPOSE_ALLIANCE_PROPOSER_PLAYER = "papp"
    PROPOSE_ALLIANCE_RECEIVER_PLAYER = "parp"
    PROPOSE_ALLIANCE_TURNS = "pat"
    ACCEPT_ALLIANCE_ACCEPTER_PLAYER = "aaap"
    ACCEPT_ALLIANCE_ACCEPTED_PLAYER = "aaadp"
    ACCEPT_ALLIANCE_TURNS = "aat"
    DECLINE_ALLIANCE_DECLINER_PLAYER = "daldp"
    DECLINE_ALLIANCE_DECLINED_PLAYER = "dalp"
    DECLINE_ALLIANCE_TURNS = "dalt"
    START_GAME_CONDITION = "sgc"
    END_GAME_WINNER = "egw"
    END_GAME_CONDITION = "egc"


class LogNode:
    def __init__(self, log: list[str], log_type: LogType) -> None:
        self._elements: dict[str, str] = {}
        self.previous = None
        self.next = None
        self._log_type = log_type
        self._build_log_node(log)

    def _build_log_node(self, parsed_log: list[str]):
        """Build the log node using the parsed log.
        Args:
            parsed_log (list[str]): The parsed log.
        """
        # Check log node type
        if self._log_type == LogType.ATTACK_SOLDIER:
            self._build_attack_soldier(parsed_log)
        elif self._log_type == LogType.ATTACK_WALL:
            self._build_attack_wall(parsed_log)
        elif self._log_type == LogType.ATTACK_TOWN:
            self._build_attack_town(parsed_log)
        elif self._log_type == LogType.ATTACK_KING:
            self._build_attack_king(parsed_log)
        elif self._log_type == LogType.UPGRADE_SOLDIER:
            self._build_upgrade_soldier(parsed_log)
        elif self._log_type == LogType.UPGRADE_WALL:
            self._build_upgrade_wall(parsed_log)
        elif self._log_type == LogType.UPGRADE_TOWN:
            self._build_upgrade_town(parsed_log)
        elif self._log_type == LogType.PROPOSE_ALLIANCE:
            self._build_propose_alliance(parsed_log)
        elif self._log_type == LogType.ACCEPT_ALLIANCE:
            self._build_accept_alliance(parsed_log)
        elif self._log_type == LogType.DECLINE_ALLIANCE:
            self._build_decline_alliance(parsed_log)
        elif self._log_type == LogType.START_GAME:
            self._build_start_game(parsed_log)
        elif self._log_type == LogType.END_GAME:
            self._build_end_game(parsed_log)

    @property
    def log_type(self) -> LogType:
        """Get the type of the log node.

        Returns:
            LogType: The type of the log node.
        """
        return self._log_type

    @property
    def elements(self) -> dict[str, str]:
        """Get the elements of the log node.

        Returns:
            dict[str, str]: The elements of the log node.
        """
        return self._elements

    def _build_start_game(self, parsed_log: list[str]):
        self._elements[LogIndexType.START_GAME_CONDITION] = parsed_log[0]

    def _build_end_game(self, parsed_log: list[str]):
        self._elements[LogIndexType.END_GAME_WINNER] = parsed_log[0]
        self._elements[LogIndexType.END_GAME_CONDITION] = parsed_log[1]

    def _build_attack_soldier(self, parsed_log: list[str]):
        self._elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_SOLDIER_ID] = parsed_log[1]
        self._elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_SOLDIER_LVL] = parsed_log[2]
        self._elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_STATUS] = parsed_log[3]
        self._elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_PLAYER] = parsed_log[4]
        self._elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_SOLDIER_ID] = parsed_log[5]
        self._elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_SOLDIER_LVL] = parsed_log[6]
        self._elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_STATUS] = parsed_log[7]

    def _build_attack_wall(self, parsed_log: list[str]):
        self._elements[LogIndexType.ATTACK_WALL_ATTACKER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.ATTACK_WALL_ATTACKER_SOLDIER_ID] = parsed_log[1]
        self._elements[LogIndexType.ATTACK_WALL_ATTACKER_SOLDIER_LVL] = parsed_log[2]
        self._elements[LogIndexType.ATTACK_WALL_ATTACKER_STATUS] = parsed_log[3]
        self._elements[LogIndexType.ATTACK_WALL_DEFENDER_PLAYER] = parsed_log[4]
        self._elements[LogIndexType.ATTACK_WALL_DEFENDER_WALL_LVL] = parsed_log[5]
        self._elements[LogIndexType.ATTACK_WALL_DEFENDER_WALL_STATUS] = parsed_log[6]

    def _build_attack_town(self, parsed_log: list[str]):
        self._elements[LogIndexType.ATTACK_TOWN_ATTACKER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.ATTACK_TOWN_ATTACKER_SOLDIER_ID] = parsed_log[1]
        self._elements[LogIndexType.ATTACK_TOWN_ATTACKER_SOLDIER_LVL] = parsed_log[2]
        self._elements[LogIndexType.ATTACK_TOWN_ATTACKER_STATUS] = parsed_log[3]
        self._elements[LogIndexType.ATTACK_TOWN_DEFENDER_PLAYER] = parsed_log[4]
        self._elements[LogIndexType.ATTACK_TOWN_DEFENDER_TOWN_LVL] = parsed_log[5]
        self._elements[LogIndexType.ATTACK_TOWN_DEFENDER_TOWN_STATUS] = parsed_log[6]

    def _build_attack_king(self, parsed_log: list[str]):
        self._elements[LogIndexType.ATTACK_KING_ATTACKER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.ATTACK_KING_ATTACKER_SOLDIER_ID] = parsed_log[1]
        self._elements[LogIndexType.ATTACK_KING_ATTACKER_SOLDIER_LVL] = parsed_log[2]
        self._elements[LogIndexType.ATTACK_KING_DEFENDER_PLAYER] = parsed_log[3]

    def _build_upgrade_soldier(self, parsed_log: list[str]):
        self._elements[LogIndexType.UPGRADE_SOLDIER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.UPGRADE_SOLDIER_SOLDIER_ID] = parsed_log[1]
        self._elements[LogIndexType.UPGRADE_SOLDIER_OLD_LVL] = parsed_log[2]
        self._elements[LogIndexType.UPGRADE_SOLDIER_POINTS_USED] = parsed_log[3]
        self._elements[LogIndexType.UPGRADE_SOLDIER_CURRENT_LVL] = parsed_log[4]

    def _build_upgrade_wall(self, parsed_log: list[str]):
        self._elements[LogIndexType.UPGRADE_WALL_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.UPGRADE_WALL_OLD_LVL] = parsed_log[1]
        self._elements[LogIndexType.UPGRADE_WALL_POINTS_USED] = parsed_log[2]
        self._elements[LogIndexType.UPGRADE_WALL_CURRENT_LVL] = parsed_log[3]

    def _build_upgrade_town(self, parsed_log: list[str]):
        self._elements[LogIndexType.UPGRADE_TOWN_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.UPGRADE_TOWN_OLD_LVL] = parsed_log[1]
        self._elements[LogIndexType.UPGRADE_TOWN_CURRENT_LVL] = parsed_log[2]

    def _build_propose_alliance(self, parsed_log: list[str]):
        self._elements[LogIndexType.PROPOSE_ALLIANCE_PROPOSER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.PROPOSE_ALLIANCE_RECEIVER_PLAYER] = parsed_log[1]
        self._elements[LogIndexType.PROPOSE_ALLIANCE_TURNS] = parsed_log[2]

    def _build_accept_alliance(self, parsed_log: list[str]):
        self._elements[LogIndexType.ACCEPT_ALLIANCE_ACCEPTER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.ACCEPT_ALLIANCE_ACCEPTED_PLAYER] = parsed_log[1]
        self._elements[LogIndexType.ACCEPT_ALLIANCE_TURNS] = parsed_log[2]

    def _build_decline_alliance(self, parsed_log: list[str]):
        self._elements[LogIndexType.DECLINE_ALLIANCE_DECLINER_PLAYER] = parsed_log[0]
        self._elements[LogIndexType.DECLINE_ALLIANCE_DECLINED_PLAYER] = parsed_log[1]
        self._elements[LogIndexType.DECLINE_ALLIANCE_TURNS] = parsed_log[2]


class LogManager:

    def __init__(self) -> None:
        self._games: dict[int, LogNode] = {}
        self._current_game_index = 0
        self._game_to_print_index = 0
        self._printable_game_logs_queue = Queue()

    def _add_log(self, log: list[str], log_type: LogType):
        """Add a log to the current game.

        Args:
            log (list[str]): The log to add.
            log_type (LogType): The type of the log.
        """
        # Check if the current game that are storing logs its the game that will be printed
        store_in_queue = self._current_game_index == self._game_to_print_index

        # Build the log using log nodes
        log_node = LogNode(log, log_type)

        # Store the log in the game
        if self._current_game_index not in self._games:
            self._games[self._current_game_index] = log_node
        else:
            current_log = self._games[self._current_game_index]
            while current_log.next is not None:
                current_log = current_log.next
            current_log.next = log_node
            log_node.previous = current_log

        # Store the log in the queue if needed
        if store_in_queue:
            self._printable_game_logs_queue.put(log_node)

    def set_game_to_print(self, index: int):
        """Set the game to print to the one at the given index.

        Args:
            index (int): The index of the game to print.
        """
        self._game_to_print_index = index

    def set_log_to(self, current_game_index):
        """Set the log to the one at the given index.

        Args:
            current_game_index (int): The index of the log to set.
        """
        self._current_game_index = current_game_index

    @property
    def available_logs_for_print(self):
        return self._printable_game_logs_queue.qsize() > 0

    @property
    def log_to_print(self):
        return self._printable_game_logs_queue.get()

    def add_start_game_log(self, player: str):
        """Add a log of the start of a game.

        Args:
            player (str): The player that starts the game.
        """
        log = [player]
        self._add_log(log, LogType.START_GAME)

    def add_end_game_log(self, winner: str, win_condition: str):
        """Add a log of the end of a game.

        Args:
            winner (str): The player that wins the game.
            win_condition (str): The condition that the winner wins the game.
        """
        log = [winner, win_condition]
        self._add_log(log, LogType.END_GAME)

    def add_soldier_attack_log(
        self,
        attacker_player: str,
        attacker_soldier_id: str,
        attacker_soldier_lvl: str,
        attacker_status: str,
        defender_player: str,
        defender_soldier_id: str,
        defender_soldier_lvl: str,
        defender_status: str,
    ):
        """Add a log of a fight between two soldiers.

        Args:
            attacker_player (str): Player that attacks.
            attacker_soldier_id (str): The id of the attacking soldier.
            attacker_soldier_lvl (str): The level of the attacking soldier.
            attacker_status (str): The status of the attacking soldier after the fight.
            defender_player (str): Player that defends.
            defender_soldier_id (str): The id of the defending soldier.
            defender_soldier_lvl (str): The level of the defending soldier.
            defender_status (str): The status of the defending soldier after the fight.
        """
        log = [
            attacker_player,
            attacker_soldier_id,
            attacker_soldier_lvl,
            attacker_status,
            defender_player,
            defender_soldier_id,
            defender_soldier_lvl,
            defender_status,
        ]
        self._add_log(log, LogType.ATTACK_SOLDIER)

    def add_wall_attack_log(
        self,
        attacker_player: str,
        attacker_soldier_id: str,
        attacker_soldier_lvl: str,
        attacker_status: str,
        defender_player: str,
        defender_wall_lvl: str,
        defender_wall_status: str,
    ):
        """Add a log of a fight between a soldier and a wall.

        Args:
            attacker_player (str): Player that attacks.
            attacker_soldier_id (str): The id of the attacking soldier.
            attacker_soldier_lvl (str): The level of the attacking soldier.
            attacker_status (str): The status of the attacking soldier after the fight.
            defender_player (str): Player that defends.
            defender_wall_lvl (str): The level of the defending wall.
            defender_wall_status (str): The status of the defending wall after the fight.
        """
        log = [
            attacker_player,
            attacker_soldier_id,
            attacker_soldier_lvl,
            attacker_status,
            defender_player,
            defender_wall_lvl,
            defender_wall_status,
        ]
        self._add_log(log, LogType.ATTACK_WALL)

    def add_town_attack_log(
        self,
        attacker_player: str,
        attacker_soldier_id: str,
        attacker_soldier_lvl: str,
        attacker_status: str,
        defender_player: str,
        defender_town_lvl: str,
        defender_town_status: str,
    ):
        """Add a log of a fight between a soldier and a town.

        Args:
            attacker_player (str): Player that attacks.
            attacker_soldier_id (str): The id of the attacking soldier.
            attacker_soldier_lvl (str): The level of the attacking soldier.
            attacker_status (str): The status of the attacking soldier after the fight.
            defender_player (str): Player that defends.
            defender_town_lvl (str): The level of the defending town.
            defender_town_status (str): The status of the defending town after the fight.
        """
        log = [
            attacker_player,
            attacker_soldier_id,
            attacker_soldier_lvl,
            attacker_status,
            defender_player,
            defender_town_lvl,
            defender_town_status,
        ]
        self._add_log(log, LogType.ATTACK_TOWN)

    def add_king_attack_log(
        self,
        attacker_player: str,
        attacker_soldier_id: str,
        attacker_soldier_lvl: str,
        attacker_status: str,
        defender_player: str,
    ):
        """Add a log of a fight between a soldier and a king.

        Args:
            attacker_player (str): Player that attacks.
            attacker_soldier_id (str): The id of the attacking soldier.
            attacker_soldier_lvl (str): The level of the attacking soldier.
            attacker_status (str): The status of the attacking soldier after the fight.
            defender_player (str): Player that defends.
        """
        log = [
            attacker_player,
            attacker_soldier_id,
            attacker_soldier_lvl,
            attacker_status,
            defender_player,
        ]
        self._add_log(log, LogType.ATTACK_KING)

    def add_soldier_upgrade_log(
        self,
        player: str,
        soldier_id: str,
        old_lvl: str,
        points_used: str,
        current_lvl: str,
    ):
        """Add a log of a soldier upgrade.

        Args:
            player (str): The player that upgrades the soldier.
            soldier_id (str): The id of the soldier.
            old_lvl (str): The old level of the soldier.
            points_used (str): The points used to upgrade the soldier.
            current_lvl (str): The current level of the soldier.
        """
        log = [player, soldier_id, old_lvl, points_used, current_lvl]
        self._add_log(log, LogType.UPGRADE_SOLDIER)

    def add_wall_upgrade_log(
        self, player: str, old_lvl: str, points_used: str, current_lvl: str
    ):
        """Add a log of a wall upgrade.

        Args:
            player (str): The player that upgrades the wall.
            old_lvl (str): The old level of the wall.
            points_used (str): The points used to upgrade the wall.
            current_lvl (str): The current level of the wall.
        """
        log = [player, old_lvl, points_used, current_lvl]
        self._add_log(log, LogType.UPGRADE_WALL)

    def add_town_upgrade_log(self, player: str, old_lvl: str, current_lvl: str):
        """Add a log of a town upgrade.

        Args:
            player (str): The player that upgrades the town.
            old_lvl (str): The old level of the town.
            current_lvl (str): The current level of the town.
        """
        log = [player, old_lvl, current_lvl]
        self._add_log(log, LogType.UPGRADE_TOWN)

    def add_propose_alliance_log(
        self, proposer_player: str, receiver_player: str, turns: str
    ):
        """Add a log of an alliance proposal.

        Args:
            proposer_player (str): The player that proposes the alliance.
            receiver_player (str): The player that receives the alliance proposal.
            turns (str): The turns that the alliance will last.
        """
        log = [proposer_player, receiver_player, turns]
        self._add_log(log, LogType.PROPOSE_ALLIANCE)

    def add_accept_alliance_log(
        self, accepter_player: str, accepted_player: str, turns: str
    ):
        """Add a log of an alliance acceptance.

        Args:
            accepter_player (str): The player that accepts the alliance.
            accepted_player (str): The player that proposed the alliance.
            turns (str): The turns that the alliance will last.
        """
        log = [accepter_player, accepted_player, turns]
        self._add_log(log, LogType.ACCEPT_ALLIANCE)

    def add_decline_alliance_log(
        self, decliner_player: str, declined_player: str, turns: str
    ):
        """Add a log of an alliance decline.

        Args:
            decliner_player (str): The player that declines the alliance.
            declined_player (str): The player that proposed the alliance.
            turns (str): The turns that the alliance would have lasted.
        """
        log = [decliner_player, declined_player, turns]
        self._add_log(log, LogType.DECLINE_ALLIANCE)

    def get_logs_from_game(self, game_index: int) -> list[LogNode]:
        """Get the logs of the given game index.

        Args:
            game_index (int): The index of the game.

        Returns:
            list[LogNode]: The logs of the game.
        """
        return self._games[game_index]

    def get_all_logs(self) -> dict[int, list[LogNode]]:
        """Get all the logs stored.

        Returns:
            dict[int, list[LogNode]]: The logs stored.
        """
        return self._games
