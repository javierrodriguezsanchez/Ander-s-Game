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
        self._first_node = None
        self._last_node = None
        self._counter = 0
        self._history_resume = ""

    def get_full_history(self) -> str:
        history = ""
        current_node = self._first_node
        while current_node is not None:
            history += current_node.get_history()
            current_node = current_node.next
        return history

    def add_entry(self, history: str, entry_log: str) -> None:
        """Add a new entry to the history

        Args:
            entry_log (str): The log to be added to the history
        """
        new_node = HistoryNode(self._counter, entry_log, history)
        if self._first_node is None:
            self._first_node = new_node
            self._last_node = new_node
        else:
            self._last_node.next = new_node
            new_node.prev = self._last_node
            self._last_node = new_node

        self._counter += 1

    def get_last_history(self) -> str:
        return self._last_node.get_history()
