import os
import random
from src.Agent.Agent import Agent
from src.Agent.Knowledge_Base import Knowledge_Base
from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Simulation_gestor.config_class import Config
from src.Llm.history_process import HistoryProcess
from src.Llm.llm_interface import LLMInterface
from src.Llm.log_manager import LogManager
from src.Simulation_gestor.simulation import Simulation
import importlib
import inspect


class SimulationInterface:
    """This class will be the connection point between the simulation and the user interface. It will be responsible for handling communication between the simulation, and the story generation process, as long as create an API for the user interface to interact with the simulation and ask for data."""

    def __init__(self) -> None:
        """Initialize the simulation interface."""
        self._log_manager = LogManager()
        self._history_process = HistoryProcess(self._log_manager, self.manage_history)
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
        another_simulation = True
        while another_simulation:

            # Get data from user
            self._get_information()
            self._set_simulation()
            self._get_game_to_print_index()

            # Start the history process
            self._history_process.start_process()

            # Run the simulator
            self._simulation.run()

            # Ask the user if they want to run another simulation
            another_simulation = self._ask_for_another_simulation()

        # End the history process
        self._history_process.stop_process()

    def manage_history(self, log):
        """Manage the history of the simulation"""
        raise NotImplementedError(
            "This method should be implemented by the child class."
        )

    def _ask_for_another_simulation(self):
        """Ask the user if they want to run another simulation"""

        raise NotImplementedError(
            "This method should be implemented by the child class."
        )


class SimulationInterfaceConsole(SimulationInterface):
    """This class will be responsible for handling the simulation interface through the console."""

    def _get_information(self):
        """Gather the necessary values to start the simulation"""
        kingdoms = self._get_amount_of_kingdoms()
        players = kingdoms
        iterations = self._get_amount_of_iterations()
        rounds_per_game = self._get_amount_of_rounds_per_game()
        verbose = self._get_verbose()

        created_kingdoms = self._create_kingdoms(kingdoms)
        created_players = self._create_players(players)

        self._simulation_config = Config(
            created_kingdoms, created_players, verbose, iterations, rounds_per_game
        )

    def _get_verbose(self):
        """Ask the user if they want to run the simulation in verbose mode"""
        # Ask the user
        prompt = "Do you want to run the simulation in verbose mode? (Y/N)"
        answer = input(prompt)

        # Clear the console
        self._clear_console()

        # Validate the answer
        while answer.lower() not in ["y", "n"]:
            self._clear_console()
            print("Please, enter a valid answer. (Y/N)")
            answer = input(prompt)

        return answer.lower() == "y"

    def _create_kingdoms(self, kingdoms: int):
        """Create the kingdoms for the simulation.

        Args:
            kingdoms (int): The amount of kingdoms that will be created.
        """
        # Create the kingdoms
        created_kingdoms = []
        for i in range(kingdoms):
            created_kingdoms.append(Kingdom())
        return created_kingdoms

    def _create_players(self, players: int):
        """Create the players for the simulation.

        Args:
            players (int): The amount of players that will be created.
        """
        # Create the players
        created_players = []
        manual_assignation = self._ask_for_random_strategy_assignation()

        # Load the strategies
        strategies = self._load_strategies()

        for i in range(players):
            created_players.append(
                Agent(self._ask_for_strategy(strategies, manual_assignation))
            )

        return created_players

    def _ask_for_strategy(
        self, strategies: list[tuple[str, type[Strategy]]], manual_choice: bool
    ) -> Strategy:
        """Ask the user for a strategy to assign to the agent"""
        # Print the strategies

        index = random.randint(0, len(strategies) - 1)
        if manual_choice:
            self._clear_console()
            print("Select a strategy to assign to the agent: ")
            for i, strategy in enumerate(strategies):
                print(f"{i}. {strategy[0]}")

            # Ask the user
            prompt = "Enter the index of the strategy: "
            index = input(prompt)

            # Validate the input
            while (
                not index.isdigit() or int(index) < 0 or int(index) >= len(strategies)
            ):
                print("Please, enter a valid index for the strategy. ")
                index = input(prompt)

        index = int(index)
        # Caso especial de MultipleStrategy
        if strategies[index][0] == "MultipleStrategy":
            return self._ask_for_multiple_strategy(strategies, index, manual_choice)

        return strategies[index][1]()

    def _ask_for_multiple_strategy(
        self,
        strategies: list[tuple[str, type[Strategy]]],
        index: int,
        manual_choice,
    ) -> Strategy:
        """Ask the user for the strategies to assign to the MultipleStrategy"""

        amount = "2"
        if manual_choice:
            # Ask the user how many strategies they want to assign
            prompt = (
                "How many strategies do you want to assign to the MultipleStrategy? "
            )
            amount = input(prompt)

            # Validate the input
            while not amount.isdigit() or int(amount) < 2:
                print("Please, enter a valid amount of strategies. ")
                amount = input(prompt)

        selected_strategies = []
        priorities = []
        # Get the strategies
        for i in range(int(amount)):
            if manual_choice:
                print(f"Select the strategy {i + 1}: ")
            selected_strategy = self._ask_for_strategy(strategies, manual_choice)
            selected_strategies.append(selected_strategy)

            priority = str(random.randint(0, 10))

            if manual_choice:
                # Ask for the priority
                prompt = "Enter the priority of the strategy: "
                priority = input(prompt)

                # Validate the input
                while not priority.isdigit() or int(priority) < 0:
                    print("Please, enter a valid priority for the strategy. ")
                    priority = input(prompt)

            priorities.append(int(priority))

        return strategies[index][1](selected_strategies, priorities)

    def _set_simulation(self):
        """Set the configuration for the simulation."""
        super()._set_simulation()

    def _get_amount_of_kingdoms(self):
        """Ask the user how many kingdoms will use"""
        # Clear the console
        self._clear_console()

        # Ask the user for the kingdoms
        prompt = "How many kingdoms will be in the simulation? "
        kingdoms = input(prompt)
        while not kingdoms.isdigit():
            self._clear_console()
            print("Please, enter a valid number for the amount of kingdoms. ")
            kingdoms = input(prompt)

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
        prompt = "How many iterations the simulation will perform? "
        iterations = input(prompt)

        # Validate input
        while not iterations.isdigit():
            self._clear_console()
            print("Please, enter a valid number for the amount of iterations. ")
            iterations = input(prompt)

        return int(iterations)

    def _get_game_to_print_index(self):
        """Get the index of the game to print. The index needs to be between 0 and the number of iterations. For better performance, its recomendable to chose the first one"""
        # Clear the console
        self._clear_console()

        # Ask for the index
        prompt = "Which game do you want to print? (0 - N) "
        index = input(prompt)

        # Validate input
        while (
            not index.isdigit()
            or int(index) < 0
            or int(index) >= self._simulation_config.iterations
        ):
            self._clear_console()
            print(
                "Please, enter a valid number for the index. Remember that it needs to be between 0 and N. "
            )
            index = input(prompt)

        # Set the game to print
        self._simulation.change_game_to_print(int(index))

    def _get_amount_of_rounds_per_game(self):
        """Ask the user how many rounds will have each game"""
        # Clear the console
        self._clear_console()

        # Ask for the rounds
        prompt = "How many rounds will have each game? "
        rounds = input(prompt)

        # Validate input
        while not rounds.isdigit():
            self._clear_console()
            print("Please, enter a valid number for the amount of rounds. ")
            rounds = input(prompt)

        return int(rounds)

    def _load_strategies(self) -> list[tuple[str, type[Strategy]]]:
        """Load the strategies from the strategies folder"""
        # Get the path to the strategies folder
        strategies_folder = os.path.join(
            os.getcwd(), "src", "Strategies", "Implementations"
        )

        # Get the files in the folder
        files = os.listdir(strategies_folder)

        # Get the strategies
        strategies = []
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Get the module name
                module_name = file[:-3]

                # Import the module
                module = importlib.import_module(
                    f"src.Strategies.Implementations.{module_name}"
                )

                # Get the classes in the module
                classes = inspect.getmembers(module, inspect.isclass)

                # Get the strategies
                for name, strategy in classes:
                    if issubclass(strategy, Strategy) and strategy != Strategy:
                        strategies.append((name, strategy))

        return strategies

    def _ask_for_random_strategy_assignation(self) -> bool:
        """Ask the user if they want to assign a strategy to the agents"""
        # Ask the user
        prompt = "Do you want to manually assign the strategies to the agents? (Y/N)"
        answer = input(prompt)

        # Clear the console
        self._clear_console()

        # Validate the answer
        while answer.lower() not in ["y", "n"]:
            self._clear_console()
            print("Please, enter a valid answer. (Y/N)")
            answer = input(prompt)

        return answer.lower() == "y"

    def manage_history(self, log):
        """Manage the history of the simulation"""
        print(log)

    def _ask_for_another_simulation(self):
        """Ask the user if they want to run another simulation"""

        # Ask the user
        prompt = "Do you want to run another simulation? (Y/N)"
        answer = input(prompt)

        # Clear the console
        self._clear_console()

        # Validate the answer
        while answer.lower() not in ["y", "n"]:
            self._clear_console()
            print("Please, enter a valid answer. (Y/N)")
            answer = input(prompt)

        return answer.lower() == "y"
