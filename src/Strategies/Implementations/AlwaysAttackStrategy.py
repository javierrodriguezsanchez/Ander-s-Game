from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
import random


class AlwaysAttackStrategy(Strategy):
    def __init():
        pass

    def Select(self, context: dict) -> int:
        my_index = context['index']
        posible_actions = context['endings']
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

    def ChooseAllies(self, context: dict) -> list[bool]:
        Kingdoms = context['state']
        return [False] * len(Kingdoms)

    def AcceptAlliance(self, context: dict) -> bool:
        prop_index = context['reign']
        reels = context['relations']

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