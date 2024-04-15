import threading
from src.Llm.history_handler import HistoryHandler
from src.Llm.llm_interface import LLMInterface
from src.Llm.log_manager import LogManager, LogNode, LogType, LogIndexType


class HistoryProcess:
    def __init__(self, log_manager: LogManager, history_simulator_communicator):
        self._llm_interface = LLMInterface()
        self._history_handler = HistoryHandler()
        self._log_manager = log_manager
        self._history_simulator_communicator = history_simulator_communicator
        self._running = False
        self._history_constants = ""
        self._last_count_of_histories = 0

    def add_log(self, log) -> None:
        self._logs_queue.append(log)

    @property
    def last_count_of_histories(self):
        return self._last_count_of_histories

    def start_process(self) -> None:
        """
        Start a new process to generate the story of the game using the logs
        """
        # Connect to the LLM interface
        try:
            self._llm_interface.connect()
        except Exception as e:
            raise Exception(f"Error connecting the LLM Interface: {e}")

        self.thread = threading.Thread(target=self._create_story)
        self._running = True
        self.thread.start()

    def _create_story(self) -> None:
        """
        Create the story of the game using the logs
        """

        log = None
        # Main loop
        while self._running:

            # Check if there are logs to process
            if self._log_manager.available_logs_for_print:

                # Take the first log
                log = self._log_manager.log_to_print

                log_text = self._extract_log_text(log)

                # Generate the history
                history, history_resume = self._llm_interface.generate_history(
                    self._history_handler._history_resume, log_text
                )

                # Check if is the first entry
                if self._history_handler._counter == 0:
                    # Feature: Se puede poner para que se procese la historia y no se guarde por completo cómo se devuelve
                    self._history_constants = history

                # Update the history resume
                self._history_handler._history_resume = history_resume

                # Add the created history to the history handler
                self._history_handler.add_entry(history, log_text)

                # Send the history to the simulator
                self._history_simulator_communicator(history)

                # Update the last count of histories
                self._last_count_of_histories = self._history_handler._counter

    def _extract_log_text(self, log: LogNode) -> str:
        """
        Extract the text from the log

        Args:
            log: The log to be processed

        Returns:
            str: The text extracted from the log
        """
        if log.log_type == LogType.START_GAME:
            return f"The game has {log.elements[LogIndexType.START_GAME_CONDITION]} players. Only create a name and a kingdom name for each player this time. A valid result would be: Aragon-Valyria, Legolas-Mirkwood, Gimli-Erebor. Be creative with the names and follow the format."

        if log.log_type == LogType.END_GAME:
            return f"The game has ended, and the end condition was: {log.elements[LogIndexType.END_GAME_CONDITION]}. The winner was: {log.elements[LogIndexType.END_GAME_WINNER]}."

        if log.log_type == LogType.ACCEPT_ALLIANCE:
            return f"After negotiations, the king {log.elements[LogIndexType.ACCEPT_ALLIANCE_ACCEPTER_PLAYER]} accept the alliance with the king {log.elements[LogIndexType.ACCEPT_ALLIANCE_ACCEPTED_PLAYER]} for {log.elements[LogIndexType.ACCEPT_ALLIANCE_TURNS]} turns."

        if log.log_type == LogType.ATTACK_KING:
            return f"{log.elements[LogIndexType.ATTACK_KING_ATTACKER_PLAYER]} attacks the kingdom of {log.elements[LogIndexType.ATTACK_KING_DEFENDER_PLAYER]} with the soldier {log.elements[LogIndexType.ATTACK_KING_ATTACKER_SOLDIER_ID]} who with a power of {log.elements[LogIndexType.ATTACK_KING_ATTACKER_SOLDIER_LVL]} destroy the king, and its kingdom."

        if log.log_type == LogType.ATTACK_SOLDIER:
            return f"{log.elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_PLAYER]} attacks the soldier {log.elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_SOLDIER_ID]} of the king {log.elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_PLAYER]} with the soldier {log.elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_SOLDIER_ID]}. The Attacker soldier has a power of {log.elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_SOLDIER_LVL]} and the defender soldier has a power of {log.elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_SOLDIER_LVL]}. After the battle, the attacker soldier end with {log.elements[LogIndexType.ATTACK_SOLDIER_ATTACKER_STATUS]} power, and the defender soldier end with {log.elements[LogIndexType.ATTACK_SOLDIER_DEFENDER_STATUS]} power."

        if log.log_type == LogType.ATTACK_TOWN:
            return f"{log.elements[LogIndexType.ATTACK_TOWN_ATTACKER_PLAYER]} attacks the town of {log.elements[LogIndexType.ATTACK_TOWN_DEFENDER_PLAYER]} with the soldier {log.elements[LogIndexType.ATTACK_TOWN_ATTACKER_SOLDIER_ID]}. The Attacker soldier has a power of {log.elements[LogIndexType.ATTACK_TOWN_ATTACKER_SOLDIER_LVL]}, and the town has a defense of {log.elements[LogIndexType.ATTACK_TOWN_DEFENDER_TOWN_LVL]}. After the battle, the town end with {log.elements[LogIndexType.ATTACK_TOWN_DEFENDER_TOWN_STATUS]} defense and the attacker soldier end with {log.elements[LogIndexType.ATTACK_TOWN_ATTACKER_STATUS]} power."

        if log.log_type == LogType.ATTACK_WALL:
            return f"{log.elements[LogIndexType.ATTACK_WALL_ATTACKER_PLAYER]} attacks the wall of {log.elements[LogIndexType.ATTACK_WALL_DEFENDER_PLAYER]} with the soldier {log.elements[LogIndexType.ATTACK_WALL_ATTACKER_SOLDIER_ID]}. The Attacker soldier has a power of {log.elements[LogIndexType.ATTACK_WALL_ATTACKER_SOLDIER_LVL]}, and the wall has a defense of {log.elements[LogIndexType.ATTACK_WALL_DEFENDER_WALL_LVL]}. After the battle, the wall end with {log.elements[LogIndexType.ATTACK_WALL_DEFENDER_WALL_STATUS]} defense and the attacker soldier end with {log.elements[LogIndexType.ATTACK_WALL_ATTACKER_STATUS]} power."

        if log.log_type == LogType.DECLINE_ALLIANCE:
            return f"After negotiations, the king {log.elements[LogIndexType.DECLINE_ALLIANCE_DECLINER_PLAYER]} decline the alliance with the king {log.elements[LogIndexType.DECLINE_ALLIANCE_DECLINED_PLAYER]}. Now {log.elements[LogIndexType.DECLINE_ALLIANCE_TURNS]} turns of peace won't be possible."

        if log.log_type == LogType.PROPOSE_ALLIANCE:
            return f"The king {log.elements[LogIndexType.PROPOSE_ALLIANCE_PROPOSER_PLAYER]} propose an alliance with the king {log.elements[LogIndexType.PROPOSE_ALLIANCE_RECEIVER_PLAYER]} for {log.elements[LogIndexType.PROPOSE_ALLIANCE_TURNS]} turns."

        if log.log_type == LogType.UPGRADE_SOLDIER:
            return f"The king {log.elements[LogIndexType.UPGRADE_SOLDIER_PLAYER]} decide to upgrade the soldier {log.elements[LogIndexType.UPGRADE_SOLDIER_SOLDIER_ID]} from level {log.elements[LogIndexType.UPGRADE_SOLDIER_OLD_LVL]} to level {log.elements[LogIndexType.UPGRADE_SOLDIER_CURRENT_LVL]} using {log.elements[LogIndexType.UPGRADE_SOLDIER_POINTS_USED]} resources."

        if log.log_type == LogType.UPGRADE_TOWN:
            return f"The management of the king {log.elements[LogIndexType.UPGRADE_TOWN_PLAYER]} makes the kingdom go from level {log.elements[LogIndexType.UPGRADE_TOWN_OLD_LVL]} to level {log.elements[LogIndexType.UPGRADE_TOWN_CURRENT_LVL]}."

        if log.log_type == LogType.UPGRADE_WALL:
            return f"The king {log.elements[LogIndexType.UPGRADE_WALL_PLAYER]} makes the wall go from level {log.elements[LogIndexType.UPGRADE_WALL_OLD_LVL]} to level {log.elements[LogIndexType.UPGRADE_WALL_CURRENT_LVL]} using {log.elements[LogIndexType.UPGRADE_WALL_POINTS_USED]} resources."

    def stop_process(self) -> None:
        """
        Stop the process to generate the story of the game
        """
        self._running = False

    def get_histories_count(self) -> int:
        """
        Get the number of histories generated

        Returns:
            int: The number of histories generated
        """
        return self._history_handler._counter

    def get_recent_update(self) -> str:
        """
        Get the most recent update of the history

        Returns:
            str: The most recent update of the history
        """
        return self._history_handler.get_last_history()

    def get_all_histories(self) -> list:
        """
        Get all the histories generated

        Returns:
            list: The list of histories generated
        """
        return self._history_handler.get_full_history()

    def get_history_resume(self) -> str:
        """
        Get the history resume

        Returns:
            str: The history resume
        """
        return self._history_handler._history_resume
