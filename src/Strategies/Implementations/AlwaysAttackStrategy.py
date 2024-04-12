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


class AlwaysAttackStrategy(Strategy):
    def __init():
        pass
    def Select(self,my_index: int,posible_actions: list[list[Kingdom]],reels: list[int] = [],Allies: list[int] = []) -> int:
        return max(range(len(posible_actions)), key=lambda x: self.Situation(posible_actions[x], my_index))

    def Situation(self, Kingdoms: list[Kingdom], index: int) -> int:
        returnValue = 1000 * len([x for x in Kingdoms if not x.king_alive])
        for k in range(len(Kingdoms)):
            if k == index:
                continue
            returnValue -= Kingdoms[k].population
            returnValue -= Kingdoms[k].walls
            returnValue -= len(Kingdoms[k].army)
        return returnValue

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
