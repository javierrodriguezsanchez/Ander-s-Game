import os
from config_class import Config
from history_process import HistoryProcess
from llm_interface import LLMInterface
from simulation import Simulation


class SimulationInterface:
    """This class will be the connection point between the simulation and the user interface. It will be responsible for handling communication between the simulation, and the story generation process, as long as create an API for the user interface to interact with the simulation and ask for data."""

    def __init__(self) -> None:
        """Initialize the simulation interface."""
        self._history_process = HistoryProcess()
        self._llm_interface = LLMInterface()
        self._simulation_config = None
        self._simulation = None

    def get_information(self):
        """Gather the necessary values to start the simulation"""
        raise NotImplementedError(
            "This method should be implemented by the child class."
        )

    def set_configuration(self):
        """Set the configuration for the simulation."""
        self._simulation = Simulation(self._simulation_config)


class SimulationInterfaceConsole(SimulationInterface):
    """This class will be responsible for handling the simulation interface through the console."""

    def get_information(self):
        """Gather the necessary values to start the simulation"""
        kingdoms = self._get_amount_of_kingdoms()
        players = kingdoms
        iterations = self._get_amount_of_iterations()

        self._simulation_config = Config(kingdoms, players, iterations)

    def set_configuration(self):
        """Set the configuration for the simulation."""
        super().set_configuration()

    def _get_amount_of_kingdoms(self):
        """Ask the user how many kingdoms will use"""
        # Clear the console
        self._clear_console()

        # Ask the user for the kingdoms
        promt = "How many kingdoms will be in the simulation?"
        kingdoms = input(promt)
        while not kingdoms.isdigit():
            self._clear_console()
            print("Please, enter a valid number for the amount of kingdoms.")
            kingdoms = input(promt)

        return int(kingdoms)

    def _clear_console(self):
        """Clear the console"""
        # Check Operating System
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def _get_amount_of_iterations(self):
        """Ask the user how many iterations of the simulation will be"""
        # Clear the console
        self._clear_console()

        # Ask for iterations
        promp = "How many iterations the simulation will perform?"
        iterations = input(promp)

        # Validate input
        while not iterations.isdigit():
            self._clear_console()
            print("Please, enter a valid number for the amount of iterations.")
            iterations = input(promp)

        return int(iterations)
