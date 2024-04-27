from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Defensive_Ending_For_i, Bad_Ending_for_i
import random


class AlliesStrategy(Strategy):
    """
    Make decisions accordin to the relations with other kingdoms
    """

    def Select(self, context: dict) -> int: 
        my_index = context['index']
        posible_actions = context['endings']
        reels = context['relations']
        Allies = context['allies']

        current_state = posible_actions[0]

        lower_reel = 2000
        enemy = -1
        for i in range(len(reels)):
            if i == my_index or not current_state[i].king_alive:
                continue

            if reels[i] < lower_reel:
                lower_reel = reels[i]
                enemy = i

        attack_ending = Bad_Ending_for_i(posible_actions, enemy, my_index)
        defensive_ending = Defensive_Ending_For_i(posible_actions, my_index)

        if lower_reel < -10:
            return attack_ending
        elif lower_reel < 0:
            if Allies[enemy] == 0:
                rand = random.random()
                if rand < 0.8:
                    return attack_ending
                else:
                    return defensive_ending
            elif Allies[enemy] > 0:
                rand = random.random()
                if rand < 0.2:
                    return attack_ending
                else:
                    return defensive_ending
        else:
            return defensive_ending

    def ChooseAllies(self, context: dict) -> list[bool]:
        my_index = context['index']
        Kingdoms = context['state']
        reels = context['relations']
        Allies = context['allies']

        prop = [False] * len(Kingdoms)
        to_propose = []

        for i in range(len(reels)):
            if i == my_index or not Kingdoms[i].king_alive or Allies[i] > 0:
                continue

            if reels[i] >= 10:
                to_propose.append(i)
            elif reels[i] > 0:
                rand = random.random()
                if rand < 0.5:
                    to_propose.append(i)

        for i in to_propose:
            prop[i] = True

        return prop

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