from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Bad_Ending_for_i, Defensive_Ending_For_i
import random


class DefendStrategy(Strategy):
    """
    Upgrades his wall and army for defend himself.

    Attacks with a low probability a kingdom with a very low relation.

    Do not offer alliance and only accept propotions from non enemy (reel > 0) kingdoms
    """

    def Select(self, context: dict) -> int:
        my_index = context['index']
        posible_actions = context['endings']
        reels = context['relations']

        enemy = -1

        for i in range(len(reels)):
            if reels[i] <= -10:
                enemy = i

        rand = random.random()
        if rand < 0.2:
            best_ending = Bad_Ending_for_i(posible_actions, enemy, my_index)
            return best_ending

        best_ending = Defensive_Ending_For_i(posible_actions, my_index)
        return best_ending

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