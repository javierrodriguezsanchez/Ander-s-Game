from llm_interface import LLMInterface


class HistoryNode:
    def __init__(self, history_id: int, entry_log, history) -> None:
        self._log = entry_log
        self.next = None
        self.prev = None
        self._id = history_id
        self._history = history

    def get_history(self) -> str:
        return self._history

    def get_id(self) -> int:
        return self._id


class HistoryHandler:
    def __init__(self) -> None:
        self.first_node = None
        self.last_node = None
        self._counter = 0
        self._history_resume = ""
        self._llm_interface = LLMInterface()

    def get_full_history(self) -> str:
        history = ""
        current_node = self.first_node
        while current_node is not None:
            history += current_node.get_history()
            current_node = current_node.next
        return history

    def add_entry(self, entry_log: str) -> None:
        """Add a new entry to the history

        Args:
            entry_log (str): The log to be added to the history
        """

        history, history_resume = self._llm_interface.generate_history(
            self._history_resume, entry_log
        )
        self._history_resume = history_resume

        new_node = HistoryNode(self._counter, entry_log, history)
        if self.first_node is None:
            self.first_node = new_node
            self.last_node = new_node
        else:
            self.last_node.next = new_node
            new_node.prev = self.last_node
            self.last_node = new_node
