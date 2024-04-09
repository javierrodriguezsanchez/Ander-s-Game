class LogManager:

    def __init__(self) -> None:
        self._games: dict[int, LogNode] = {}
        self._current_game_index = 0

    # Todo: Poner los nodos del log manager
    # Todo: Terminar de definir lo referente al LogManager
    def add_log(self, log):
        # Todo: Implementar el método de añadir log
        raise NotImplementedError("Not implemented yet")

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


class LogNode:
    def __init__(self, log):
        self.log = log
        self.next = None
