import threading
from src.Llm.history_handler import HistoryHandler
from src.Llm.llm_interface import LLMInterface
from src.Llm.log_manager import LogManager, LogNode


class HistoryProcess:
    def __init__(self, log_manager: LogManager):
        self._llm_interface = LLMInterface()
        self._history_handler = HistoryHandler()
        self._log_manager = log_manager
        self._running = False

    def add_log(self, log) -> None:
        self._logs_queue.append(log)

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

                # Update the history resume
                self._history_handler._history_resume = history_resume

                # Add the created history to the history handler
                self._history_handler.add_entry(history, log_text)

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
        return str(log)

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
