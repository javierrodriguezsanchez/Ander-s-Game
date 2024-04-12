from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import (
    Media,
    Bad_Ending_for_i,
    Defensive_Ending_For_i,
    Strongest_Army,
    Weakest_Army,
)
import random


class DefendStrategy(Strategy):
    """
    Upgrades his wall and army for defend himself.

    Attacks with a low probability a kingdom with a very low relation.

    Do not offer alliance and only accept propotions from non enemy (reel > 0) kingdoms
    """

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int] = [],
        Allies: list[int] = []
    ) -> int:

        enemy = -1

        for i in range(len(reels)):
            if reels[i] <= -50:
                enemy = i

        rand = random.random()
        if rand < 0.2:
            best_ending = Bad_Ending_for_i(posible_actions, enemy, my_index)
            return best_ending

        best_ending = Defensive_Ending_For_i(posible_actions, my_index)
        return best_ending

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
