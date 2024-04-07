from history_process import HistoryProcess
from llm_interface import LLMInterface


class SimulationInterface:
    """This class will be the connection point between the simulation and the user interface. It will be responsible for handling communication between the simulation, and the story generation process, as long as create an API for the user interface to interact with the simulation and ask for data."""

    def __init__(self) -> None:
        """Initialize the simulation interface."""
        self._history_process = HistoryProcess()
        self._llm_interface = LLMInterface()

    def ask_for_parameters(self):
        """Ask for the parameters to the user interface."""
        pass
