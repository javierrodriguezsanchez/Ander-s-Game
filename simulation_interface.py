import os
from config_class import Config
from history_process import HistoryProcess
from llm_interface import LLMInterface
from log_manager import LogManager
from simulation import Simulation


class SimulationInterface:
    """This class will be the connection point between the simulation and the user interface. It will be responsible for handling communication between the simulation, and the story generation process, as long as create an API for the user interface to interact with the simulation and ask for data."""

    def __init__(self) -> None:
        """Initialize the simulation interface."""
        self._log_manager = LogManager()
        self._history_process = HistoryProcess(self._log_manager)
        self._simulation_config = None
        self._simulation = None

    def _get_information(self):
        """Gather the necessary values to start the simulation"""
        raise NotImplementedError(
            "This method should be implemented by the child class."
        )

    def _get_game_to_print_index(self):
        """Get the index of the game to print. The index needs to be between 0 and the number of iterations. For better performance, its recomendable to chose the first one"""
        raise NotImplementedError(
            "This method should be implemented by the child class."
        )

    def _set_simulation(self):
        """Set the configuration for the simulation."""
        self._simulation = Simulation(self._simulation_config, self._log_manager)

    def run(self):
        """Run the simulation"""

        # Get data from user
        self._get_information()
        self._set_simulation()
        self._get_game_to_print_index()

        # Run the simulator
        self._simulation.run()

        # Start the history process
        self._history_process.start_process()


class SimulationInterfaceConsole(SimulationInterface):
    """This class will be responsible for handling the simulation interface through the console."""

    def _get_information(self):
        """Gather the necessary values to start the simulation"""
        kingdoms = self._get_amount_of_kingdoms()
        players = kingdoms
        iterations = self._get_amount_of_iterations()

        self._simulation_config = Config(kingdoms, players, iterations)

    def _set_simulation(self):
        """Set the configuration for the simulation."""
        super()._set_simulation()

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

    def _get_game_to_print_index(self):
        """Get the index of the game to print. The index needs to be between 0 and the number of iterations. For better perfomance, its recomendable to chose the first one"""
        # Clear the console
        self._clear_console()

        # Ask for the index
        promp = "Which game do you want to print? (0 - N)"
        index = input(promp)

        # Validate input
        while (
            not index.isdigit()
            or int(index) < 0
            or int(index) >= self._simulation_config.number_of_simulations
        ):
            self._clear_console()
            print(
                "Please, enter a valid number for the index. Remember that it needs to be between 0 and N."
            )
            index = input(promp)

        # Set the game to print
        self._simulation.change_game_to_print(int(index))
