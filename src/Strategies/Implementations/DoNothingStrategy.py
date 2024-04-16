from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
import random


class DoNothingStrategy(Strategy):
    '''
    Its hard to explain this one :(
    '''

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int] = [],
        Allies: list[int] = []
    ) -> int:

        return 0

    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int]
    ) -> list[bool]:

        return [False] * len(Kingdoms)

    def AcceptAlliance(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        prop_index: int,
        reels: list[int],
        Allies: list[int]
    ) -> bool:

        if reels[prop_index] >= 10:
            return True
        elif reels[prop_index] > 0:
            rand = random.random()
            if rand < 0.5:
                return True
            else:
                return False
        else:
            return False
